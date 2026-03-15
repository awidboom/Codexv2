import asyncio
import argparse
import csv
import re
from datetime import date, datetime, timedelta
from pathlib import Path

from playwright.async_api import async_playwright

PORTAL_URL = "https://oitco.hylandcloud.com/CDPHERMPublicAccess/index.html"
SEARCH_TYPE_TEXT = "CDPHERM Air Stationary Source Enforcement"
DEFAULT_DAYS_BACK = 7
DEFAULT_DOWNLOAD_DIR = Path(__file__).resolve().parent / "downloads"
DEFAULT_MANIFEST_NAME = "cdphe_download_manifest.csv"
DEFAULT_HEADLESS = False


def clean_part(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"[\\/:*?\"<>|]", "_", s)
    s = re.sub(r"\s+", " ", s)
    return s[:120] or "unknown"


def fmt_date(s: str) -> str:
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", s or "")
    if m:
        mm, dd, yy = m.groups()
        yyyy = int(yy) if len(yy) == 4 else 2000 + int(yy)
        return f"{yyyy:04d}-{int(mm):02d}-{int(dd):02d}"
    return (s or "").replace("/", "-") or "date"


def parse_any_date(value: str) -> date:
    value = (value or "").strip()
    if not value:
        raise ValueError("Empty date")
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value!r} (use YYYY-MM-DD or MM/DD/YYYY)")


def month_bounds(month: str) -> tuple[date, date]:
    m = re.fullmatch(r"(\d{4})-(\d{2})", (month or "").strip())
    if not m:
        raise ValueError("Month must be YYYY-MM (example: 2025-12)")
    year = int(m.group(1))
    mon = int(m.group(2))
    if not (1 <= mon <= 12):
        raise ValueError("Month must be between 01 and 12")
    start = date(year, mon, 1)
    if mon == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, mon + 1, 1)
    end = next_month - timedelta(days=1)
    return start, end


def to_portal_date(d: date) -> str:
    return d.strftime("%m/%d/%Y")


async def wait_for_rows(page):
    await page.wait_for_selector("#obpa-grid tbody tr:has(td)", timeout=30_000)


async def fetch_pdf(context, url, dest):
    resp = await context.request.get(url)
    if not resp.ok:
        raise RuntimeError(f"Download failed ({resp.status}): {url}")
    dest.write_bytes(await resp.body())


