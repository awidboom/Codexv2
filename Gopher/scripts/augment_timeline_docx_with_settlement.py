from __future__ import annotations

from pathlib import Path

from docx import Document

from settlement_letter_data import SETTLEMENT_BY_NOTICE, SETTLEMENT_SOURCE_NOTE


ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = ROOT / "outputs" / "Ecobat_violation_timeline.docx"


def ensure_columns(table) -> tuple[int, int]:
    headers = [cell.text.strip() for cell in table.rows[0].cells]

    if "SCAQMD Response (Global Settlement Letter)" in headers:
        response_idx = headers.index("SCAQMD Response (Global Settlement Letter)")
    else:
        table.add_column(table.columns[-1].width)
        response_idx = len(table.columns) - 1
        table.rows[0].cells[response_idx].text = "SCAQMD Response (Global Settlement Letter)"

    headers = [cell.text.strip() for cell in table.rows[0].cells]
    if "Offered Penalty (Global Settlement Letter)" in headers:
        penalty_idx = headers.index("Offered Penalty (Global Settlement Letter)")
    else:
        table.add_column(table.columns[-1].width)
        penalty_idx = len(table.columns) - 1
        table.rows[0].cells[penalty_idx].text = "Offered Penalty (Global Settlement Letter)"

    return response_idx, penalty_idx


def main() -> None:
    doc = Document(DOCX_PATH)
    nov_table = doc.tables[1]
    response_idx, penalty_idx = ensure_columns(nov_table)

    for row in nov_table.rows[1:]:
        notice = row.cells[0].text.strip()
        payload = SETTLEMENT_BY_NOTICE.get(
            notice,
            {
                "response": f"Not mapped. Source note: {SETTLEMENT_SOURCE_NOTE}",
                "offered_penalty": "Not mapped.",
            },
        )
        row.cells[response_idx].text = payload["response"]
        row.cells[penalty_idx].text = payload["offered_penalty"]

    doc.save(DOCX_PATH)
    print(f"Updated {DOCX_PATH}")


if __name__ == "__main__":
    main()
