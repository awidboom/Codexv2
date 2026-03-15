import argparse
import subprocess
import sys
from pathlib import Path


def run_script(script_name: str, args: list[str]) -> None:
    script_path = Path(__file__).resolve().parent / script_name
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CDPHE download + processing pipeline.")
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument("--month", help="Download one calendar month (YYYY-MM), e.g. 2025-12.")
    date_group.add_argument("--from-date", help="Portal 'From Date' (YYYY-MM-DD or MM/DD/YYYY).")
    parser.add_argument("--to-date", help="Optional portal 'To Date' (YYYY-MM-DD or MM/DD/YYYY).")
    parser.add_argument("--days", type=int, help="Days back from today when --from-date/--month not provided.")
    parser.add_argument("--headless", action="store_true", help="Run the downloader browser headless.")
    parser.add_argument(
        "--cleanup-pdfs",
        action="store_true",
        default=False,
        help="Delete the PDFs for this run after processing (default: keep PDFs).",
    )
    args = parser.parse_args()

    downloader_args: list[str] = []
    if args.month:
        downloader_args += ["--month", args.month]
    if args.from_date:
        downloader_args += ["--from-date", args.from_date]
    if args.to_date:
        downloader_args += ["--to-date", args.to_date]
    if args.days is not None:
        downloader_args += ["--days", str(args.days)]
    if args.headless:
        downloader_args += ["--headless"]

    processor_args: list[str] = ["--manifest-only"]
    if args.cleanup_pdfs:
        processor_args.append("--cleanup-pdfs")

    run_script("cdphe_downloader.py", downloader_args)
    run_script("cdphe_processor.py", processor_args)


if __name__ == "__main__":
    main()
