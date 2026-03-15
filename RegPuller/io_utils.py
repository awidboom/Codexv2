import io
import os

from pypdf import PdfReader, PdfWriter
import docx

try:
    import pytesseract
    from pdf2image import convert_from_path
except Exception:
    pytesseract = None
    convert_from_path = None


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    out = []
    for _, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            out.append(text)
    return "\n".join(out)


def read_docx(path: str) -> str:
    d = docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs if p.text.strip())


def ocr_output_path(path: str) -> str:
    root, ext = os.path.splitext(path)
    return f"{root}_OCR{ext}"


def is_ocr_pdf(path: str) -> bool:
    return path.lower().endswith("_ocr.pdf")


def pdf_needs_ocr(path: str, min_chars: int = 40, min_text_ratio: float = 0.3) -> bool:
    try:
        reader = PdfReader(path)
        total = len(reader.pages)
        if total == 0:
            return False
        with_text = 0
        for page in reader.pages:
            text = (page.extract_text() or "").strip()
            if len(text) >= min_chars:
                with_text += 1
        return (with_text / total) < min_text_ratio
    except Exception:
        return False


def ocr_pdf_to_searchable(path: str, output_path: str, dpi: int = 300) -> bool:
    if pytesseract is None or convert_from_path is None:
        return False
    try:
        images = convert_from_path(path, dpi=dpi)
        writer = PdfWriter()
        for img in images:
            pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf")
            page_reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in page_reader.pages:
                writer.add_page(page)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            writer.write(f)
        return True
    except Exception:
        return False
