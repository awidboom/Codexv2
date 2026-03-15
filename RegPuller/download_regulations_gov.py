import argparse
import os
import re
import sys
import urllib.parse
import urllib.request
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


API_BASE = "https://api.regulations.gov/v4"
USER_AGENT = "RegPuller/0.1 (+https://www.regulations.gov)"


def _headers(api_key: str) -> Dict[str, str]:
    headers = {"User-Agent": USER_AGENT}
    if api_key:
        headers["X-Api-Key"] = api_key
    return headers


def fetch_json(url: str, api_key: str) -> Dict[str, object]:
    req = urllib.request.Request(url, headers=_headers(api_key))
    with urllib.request.urlopen(req) as resp:
        return eval_json(resp.read())


def eval_json(data: bytes) -> Dict[str, object]:
    import json

    return json.loads(data.decode("utf-8", errors="ignore"))


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def sanitize_slug(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    return cleaned.strip("-") or "item"


def keyword_match(text: str, keywords: Sequence[str]) -> bool:
    if not text:
        return False
    hay = text.lower()
    return any(kw.lower() in hay for kw in keywords if kw.strip())


def search_documents(
    docket_id: str,
    keyword: str,
    api_key: str,
    page_size: int = 250,
    max_pages: int = 20,
) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    for page in range(1, max_pages + 1):
        params = [
            ("filter[docketId]", docket_id),
            ("filter[searchTerm]", keyword),
            ("page[size]", str(page_size)),
            ("page[number]", str(page)),
        ]
        url = f"{API_BASE}/documents?{urllib.parse.urlencode(params)}"
        data = fetch_json(url, api_key)
        data_items = data.get("data") or []
        if not isinstance(data_items, list) or not data_items:
            break
        results.extend(data_items)
    return results


def get_document_details(doc_id: str, api_key: str) -> Dict[str, object]:
    params = [("include", "attachments")]
    url = f"{API_BASE}/documents/{urllib.parse.quote(doc_id)}?{urllib.parse.urlencode(params)}"
    return fetch_json(url, api_key)


def iter_attachments(detail: Dict[str, object]) -> Iterable[Dict[str, object]]:
    included = detail.get("included") or []
    if not isinstance(included, list):
        return []
    return [item for item in included if item.get("type") == "attachments"]


def download_file(url: str, path: str) -> None:
    ensure_dir(os.path.dirname(path))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp, open(path, "wb") as f:
        f.write(resp.read())


def download_docket_attachments(
    docket_id: str,
    keywords: Sequence[str],
    out_dir: str,
    api_key: str,
    allowed_formats: Sequence[str] = ("pdf", "txt"),
) -> List[Dict[str, str]]:
    seen_doc_ids: Set[str] = set()
    documents: List[Dict[str, object]] = []
    for keyword in keywords:
        if not keyword.strip():
            continue
        for item in search_documents(docket_id, keyword, api_key):
            doc_id = item.get("id")
            if not doc_id or doc_id in seen_doc_ids:
                continue
            seen_doc_ids.add(doc_id)
            documents.append(item)

    downloaded: List[Dict[str, str]] = []
    for item in documents:
        doc_id = str(item.get("id"))
        detail = get_document_details(doc_id, api_key)
        data = detail.get("data") or {}
        attributes = data.get("attributes") or {}
        doc_title = str(attributes.get("title") or "")
        doc_matches = keyword_match(doc_title, keywords)
        for att in iter_attachments(detail):
            att_attrs = att.get("attributes") or {}
            att_title = str(att_attrs.get("title") or "")
            att_matches = keyword_match(att_title, keywords)
            if not (doc_matches or att_matches):
                continue
            for fmt in att_attrs.get("fileFormats") or []:
                file_url = fmt.get("fileUrl")
                file_format = str(fmt.get("format") or "").lower()
                if not file_url or file_format not in allowed_formats:
                    continue
                folder = os.path.join(out_dir, "regulations_gov", docket_id, doc_id)
                base = sanitize_slug(att_title or doc_title or doc_id)
                filename = f"{base}.{file_format}"
                path = os.path.join(folder, filename)
                download_file(file_url, path)
                downloaded.append(
                    {
                        "path": path,
                        "document_id": doc_id,
                        "document_title": doc_title,
                        "attachment_title": att_title,
                        "format": file_format,
                        "file_url": str(file_url),
                    }
                )
    return downloaded


def main() -> int:
    parser = argparse.ArgumentParser(description="Download Regulations.gov attachments by docket.")
    parser.add_argument("--docket", required=True, help="Docket ID")
    parser.add_argument(
        "--keywords",
        default="Technical Support Document, Response to Comments",
        help="Comma-separated keywords",
    )
    parser.add_argument("--out-dir", default="data", help="Output directory (default: data)")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("REGGOV_API_KEY", ""),
        help="Regulations.gov API key (X-Api-Key).",
    )
    parser.add_argument(
        "--formats",
        default="pdf,txt",
        help="Comma-separated formats to download (default: pdf,txt)",
    )
    args = parser.parse_args()

    if not args.api_key:
        print("Missing --api-key (or REGGOV_API_KEY).", file=sys.stderr)
        return 2
    keywords = [item.strip() for item in args.keywords.split(",") if item.strip()]
    formats = tuple(item.strip().lower() for item in args.formats.split(",") if item.strip())
    downloads = download_docket_attachments(
        args.docket,
        keywords,
        args.out_dir,
        args.api_key,
        allowed_formats=formats,
    )
    print(f"Downloaded {len(downloads)} file(s).")
    for item in downloads:
        print(f"- {item.get('path')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
