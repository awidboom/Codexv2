import argparse
from pathlib import Path


def convert_doc_to_docx(in_path: Path, out_path: Path) -> Path:
    try:
        import win32com.client  # type: ignore
    except Exception as e:
        raise RuntimeError("pywin32 is required (pip install pywin32)") from e

    wdFormatXMLDocument = 12

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(in_path.resolve()), ReadOnly=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.SaveAs2(str(out_path.resolve()), FileFormat=wdFormatXMLDocument)
    doc.Close(False)
    word.Quit()
    return out_path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Convert legacy .doc to .docx using Microsoft Word (COM).")
    ap.add_argument("--in", dest="in_path", required=True, help="Input .doc path")
    ap.add_argument("--out", dest="out_path", required=True, help="Output .docx path")
    args = ap.parse_args(argv)

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    convert_doc_to_docx(in_path, out_path)
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

