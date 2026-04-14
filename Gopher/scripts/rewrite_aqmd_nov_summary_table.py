from __future__ import annotations

from pathlib import Path

from docx import Document

from aqmd_nov_summary_rows import AQMD_NOV_SUMMARY_HEADERS, AQMD_NOV_SUMMARY_ROWS


ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = ROOT / "outputs" / "Ecobat_violation_timeline.docx"


def clear_table(table) -> None:
    tbl = table._tbl
    for row in list(table.rows):
        tbl.remove(row._tr)


def main() -> None:
    doc = Document(DOCX_PATH)
    table = doc.tables[1]
    while len(table.columns) < len(AQMD_NOV_SUMMARY_HEADERS):
        table.add_column(table.columns[-1].width)
    clear_table(table)

    header_cells = table.add_row().cells
    for idx, header in enumerate(AQMD_NOV_SUMMARY_HEADERS):
        header_cells[idx].text = header

    for item in AQMD_NOV_SUMMARY_ROWS:
        row = table.add_row().cells
        row[0].text = item["notice"]
        row[1].text = item["violation_date"]
        row[2].text = item["issue_date"]
        row[3].text = item["status"]
        row[4].text = item["rules"]
        row[5].text = item["violation_description"]
        row[6].text = item["ecobat_response"]
        row[7].text = item["scaqmd_response"]
        row[8].text = item["offered_penalty"]

    doc.save(DOCX_PATH)
    print(f"Updated {DOCX_PATH}")


if __name__ == "__main__":
    main()