async def run(from_date: str, to_date: str | None, download_dir: Path, manifest_csv: Path, headless: bool) -> None:
    download_dir.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(PORTAL_URL, wait_until="load", timeout=90_000)

        await page.get_by_label("Search Type", exact=False).select_option(label=SEARCH_TYPE_TEXT)
        await page.get_by_label("From Date", exact=False).fill(from_date)
        if to_date:
            filled = False
            for label in ["To Date", "Through Date", "Thru Date", "End Date", "To"]:
                try:
                    await page.get_by_label(label, exact=False).fill(to_date)
                    filled = True
                    break
                except Exception:
                    continue
            if not filled:
                print("Warning: could not find a 'To Date' field on the page; running with From Date only.")
        await page.get_by_role("button", name="Search").click()

        await wait_for_rows(page)

        headers = page.locator("#obpa-grid thead th")
        hcount = await headers.count()
        header_texts = [(await headers.nth(i).inner_text()).strip().lower() for i in range(hcount)]

        def find_idx(name):
            for i, h in enumerate(header_texts):
                if name in h:
                    return i
            return -1

        idx_date = find_idx("document date")
        idx_company = find_idx("company")
        idx_case = find_idx("case")

        rows = page.locator("#obpa-grid tbody tr:has(td)")
        visible_rows = []
        for i in range(await rows.count()):
            r = rows.nth(i)
            if await r.is_visible():
                visible_rows.append(r)

        if not visible_rows:
            print("No results detected.")
            await browser.close()
            return

        records = []
        seen_files = set()
        seen_urls = set()
        for row in visible_rows:
            tds = row.locator("td")
            doc_date = await tds.nth(idx_date).inner_text() if idx_date >= 0 else ""
            company = await tds.nth(idx_company).inner_text() if idx_company >= 0 else ""
            case_num = await tds.nth(idx_case).inner_text() if idx_case >= 0 else ""
            filename = f"{fmt_date(doc_date)}__{clean_part(company)}__{clean_part(case_num)}.pdf"

            target = row.locator("td.js-obpa_icon svg").first
            if await target.count() == 0:
                target = row.locator("td.js-obpa_action button").first

            popup = None
            for attempt in range(2):
                try:
                    popup_task = asyncio.create_task(page.wait_for_event("popup", timeout=30_000))
                    await target.click()
                    popup = await popup_task
                    break
                except Exception:
                    if attempt == 0:
                        await page.wait_for_timeout(500)
                        continue
                    print(f"Warning: could not open document popup for {filename}; skipping.")
                    popup = None
            if popup is None:
                continue
            try:
                await popup.wait_for_load_state("domcontentloaded", timeout=90_000)
            except Exception:
                pass
            try:
                await popup.wait_for_url("**/*", timeout=90_000)
            except Exception:
                pass

            pdf_url = popup.url
            dest = download_dir / filename

            if pdf_url in seen_urls or dest.name in seen_files:
                await popup.close()
                continue

            seen_urls.add(pdf_url)
            seen_files.add(dest.name)

            if dest.exists() and dest.stat().st_size > 0:
                print(f"Using existing {dest}")
            else:
                await fetch_pdf(context, pdf_url, dest)
                print(f"Saved {dest}")
            await popup.close()

            records.append(
                {
                    "file_name": dest.name,
                    "pdf_url": pdf_url,
                    "document_date": doc_date,
                    "company": company,
                    "case_number": case_num,
                }
            )

        if records:
            with manifest_csv.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["file_name", "pdf_url", "document_date", "company", "case_number"],
                )
                writer.writeheader()
                writer.writerows(records)
            print(f"Wrote manifest {manifest_csv}")

        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download CDPHE air enforcement PDFs and write a download manifest.")
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--month",
        help="Download one calendar month (YYYY-MM), e.g. 2025-12.",
    )
    date_group.add_argument(
        "--from-date",
        help="Portal 'From Date' (YYYY-MM-DD or MM/DD/YYYY). Defaults to today minus 7 days.",
    )
    parser.add_argument(
        "--to-date",
        help="Optional portal 'To Date' (YYYY-MM-DD or MM/DD/YYYY).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_DAYS_BACK,
        help="Days back from today when --from-date/--month not provided (default: 7).",
    )
    parser.add_argument(
        "--download-dir",
        type=Path,
        default=DEFAULT_DOWNLOAD_DIR,
        help="Directory to save PDFs and the manifest (default: ./downloads).",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Manifest CSV path (default: <download-dir>/cdphe_download_manifest.csv).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=DEFAULT_HEADLESS,
        help="Run the browser in headless mode.",
    )
    args = parser.parse_args()

    if args.month:
        start, end = month_bounds(args.month)
        from_date = to_portal_date(start)
        to_date = to_portal_date(end)
    elif args.from_date:
        from_date = to_portal_date(parse_any_date(args.from_date))
        to_date = to_portal_date(parse_any_date(args.to_date)) if args.to_date else None
    else:
        start = date.today() - timedelta(days=max(args.days, 0))
        from_date = to_portal_date(start)
        to_date = to_portal_date(parse_any_date(args.to_date)) if args.to_date else None

    download_dir = args.download_dir
    manifest_csv = args.manifest or (download_dir / DEFAULT_MANIFEST_NAME)
    asyncio.run(run(from_date=from_date, to_date=to_date, download_dir=download_dir, manifest_csv=manifest_csv, headless=args.headless))
