import argparse
import csv
import importlib.util
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener

from pypdf.errors import DependencyError


def _is_blank(val):
    if val is None:
        return True
    s = str(val).strip()
    return s == "" or s.lower() == "nan"


def _download_pdf(opener, url, timeout=30, retries=3, backoff_sec=1.5):
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; udaq-permitting/1.0)"})
            with opener.open(req, timeout=timeout) as resp:
                return resp.read()
        except (HTTPError, URLError, TimeoutError, OSError) as e:
            last_err = e
            if attempt < retries:
                time.sleep(backoff_sec * attempt)
    return None


def _load_scraper_module():
    scrape_path = Path(__file__).resolve().parent / "scrape_permits.py"
    spec = importlib.util.spec_from_file_location("scrape_permits", scrape_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_csv", default="permits_all.csv", help="Input CSV path")
    parser.add_argument("--out", dest="out_csv", default="permits_all_reprocessed.csv", help="Output CSV path")
    parser.add_argument("--max", type=int, default=None, help="Limit number of unknown rows to reprocess")
    parser.add_argument("--only-url", action="append", default=[], help="Process only rows with this exact PDFLink (repeatable)")
    parser.add_argument("--update-existing-nsr", action="store_true", help="Overwrite NSR_Classification when a parsed value is available")
    parser.add_argument("--timeout", type=int, default=30, help="Per-download timeout (seconds)")
    args = parser.parse_args(argv)

    scraper = _load_scraper_module()
    parse_pdf_v2 = scraper.parse_pdf_v2

    opener = build_opener(ProxyHandler({}))

    with open(args.in_csv, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if not fieldnames:
        raise SystemExit(f"No header found in {args.in_csv}")

    target_rows = []
    for i, row in enumerate(rows):
        nsr = row.get("NSR_Classification", "")
        if args.only_url:
            if (row.get("PDFLink") or "").strip() in {u.strip() for u in args.only_url if u.strip()}:
                target_rows.append(i)
            continue
        if _is_blank(nsr) or "unknown" in str(nsr).lower():
            target_rows.append(i)

    if args.only_url:
        print(f"Loaded {len(rows)} rows; targeted rows: {len(target_rows)}")
    else:
        print(f"Loaded {len(rows)} rows; unknown NSR_Classification: {len(target_rows)}")

    updated = 0
    attempted = 0
    parse_dependency_errors = 0
    parse_other_errors = 0
    warned_dependency = False
    cache = {}

    pdf_fields = [
        "ApprovalOrderID",
        "SIC_Code",
        "SourceContactName",
        "SourceContactPhone",
        "SourceContactEmail",
        "UTM_Easting",
        "UTM_Northing",
        "UTM_Zone",
        "UTM_Datum",
        "GeneralDescription",
        "NSR_Classification",
        "Source_Classification",
        "Applicable_Federal_Standards",
        "Project_Description",
        "Project_CO2e_TPY",
        "Project_CO_TPY",
        "Project_NOx_TPY",
        "Project_PM10_TPY",
        "Project_PM25_TPY",
        "Project_SO2_TPY",
        "Project_VOC_TPY",
        "Project_Total_HAPs_TPY",
        "Source_CO2e_TPY",
        "Source_CO_TPY",
        "Source_NOx_TPY",
        "Source_PM10_TPY",
        "Source_PM25_TPY",
        "Source_SO2_TPY",
        "Source_VOC_TPY",
        "Source_Total_HAPs_TPY",
    ]

    to_process = target_rows
    if args.max:
        to_process = target_rows[: args.max]

    for n, idx in enumerate(to_process, 1):
        row = rows[idx]
        url = row.get("PDFLink", "")
        if _is_blank(url):
            continue

        attempted += 1
        if url in cache:
            parsed = cache[url]
        else:
            pdf_bytes = _download_pdf(opener, url, timeout=args.timeout)
            if not pdf_bytes:
                cache[url] = None
                continue
            try:
                parsed = parse_pdf_v2(pdf_bytes)
            except DependencyError:
                parse_dependency_errors += 1
                if not warned_dependency:
                    warned_dependency = True
                    print(
                        "Note: some PDFs are AES-encrypted and require `cryptography>=3.1` for pypdf to decrypt. "
                        "Install with `pip install cryptography` and re-run to reduce remaining unknowns.",
                        flush=True,
                    )
                parsed = None
            except Exception:
                parse_other_errors += 1
                parsed = None
            cache[url] = parsed

        if not parsed:
            continue

        before = (row.get("NSR_Classification") or "").strip()
        for k in pdf_fields:
            if k not in fieldnames:
                continue
            if _is_blank(row.get(k, "")) and not _is_blank(parsed.get(k, "")):
                row[k] = parsed.get(k, "")

        # Optionally recompute NSR even when already populated.
        if args.update_existing_nsr and "NSR_Classification" in fieldnames:
            parsed_nsr = (parsed.get("NSR_Classification") or "").strip()
            if not _is_blank(parsed_nsr):
                row["NSR_Classification"] = parsed_nsr

        after = (row.get("NSR_Classification") or "").strip()
        if (_is_blank(before) and not _is_blank(after)) or (args.update_existing_nsr and before != after):
            updated += 1

        if n % 25 == 0:
            print(f"Reprocessed {n}/{len(to_process)} unknown rows (updated {updated})", flush=True)

    # Recompute unknown count
    unknown_after = 0
    for row in rows:
        nsr = row.get("NSR_Classification", "")
        if _is_blank(nsr) or "unknown" in str(nsr).lower():
            unknown_after += 1

    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.out_csv}")
    print(f"Attempted downloads: {attempted}; updated NSR_Classification: {updated}")
    if parse_dependency_errors:
        print(f"Parse failures due to missing cryptography: {parse_dependency_errors}")
    if parse_other_errors:
        print(f"Other parse failures: {parse_other_errors}")
    print(f"Unknown NSR_Classification after: {unknown_after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
