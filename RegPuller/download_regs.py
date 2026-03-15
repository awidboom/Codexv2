import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from typing import Dict, Iterable, List, Optional, Set, Tuple


USER_AGENT = "RegPuller/0.1 (+https://www.ecfr.gov)"
FR_HOST = "www.federalregister.gov"
ECFR_HOST = "www.ecfr.gov"
ECFR_API_BASE = "https://www.ecfr.gov/api/versioner/v1"
FR_API_BASE = "https://www.federalregister.gov/api/v1"


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: List[Tuple[str, str]] = []
        self._in_anchor = False
        self._href = ""
        self._text_parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        if tag.lower() != "a":
            return
        self._in_anchor = True
        self._href = ""
        self._text_parts = []
        for k, v in attrs:
            if k.lower() == "href":
                self._href = v or ""

    def handle_data(self, data: str) -> None:
        if self._in_anchor:
            self._text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a":
            return
        if self._in_anchor:
            text = " ".join(" ".join(self._text_parts).split())
            self.links.append((self._href, text))
        self._in_anchor = False
        self._href = ""
        self._text_parts = []


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: List[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        if tag.lower() in {"script", "style"}:
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"}:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip and data.strip():
            self.parts.append(data)


def fetch_url(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def parse_links(html: str) -> List[Tuple[str, str]]:
    parser = LinkExtractor()
    parser.feed(html)
    return parser.links


def html_to_text(html: str) -> str:
    parser = TextExtractor()
    parser.feed(html)
    return " ".join(parser.parts)


def to_absolute(base: str, href: str) -> str:
    return urllib.parse.urljoin(base, href)


def sanitize_slug(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    return cleaned.strip("-") or "item"


def slug_from_ecfr_url(url: str) -> Optional[str]:
    path = urllib.parse.urlparse(url).path.strip("/")
    parts = [p for p in path.split("/") if p]
    wanted = []
    for part in parts:
        lower = part.lower()
        if lower.startswith("title-") or lower.startswith("part-") or lower.startswith("subpart-"):
            wanted.append(part)
    if wanted:
        return "_".join(wanted)
    return None


def parse_ecfr_hierarchy(url: str) -> Dict[str, str]:
    path = urllib.parse.urlparse(url).path.strip("/")
    parts = [p for p in path.split("/") if p]
    hierarchy: Dict[str, str] = {}
    for part in parts:
        lower = part.lower()
        if lower.startswith("title-"):
            hierarchy["title"] = part.split("-", 1)[1]
        elif lower.startswith("chapter-"):
            hierarchy["chapter"] = part.split("-", 1)[1]
        elif lower.startswith("subchapter-"):
            hierarchy["subchapter"] = part.split("-", 1)[1]
        elif lower.startswith("part-"):
            hierarchy["part"] = part.split("-", 1)[1]
        elif lower.startswith("subpart-"):
            hierarchy["subpart"] = part.split("-", 1)[1]
    return hierarchy


def ensure_dir(path: str) -> None:
    if not path:
        return
    os.makedirs(path, exist_ok=True)


def write_bytes(path: str, data: bytes) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "wb") as f:
        f.write(data)


def infer_fr_action(content: bytes) -> str:
    text = content.decode("utf-8", errors="ignore")
    for line in text.splitlines():
        if line.strip().lower().startswith("action:"):
            action = line.split(":", 1)[1].strip()
            return action
    return ""


def fetch_json(url: str) -> Dict[str, object]:
    return json.loads(fetch_url(url).decode("utf-8", errors="ignore"))


def get_ecfr_title_date(title: str) -> Optional[str]:
    url = f"{ECFR_API_BASE}/titles.json"
    data = fetch_json(url)
    titles = data.get("titles", [])
    for item in titles:
        if str(item.get("number")) == str(title):
            return item.get("up_to_date_as_of")
    return None


def fetch_ecfr_xml_subset(date: str, title: str, hierarchy: Dict[str, str]) -> bytes:
    params = {}
    for key in ["subtitle", "chapter", "subchapter", "part", "subpart", "section", "appendix"]:
        if key in hierarchy:
            params[key] = hierarchy[key]
    query = urllib.parse.urlencode(params)
    url = f"{ECFR_API_BASE}/full/{date}/title-{title}.xml"
    if query:
        url = f"{url}?{query}"
    return fetch_url(url)


def ecfr_subpart_present(xml_bytes: bytes, subpart: str) -> bool:
    if not xml_bytes or not subpart:
        return False
    needle = f'TYPE="SUBPART"'
    subpart_attr = f'N="{subpart}"'
    text = xml_bytes.decode("utf-8", errors="ignore")
    return needle in text and subpart_attr in text


def find_dev_tools_link(html: str, base_url: str) -> Optional[str]:
    for href, text in parse_links(html):
        if not href:
            continue
        if "developer tools" in text.lower():
            return to_absolute(base_url, href)
    # Fallback: look for obvious API/data links.
    for href, _text in parse_links(html):
        if href and ("api" in href or "developer" in href):
            return to_absolute(base_url, href)
    return None


def pick_ecfr_download_link(html: str, base_url: str) -> Optional[Tuple[str, str]]:
    links = parse_links(html)
    candidates: Dict[str, str] = {}
    for href, text in links:
        if not href:
            continue
        lower = href.lower()
        if "xml" in lower:
            candidates["xml"] = to_absolute(base_url, href)
        elif "html" in lower:
            candidates["html"] = to_absolute(base_url, href)
        elif "json" in lower:
            candidates["json"] = to_absolute(base_url, href)
        if "xml" in text.lower():
            candidates.setdefault("xml", to_absolute(base_url, href))
        if "html" in text.lower():
            candidates.setdefault("html", to_absolute(base_url, href))
        if "json" in text.lower():
            candidates.setdefault("json", to_absolute(base_url, href))
    for key in ["xml", "html", "json"]:
        if key in candidates:
            return key, candidates[key]
    return None


def extract_rule_title(html: str) -> Optional[str]:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    if m:
        text = re.sub(r"<[^>]+>", " ", m.group(1))
        return " ".join(text.split())
    return None


def extract_rule_summary_candidates(
    html: str, rule_title: str, extra_candidates: Optional[List[str]] = None
) -> List[str]:
    candidates: List[str] = []
    if rule_title:
        candidates.append(rule_title)
    if extra_candidates:
        for candidate in extra_candidates:
            if candidate:
                candidates.append(candidate)
    text = html_to_text(html)
    for line in text.splitlines():
        cleaned = " ".join(line.split())
        if len(cleaned) < 20:
            continue
        lowered = cleaned.lower()
        if "national emission standards" in lowered or "federal standards" in lowered:
            candidates.append(cleaned)
            break
    deduped: List[str] = []
    seen: Set[str] = set()
    for item in candidates:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def extract_ecfr_headings(xml_text: str) -> List[str]:
    headings: List[str] = []
    for match in re.finditer(r"<HEAD[^>]*>(.*?)</HEAD>", xml_text, re.IGNORECASE | re.DOTALL):
        raw = match.group(1)
        cleaned = re.sub(r"<[^>]+>", " ", raw)
        cleaned = html.unescape(cleaned)
        cleaned = cleaned.replace("\u2014", " - ").replace("\u2013", " - ")
        cleaned = " ".join(cleaned.split())
        if cleaned:
            headings.append(cleaned)
    return headings


def pick_best_heading(headings: List[str]) -> str:
    if not headings:
        return ""
    for heading in headings:
        lowered = heading.lower()
        if "national emission standards" in lowered or "federal standards" in lowered:
            return heading
    return headings[0]


def pick_best_title_candidate(candidates: List[str], fallback: str) -> str:
    cleaned = [c for c in candidates if c and len(c.strip()) > 8]
    if cleaned:
        return max(cleaned, key=len)
    return fallback


STOPWORDS = {
    "the",
    "and",
    "for",
    "from",
    "of",
    "to",
    "in",
    "on",
    "at",
    "by",
    "with",
    "a",
    "an",
    "or",
    "as",
    "is",
    "are",
    "be",
    "this",
    "that",
    "these",
    "those",
    "its",
    "their",
    "into",
    "under",
    "near",
    "part",
    "subpart",
}


def normalize_match_text(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def normalize_search_text(text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = html.unescape(cleaned)
    return " ".join(cleaned.split())


def title_candidate_score(candidate: str, title: str) -> Tuple[float, int]:
    normalized_title = normalize_match_text(title)
    normalized_candidate = normalize_match_text(candidate)
    if not normalized_candidate:
        return 0.0, 0
    if normalized_candidate in normalized_title:
        tokens = [
            token
            for token in normalized_candidate.split()
            if token and token not in STOPWORDS and len(token) > 2
        ]
        return 1.0, len(tokens)
    title_terms = set(normalized_title.split())
    tokens = [
        token
        for token in normalized_candidate.split()
        if token and token not in STOPWORDS and len(token) > 2
    ]
    if not tokens:
        return 0.0, 0
    hits = [token for token in tokens if token in title_terms]
    return len(hits) / len(tokens), len(hits)


def summary_match_details(content: str, title_candidate: str) -> Dict[str, object]:
    if not content or not title_candidate:
        return {
            "matched": False,
            "matched_phrase": "",
            "keywords_hit": 0,
            "keywords_total": 0,
            "keywords_missing": 0,
        }
    normalized_content = normalize_match_text(content)
    content_terms = set(normalized_content.split())
    normalized_candidate = normalize_match_text(title_candidate)
    tokens = [
        token
        for token in normalized_candidate.split()
        if token and token not in STOPWORDS and len(token) > 2
    ]
    total = len(tokens)
    if normalized_candidate and normalized_candidate in normalized_content:
        return {
            "matched": True,
            "matched_phrase": title_candidate,
            "keywords_hit": total,
            "keywords_total": total,
            "keywords_missing": 0,
        }
    hits = [token for token in tokens if token in content_terms]
    missing = max(0, total - len(hits))
    matched_phrase = ""
    if total:
        matched_phrase = f"keywords: {', '.join(hits)} ({len(hits)}/{total})"
    return {
        "matched": total > 0 and missing <= 1,
        "matched_phrase": matched_phrase,
        "keywords_hit": len(hits),
        "keywords_total": total,
        "keywords_missing": missing,
    }


def extract_fr_links(html: str, base_url: str) -> Dict[str, str]:
    fr_links: Dict[str, str] = {}
    for href, text in parse_links(html):
        if not href:
            continue
        abs_url = to_absolute(base_url, href)
        if FR_HOST not in urllib.parse.urlparse(abs_url).netloc.lower():
            continue
        cite = extract_fr_citation(text)
        if cite:
            fr_links[cite] = abs_url
    return fr_links


def extract_fr_citation(text: str) -> Optional[str]:
    m = re.search(r"\b(\d+)\s+FR\s+(\d+)\b", text)
    if not m:
        return None
    return f"{m.group(1)} FR {m.group(2)}"


def is_fr_citation(text: str) -> bool:
    return bool(re.search(r"\b\d+\s+FR\s+\d+\b", text))


def parse_fr_citation_parts(citation: str) -> Optional[Tuple[int, int]]:
    m = re.search(r"\b(\d+)\s+FR\s+(\d+)\b", citation)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def fr_api_doc_matches_citation(doc: Dict[str, object], citation: str) -> bool:
    parts = parse_fr_citation_parts(citation)
    if not parts:
        return False
    volume, page = parts
    if int(doc.get("volume") or 0) != volume:
        return False
    start_page = int(doc.get("start_page") or 0)
    end_page = int(doc.get("end_page") or start_page or 0)
    if start_page and end_page and start_page <= page <= end_page:
        return True
    doc_citation = str(doc.get("citation") or "")
    if doc_citation:
        if citation in doc_citation:
            return True
        m = re.search(r"\b(\d+)\s+FR\s+(\d+)(?:-(\d+))?\b", doc_citation)
        if m and int(m.group(1)) == volume:
            try:
                start = int(m.group(2))
                end = int(m.group(3) or m.group(2))
            except ValueError:
                return False
            return start <= page <= end
    return False


DATE_REGEX = r"[A-Za-z]{3,9}\.?\s+\d{1,2},\s+\d{4}"


def extract_fr_citations_with_dates(text: str) -> List[Tuple[str, str]]:
    pattern = re.compile(rf"(?P<fr>\d+\s+FR\s+\d+)\s*,\s*(?P<date>{DATE_REGEX})")
    return [(m.group("fr"), m.group("date")) for m in pattern.finditer(text)]


def extract_fr_citations_from_ecfr_xml(xml_text: str) -> Tuple[List[str], Dict[str, str]]:
    cita_blocks = re.findall(r"<CITA[^>]*>(.*?)</CITA>", xml_text, re.IGNORECASE | re.DOTALL)
    citations: Dict[str, str] = {}
    for block in cita_blocks:
        text = re.sub(r"<[^>]+>", " ", block)
        for cite, date in extract_fr_citations_with_dates(text):
            citations.setdefault(cite, date)
        for m in re.finditer(r"\b(\d+\s+FR\s+\d+)\b", text):
            citations.setdefault(m.group(1), "")
    return sorted(citations.keys()), citations


def extract_fr_citations_from_ecfr_xml_with_provenance(
    xml_text: str,
) -> Tuple[List[str], Dict[str, str], List[Dict[str, str]]]:
    citations: Dict[str, str] = {}
    provenance: List[Dict[str, str]] = []
    for match in re.finditer(r"<CITA[^>]*>(.*?)</CITA>", xml_text, re.IGNORECASE | re.DOTALL):
        block = match.group(1)
        text = re.sub(r"<[^>]+>", " ", block)
        line = xml_text[: match.start()].count("\n") + 1
        cites = set()
        for cite, date in extract_fr_citations_with_dates(text):
            citations.setdefault(cite, date)
            cites.add(cite)
        for m in re.finditer(r"\b(\d+\s+FR\s+\d+)\b", text):
            citations.setdefault(m.group(1), "")
            cites.add(m.group(1))
        if cites:
            provenance.append(
                {
                    "source": "ecfr_xml_cita",
                    "line": str(line),
                    "citations": ", ".join(sorted(cites)),
                    "text": " ".join(text.split())[:300],
                }
            )
    return sorted(citations.keys()), citations, provenance


MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def parse_date_string(value: str) -> Optional[datetime]:
    cleaned = value.strip().replace(".", "")
    parts = cleaned.split()
    if len(parts) != 3:
        return None
    month = MONTHS.get(parts[0].lower())
    if not month:
        return None
    try:
        day = int(parts[1].rstrip(","))
        year = int(parts[2])
    except ValueError:
        return None
    return datetime(year, month, day)


def to_iso_date(value: str) -> str:
    if not value:
        return ""
    dt = parse_date_string(value)
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d")


def normalize_docket_id(value: str) -> str:
    cleaned = re.sub(r"[^\w-]", "", value.strip().upper())
    parts = [p for p in cleaned.split("-") if p]
    if len(parts) >= 6 and parts[-1].isdigit() and parts[-2].isdigit():
        if len(parts[-1]) in (3, 4) and len(parts[-2]) == 4:
            parts = parts[:-1]
    return "-".join(parts)


def extract_docket_ids(text: str) -> List[str]:
    pattern = re.compile(
        r"\bDocket\s+(?:ID\s+)?(?:No\.|Nos\.|Number)?\s*(?P<id>[A-Z0-9]+(?:-[A-Z0-9]+){1,6})",
        re.IGNORECASE,
    )
    ids: Set[str] = set()
    for match in pattern.finditer(text):
        raw = match.group("id")
        docket_id = normalize_docket_id(raw)
        if docket_id and re.search(r"\d", docket_id):
            ids.add(docket_id)
    return sorted(ids)




def fr_api_search_by_citation(citation: str, publication_date: str = "") -> Optional[Dict[str, object]]:
    fields = [
        "citation",
        "document_number",
        "full_text_xml_url",
        "raw_text_url",
        "html_url",
        "publication_date",
        "type",
        "title",
        "pdf_url",
        "volume",
        "start_page",
        "end_page",
    ]
    parts = parse_fr_citation_parts(citation)
    if publication_date and parts:
        params: List[Tuple[str, str]] = [
            ("conditions[publication_date][is]", publication_date),
            ("per_page", "1000"),
        ]
        params += [("fields[]", field) for field in fields]
        max_pages = 10
        for api_page in range(1, max_pages + 1):
            params_page = params + [("page", str(api_page))]
            url = f"{FR_API_BASE}/documents.json?{urllib.parse.urlencode(params_page)}"
            data = fetch_json(url)
            results = data.get("results") or []
            if not isinstance(results, list) or not results:
                break
            for result in results:
                if fr_api_doc_matches_citation(result, citation):
                    return result
            total_pages = int(data.get("total_pages") or 0)
            if total_pages and api_page >= total_pages:
                break
    volume = page = None
    if parts:
        volume, page = parts
    params = [("conditions[term]", citation), ("per_page", "100")]
    params += [("fields[]", field) for field in fields]
    url = f"{FR_API_BASE}/documents.json?{urllib.parse.urlencode(params)}"
    data = fetch_json(url)
    results = data.get("results") or []
    if not isinstance(results, list):
        return None
    for result in results:
        if fr_api_doc_matches_citation(result, citation):
            return result
    if volume is not None and page is not None:
        params = [
            ("conditions[volume]", str(volume)),
            ("conditions[page]", str(page)),
            ("per_page", "1000"),
        ]
        params += [("fields[]", field) for field in fields]
        url = f"{FR_API_BASE}/documents.json?{urllib.parse.urlencode(params)}"
        try:
            data = fetch_json(url)
        except Exception:
            return None
        results = data.get("results") or []
        if isinstance(results, list):
            for result in results:
                if fr_api_doc_matches_citation(result, citation):
                    return result
        params = [
            ("conditions[volume]", str(volume)),
            ("per_page", "1000"),
        ]
        params += [("fields[]", field) for field in fields]
        max_pages = 50
        for api_page in range(1, max_pages + 1):
            params_page = params + [("page", str(api_page))]
            url = f"{FR_API_BASE}/documents.json?{urllib.parse.urlencode(params_page)}"
            try:
                data = fetch_json(url)
            except Exception:
                break
            results = data.get("results") or []
            if not isinstance(results, list) or not results:
                break
            for result in results:
                if fr_api_doc_matches_citation(result, citation):
                    return result
            total_pages = int(data.get("total_pages") or 0)
            if total_pages and api_page >= total_pages:
                break
    return None


def fr_api_search_by_title_and_date(title: str, publication_date: str) -> Optional[Dict[str, object]]:
    if not title or not publication_date:
        return None
    fields = [
        "citation",
        "document_number",
        "full_text_xml_url",
        "raw_text_url",
        "html_url",
        "publication_date",
        "type",
        "title",
        "pdf_url",
    ]
    params: List[Tuple[str, str]] = [
        ("conditions[term]", title),
        ("conditions[publication_date][is]", publication_date),
        ("per_page", "100"),
    ]
    params += [("fields[]", field) for field in fields]
    url = f"{FR_API_BASE}/documents.json?{urllib.parse.urlencode(params)}"
    data = fetch_json(url)
    results = data.get("results") or []
    if not isinstance(results, list):
        return None
    return results[0] if results else None


def fr_api_search_by_title_date_section(
    title_candidates: List[str],
    publication_date: str,
    sections: Optional[List[str]] = None,
    citation: str = "",
    strict_citation: bool = True,
) -> Optional[Dict[str, object]]:
    if not title_candidates or not publication_date:
        return None
    fields = [
        "citation",
        "document_number",
        "full_text_xml_url",
        "raw_text_url",
        "html_url",
        "publication_date",
        "type",
        "title",
        "pdf_url",
        "volume",
        "start_page",
        "end_page",
    ]
    candidates = [
        candidate
        for candidate in sorted(title_candidates, key=len, reverse=True)
        if candidate and len(candidate.strip()) > 8
    ]
    if not candidates:
        return None
    params: List[Tuple[str, str]] = [
        ("conditions[publication_date][is]", publication_date),
        ("per_page", "1000"),
    ]
    if sections:
        for section in sections:
            params.append(("conditions[sections][]", section))
    params += [("fields[]", field) for field in fields]
    max_pages = 10
    best_doc = None
    best_score = 0.0
    best_hits = 0
    for api_page in range(1, max_pages + 1):
        params_page = params + [("page", str(api_page))]
        url = f"{FR_API_BASE}/documents.json?{urllib.parse.urlencode(params_page)}"
        data = fetch_json(url)
        results = data.get("results") or []
        if not isinstance(results, list) or not results:
            break
        for result in results:
            title = str(result.get("title") or "")
            if citation and strict_citation and not fr_api_doc_matches_citation(result, citation):
                continue
            for candidate in candidates:
                score, hits = title_candidate_score(candidate, title)
                if score > best_score and (hits >= 3 or score >= 0.7):
                    best_score = score
                    best_hits = hits
                    best_doc = result
        total_pages = int(data.get("total_pages") or 0)
        if total_pages and api_page >= total_pages:
            break
    return best_doc


def fr_citation_slug(cite: str, url: str = "") -> str:
    if cite:
        return sanitize_slug(cite.replace(" FR ", "-fr-"))
    if url:
        path = urllib.parse.urlparse(url).path.strip("/")
        return sanitize_slug(path.split("/")[-1])
    return "fr-document"


def download_fr_doc_from_api_doc(
    doc: Dict[str, object],
    citation: str,
    role: str,
    out_dir: str,
) -> Optional[Dict[str, str]]:
    xml_url = doc.get("full_text_xml_url")
    text_url = doc.get("raw_text_url")
    html_url = doc.get("html_url")
    content_url = xml_url or text_url or html_url
    if not content_url:
        return None
    ext = "xml" if xml_url else "txt" if text_url else "html"
    content = fetch_url(str(content_url))
    action = infer_fr_action(content)
    action_slug = sanitize_slug(action) if action else ""
    folder = os.path.join(out_dir, "fr", fr_citation_slug(citation, str(content_url)))
    ensure_dir(folder)
    filename = f"{action_slug or role}-rule.{ext}" if action_slug else f"{role}-rule.{ext}"
    path = os.path.join(folder, filename)
    write_bytes(path, content)
    return {
        "path": path,
        "ext": ext,
        "citation": citation,
        "api_citation": str(doc.get("citation") or ""),
        "url": str(content_url),
        "role": role,
        "action": action,
        "document_number": str(doc.get("document_number") or ""),
        "publication_date": str(doc.get("publication_date") or ""),
        "title": str(doc.get("title") or ""),
        "type": str(doc.get("type") or ""),
        "volume": str(doc.get("volume") or ""),
        "start_page": str(doc.get("start_page") or ""),
        "end_page": str(doc.get("end_page") or ""),
        "full_text_xml_url": str(doc.get("full_text_xml_url") or ""),
        "raw_text_url": str(doc.get("raw_text_url") or ""),
        "pdf_url": str(doc.get("pdf_url") or ""),
        "html_url": str(doc.get("html_url") or ""),
    }


def download_fr_doc_by_citation(
    citation: str,
    role: str,
    out_dir: str,
    publication_date: str = "",
) -> Optional[Dict[str, str]]:
    doc = fr_api_search_by_citation(citation, publication_date)
    if not doc:
        return None
    return download_fr_doc_from_api_doc(doc, citation, role, out_dir)


def extract_proposed_fr_citations(text: str) -> List[str]:
    keywords = ["propos", "notice of proposed rulemaking", "nprm"]
    citations = []
    clean_text = normalize_search_text(text)
    for m in re.finditer(r"\b(\d+\s+FR\s+\d+)\b", clean_text):
        start = max(0, m.start() - 400)
        end = min(len(clean_text), m.end() + 400)
        window = clean_text[start:end].lower()
        if any(k in window for k in keywords):
            citations.append(m.group(1))
    return sorted(set(citations))


def extract_proposed_fr_citations_with_dates(text: str) -> Dict[str, str]:
    keywords = ["propos", "notice of proposed rulemaking", "nprm"]
    citations: Dict[str, str] = {}
    date_pattern = re.compile(DATE_REGEX)
    clean_text = normalize_search_text(text)
    for m in re.finditer(r"\b(\d+\s+FR\s+\d+)\b", clean_text):
        start = max(0, m.start() - 400)
        end = min(len(clean_text), m.end() + 400)
        window = clean_text[start:end].lower()
        if not any(k in window for k in keywords):
            continue
        citation = m.group(1)
        near_start = max(0, m.start() - 400)
        near_end = min(len(clean_text), m.end() + 400)
        near_text = clean_text[near_start:near_end]
        best_date = ""
        best_dist: Optional[int] = None
        for dmatch in date_pattern.finditer(near_text):
            date_str = dmatch.group(0)
            abs_start = near_start + dmatch.start()
            dist = abs(abs_start - m.start())
            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_date = date_str
        citations.setdefault(citation, best_date)
    return citations


def extract_proposed_dates(text: str) -> List[str]:
    patterns = [
        r"propos\w*\s+(?:on\s+)?(?P<date>[A-Za-z]{3,9}\.?\s+\d{1,2},\s+\d{4})",
        r"notice of proposed rulemaking.*?(?P<date>[A-Za-z]{3,9}\.?\s+\d{1,2},\s+\d{4})",
        r"nprm.*?(?P<date>[A-Za-z]{3,9}\.?\s+\d{1,2},\s+\d{4})",
    ]
    dates: List[str] = []
    text = normalize_search_text(text)
    for pattern in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
            dates.append(m.group("date"))
    return dates


def download_rule(rule_url: str, out_dir: str) -> Tuple[str, str, str, str]:
    html = fetch_url(rule_url).decode("utf-8", errors="ignore")
    title = extract_rule_title(html) or "ecfr-rule"
    slug = slug_from_ecfr_url(rule_url) or sanitize_slug(title)
    rule_dir = os.path.join(out_dir, "ecfr", slug)
    ensure_dir(rule_dir)

    rule_ext = "xml"
    rule_content = b""
    hierarchy = parse_ecfr_hierarchy(rule_url)
    api_date = None
    if hierarchy.get("title"):
        api_date = get_ecfr_title_date(hierarchy["title"])
    if api_date and hierarchy.get("title"):
        try:
            rule_content = fetch_ecfr_xml_subset(api_date, hierarchy["title"], hierarchy)
            if hierarchy.get("subpart") and not ecfr_subpart_present(rule_content, hierarchy["subpart"]):
                rule_content = b""
        except Exception:
            rule_content = b""
    if not rule_content:
        dev_link = find_dev_tools_link(html, rule_url)
        rule_ext = "html"
        rule_content = html.encode("utf-8")
        if dev_link:
            dev_html = fetch_url(dev_link).decode("utf-8", errors="ignore")
            picked = pick_ecfr_download_link(dev_html, dev_link)
            if picked:
                rule_ext, link = picked
                rule_content = fetch_url(link)
    rule_path = os.path.join(rule_dir, f"rule.{rule_ext}")
    write_bytes(rule_path, rule_content)
    return html, title, rule_dir, rule_path


def collect_final_fr_docs(
    rule_html: str, rule_url: str
) -> Tuple[Dict[str, str], Dict[str, str]]:
    fr_links = extract_fr_links(rule_html, rule_url)
    text = html_to_text(rule_html)
    fr_dates: Dict[str, str] = {}
    for cite, _date in extract_fr_citations_with_dates(text):
        fr_dates.setdefault(cite, _date)
        fr_links.setdefault(cite, "")
    return fr_links, fr_dates


def load_manifest(path: str) -> Dict[str, object]:
    if not os.path.exists(path):
        return {"created_local": datetime.now().isoformat(timespec="seconds"), "entries": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"created_local": datetime.now().isoformat(timespec="seconds"), "entries": []}


def write_manifest(path: str, manifest: Dict[str, object]) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)


def write_fr_provenance_markdown(path: str, entry: Dict[str, object]) -> None:
    target_path = path
    lines: List[str] = []
    lines.append("# FR Citation Provenance")
    lines.append("")
    lines.append(f"- Rule URL: {entry.get('rule_url')}")
    lines.append(f"- Rule title: {entry.get('rule_title')}")
    lines.append(f"- Rule file: {entry.get('rule_file')}")
    lines.append("")
    downloaded_paths: Dict[str, str] = {}
    for item in entry.get("final_rules") or []:
        cite = item.get("citation")
        downloaded_path = item.get("path")
        if cite and downloaded_path:
            downloaded_paths[str(cite)] = str(downloaded_path)
    for item in entry.get("proposed_rules") or []:
        cite = item.get("citation")
        downloaded_path = item.get("path")
        if cite and downloaded_path:
            downloaded_paths[str(cite)] = str(downloaded_path)
    prov = entry.get("fr_provenance") or []
    if not isinstance(prov, list):
        prov = []
    status = entry.get("fr_download_status") or []
    if not isinstance(status, list):
        status = []
    if not prov:
        lines.append("No FR provenance recorded.")
        lines.append("")
    else:
        ecfr = [p for p in prov if p.get("source") == "ecfr_xml_cita"]
        if ecfr:
            lines.append("## From eCFR XML <CITA> blocks")
            for item in ecfr:
                lines.append(f"- Line {item.get('line')}: {item.get('citations')}")
                lines.append(f"  - Context: {item.get('text')}")
            lines.append("")
        fr_text = [p for p in prov if p.get("source") == "fr_text_proposed"]
        if fr_text:
            lines.append("## From FR text (proposed citations)")
            for item in fr_text:
                cited = str(item.get("citations") or "")
                dest = downloaded_paths.get(cited, "")
                suffix = f" | downloaded to {dest}" if dest else ""
                lines.append(
                    f"- Found in {item.get('from_citation')} at {item.get('from_path')}: {cited}{suffix}"
                )
            lines.append("")
        fr_text_dates = [p for p in prov if p.get("source") == "fr_text_proposed_date"]
        if fr_text_dates:
            lines.append("## From FR text (proposed citations with dates)")
            for item in fr_text_dates:
                cited = str(item.get("citations") or "")
                date_str = str(item.get("date") or "")
                dest = downloaded_paths.get(cited, "")
                suffix = f" | downloaded to {dest}" if dest else ""
                if date_str:
                    lines.append(
                        f"- Found in {item.get('from_citation')} at {item.get('from_path')}: {cited} ({date_str}){suffix}"
                    )
                else:
                    lines.append(
                        f"- Found in {item.get('from_citation')} at {item.get('from_path')}: {cited}{suffix}"
                    )
            lines.append("")
        title_date = [p for p in prov if p.get("source") == "fr_title_date_search"]
        if title_date:
            lines.append("## From proposed-rule date + title search")
            for item in title_date:
                cited = str(item.get("citations") or "")
                dest = downloaded_paths.get(cited, "")
                suffix = f" | downloaded to {dest}" if dest else ""
                lines.append(
                    f"- {item.get('date')} | {item.get('title')} -> {cited}{suffix}"
                )
            lines.append("")
    if status:
        lines.append("## Download status")
        for item in status:
            cite = item.get("citation")
            kind = item.get("kind")
            state = item.get("status")
            reason = item.get("reason") or ""
            lines.append(f"- {cite} ({kind}): {state} {reason}".rstrip())
        lines.append("")
    summary_checks = entry.get("fr_summary_checks") or []
    if isinstance(summary_checks, list) and summary_checks:
        lines.append("## Summary match check")
        for item in summary_checks:
            cite = item.get("citation")
            role = item.get("role")
            matched = item.get("matched")
            phrase = item.get("matched_phrase") or ""
            missing = item.get("keywords_missing")
            total = item.get("keywords_total")
            filtered = item.get("filtered")
            status_text = "matched" if matched else "missing"
            if filtered:
                status_text = "filtered"
            count_suffix = ""
            if isinstance(missing, int) and isinstance(total, int) and total:
                count_suffix = f" ({missing}/{total} missing)"
            suffix = f" | {phrase}" if phrase else ""
            lines.append(f"- {cite} ({role}): {status_text}{count_suffix}{suffix}")
        lines.append("")
    ensure_dir(os.path.dirname(target_path))
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).strip() + "\n")


def run_download(rule_url: str, out_dir: str, rule_title_override: str = "") -> Dict[str, object]:
    if isinstance(out_dir, str):
        out_dir = out_dir.strip()
    if not out_dir:
        out_dir = "data"
    entry: Dict[str, object] = {
        "rule_url": rule_url,
        "rule_title": "",
        "rule_dir": "",
        "rule_file": "",
        "out_dir": out_dir,
        "rule_summary_candidates": [],
        "final_rules": [],
        "proposed_rules": [],
        "docket_ids": [],
        "docket_sources": [],
        "fr_provenance": [],
        "fr_summary_checks": [],
        "fr_download_status": [],
        "errors": [],
        "created_local": datetime.now().isoformat(timespec="seconds"),
    }
    try:
        rule_html, rule_title, rule_dir, rule_path = download_rule(rule_url, out_dir)
    except Exception as exc:
        entry["errors"].append(f"Failed to download rule: {exc}")
        return entry
    if rule_title_override:
        rule_title = rule_title_override
    xml_heading = ""
    fr_links, fr_dates = collect_final_fr_docs(rule_html, rule_url)
    if rule_path.lower().endswith(".xml"):
        try:
            with open(rule_path, "r", encoding="utf-8", errors="ignore") as f:
                xml_text = f.read()
            xml_cites, xml_dates, xml_prov = extract_fr_citations_from_ecfr_xml_with_provenance(
                xml_text
            )
            for cite in xml_cites:
                fr_links.setdefault(cite, "")
            for cite, date_str in xml_dates.items():
                if date_str:
                    fr_dates.setdefault(cite, date_str)
            entry["fr_provenance"].extend(xml_prov)
            xml_heading = pick_best_heading(extract_ecfr_headings(xml_text))
        except OSError:
            pass
    if xml_heading and (not rule_title or rule_title.lower() == "request access"):
        rule_title = xml_heading
    entry["rule_title"] = rule_title
    entry["rule_dir"] = rule_dir
    entry["rule_file"] = rule_path
    summary_extras = [xml_heading] if xml_heading else []
    entry["rule_summary_candidates"] = extract_rule_summary_candidates(
        rule_html, rule_title, summary_extras
    )
    best_title_candidate = pick_best_title_candidate(
        entry["rule_summary_candidates"], rule_title
    )

    downloaded_final: List[Dict[str, str]] = []
    downloaded_final_cites: Set[str] = set()
    for cite, url in fr_links.items():
        if not is_fr_citation(cite):
            continue
        iso_date = to_iso_date(fr_dates.get(cite, ""))
        info = download_fr_doc_by_citation(cite, "final", out_dir, iso_date)
        if info:
            downloaded_final.append(info)
            downloaded_final_cites.add(cite)
            entry["fr_download_status"].append(
                {"citation": cite, "kind": "final", "status": "downloaded"}
            )
        else:
            reason = "no API match"
            if iso_date:
                reason = f"no API match (date={iso_date})"
            entry["fr_download_status"].append(
                {"citation": cite, "kind": "final", "status": "missing", "reason": reason}
            )

    entry["final_rules"] = downloaded_final

    docket_ids: Set[str] = set()
    docket_sources: Dict[str, Set[str]] = {}
    for info in downloaded_final:
        path = info.get("path", "")
        if not path:
            continue
        try:
            with open(path, "rb") as f:
                content = f.read().decode("utf-8", errors="ignore")
        except OSError:
            continue
        for docket_id in extract_docket_ids(content):
            docket_ids.add(docket_id)
            docket_sources.setdefault(docket_id, set()).add(str(info.get("citation") or ""))
        proposed_cites = extract_proposed_fr_citations(content)
        proposed_cites_with_dates = extract_proposed_fr_citations_with_dates(content)
        proposed_dates = extract_proposed_dates(content)
        for cite in proposed_cites:
            if cite in fr_links and fr_links[cite]:
                continue
            fr_links.setdefault(cite, "")
            entry["fr_provenance"].append(
                {
                    "source": "fr_text_proposed",
                    "from_citation": str(info.get("citation") or ""),
                    "from_path": str(path),
                    "citations": cite,
                }
            )
        for cite, date_str in proposed_cites_with_dates.items():
            fr_links.setdefault(cite, "")
            if date_str:
                fr_dates.setdefault(cite, date_str)
            entry["fr_provenance"].append(
                {
                    "source": "fr_text_proposed_date",
                    "from_citation": str(info.get("citation") or ""),
                    "from_path": str(path),
                    "citations": cite,
                    "date": date_str,
                    }
                )
        for date_str in proposed_dates:
            iso_date = to_iso_date(date_str)
            if not iso_date:
                continue
            doc = fr_api_search_by_title_and_date(best_title_candidate, iso_date)
            if not doc:
                continue
            citation = doc.get("citation") or ""
            if citation:
                fr_links.setdefault(str(citation), "")
                fr_dates.setdefault(str(citation), date_str)
                entry["fr_provenance"].append(
                    {
                        "source": "fr_title_date_search",
                        "date": iso_date,
                        "title": rule_title,
                        "citations": str(citation),
                    }
                )

    if docket_ids:
        entry["docket_ids"] = sorted(docket_ids)
    if docket_sources:
        entry["docket_sources"] = [
            {"docket_id": docket_id, "citations": sorted(cites)}
            for docket_id, cites in sorted(docket_sources.items())
        ]

    downloaded_proposed: List[Dict[str, str]] = []
    downloaded_proposed_cites: Set[str] = set()
    for cite, url in fr_links.items():
        if cite in downloaded_final_cites or cite in downloaded_proposed_cites:
            continue
        if not is_fr_citation(cite):
            continue
        iso_date = to_iso_date(fr_dates.get(cite, ""))
        info = download_fr_doc_by_citation(cite, "proposed", out_dir, iso_date)
        if not info and iso_date and entry.get("rule_summary_candidates"):
            doc = fr_api_search_by_title_date_section(
                entry.get("rule_summary_candidates") or [],
                iso_date,
                ["environment"],
                cite,
            )
            if not doc:
                doc = fr_api_search_by_title_date_section(
                    entry.get("rule_summary_candidates") or [],
                    iso_date,
                    ["environment"],
                    cite,
                    strict_citation=False,
                )
            if doc:
                info = download_fr_doc_from_api_doc(doc, cite, "proposed", out_dir)
                if info is not None:
                    info["lookup_method"] = "title_date_section"
                    if not fr_api_doc_matches_citation(doc, cite):
                        info["lookup_method"] = "title_date_section_unverified"
        if info:
            downloaded_proposed.append(info)
            downloaded_proposed_cites.add(cite)
            reason = info.get("lookup_method") if isinstance(info, dict) else ""
            entry["fr_download_status"].append(
                {
                    "citation": cite,
                    "kind": "proposed",
                    "status": "downloaded",
                    "reason": reason or "",
                }
            )
        else:
            reason = "no API match"
            if iso_date:
                reason = f"no API match (date={iso_date})"
            entry["fr_download_status"].append(
                {"citation": cite, "kind": "proposed", "status": "missing", "reason": reason}
            )
    entry["proposed_rules"] = downloaded_proposed
    summary_candidates = entry.get("rule_summary_candidates") or []
    if isinstance(summary_candidates, list) and summary_candidates:
        best_title_candidate = pick_best_title_candidate(summary_candidates, entry["rule_title"])
        filtered_final: List[Dict[str, str]] = []
        filtered_proposed: List[Dict[str, str]] = []
        for doc in downloaded_final + downloaded_proposed:
            path = doc.get("path", "")
            if not path:
                continue
            try:
                with open(path, "rb") as f:
                    content = f.read().decode("utf-8", errors="ignore")
            except OSError:
                entry["fr_summary_checks"].append(
                    {
                        "citation": str(doc.get("citation") or ""),
                        "role": str(doc.get("role") or ""),
                        "path": path,
                        "matched": False,
                        "matched_phrase": "unreadable",
                        "keywords_hit": 0,
                        "keywords_total": 0,
                        "keywords_missing": 0,
                        "filtered": False,
                    }
                )
                continue
            details = summary_match_details(content, best_title_candidate)
            missing = int(details.get("keywords_missing") or 0)
            total = int(details.get("keywords_total") or 0)
            filtered = total > 0 and missing > 1
            entry["fr_summary_checks"].append(
                {
                    "citation": str(doc.get("citation") or ""),
                    "role": str(doc.get("role") or ""),
                    "path": path,
                    "matched": bool(details.get("matched")),
                    "matched_phrase": str(details.get("matched_phrase") or ""),
                    "keywords_hit": int(details.get("keywords_hit") or 0),
                    "keywords_total": total,
                    "keywords_missing": missing,
                    "filtered": filtered,
                }
            )
            if filtered:
                try:
                    os.remove(path)
                except OSError:
                    entry["errors"].append(f"Failed to remove filtered file: {path}")
                reason = f"summary mismatch ({missing}/{total} missing)"
                for status in entry.get("fr_download_status") or []:
                    if status.get("citation") == doc.get("citation") and status.get("kind") == doc.get("role"):
                        status["status"] = "filtered"
                        status["reason"] = reason
                        break
            else:
                if doc.get("role") == "final":
                    filtered_final.append(doc)
                else:
                    filtered_proposed.append(doc)
        entry["final_rules"] = filtered_final
        entry["proposed_rules"] = filtered_proposed
    out_root = os.path.abspath(out_dir or "data")
    ensure_dir(out_root)
    provenance_paths = [
        os.path.join(out_root, "fr_provenance.md"),
        os.path.join(entry.get("rule_dir") or out_root, "fr_provenance.md"),
        os.path.join(os.getcwd(), "fr_provenance.md"),
    ]
    wrote = False
    for provenance_path in provenance_paths:
        try:
            write_fr_provenance_markdown(provenance_path, entry)
            entry["fr_provenance_path"] = provenance_path
            wrote = True
        except Exception as exc:
            entry["errors"].append(f"Failed to write fr_provenance.md: {exc}")
    if not wrote:
        entry["errors"].append("Failed to write fr_provenance.md to any output location.")
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download eCFR rule text and related Federal Register documents."
    )
    parser.add_argument("rule_url", nargs="?", default="", help="eCFR rule URL")
    parser.add_argument("--out-dir", default="data", help="Output directory (default: data)")
    parser.add_argument("--rule-title", default="", help="Optional override for rule title")
    parser.add_argument(
        "--config",
        default="",
        help="Optional JSON config file with rules to download",
    )
    parser.add_argument(
        "--manifest",
        default="",
        help="Optional manifest file path (default: <out-dir>/manifest.json)",
    )
    args = parser.parse_args()

    entries: List[Dict[str, object]] = []
    if args.config:
        try:
            with open(args.config, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Failed to read config: {exc}", file=sys.stderr)
            return 2
        rules = cfg.get("rules", [])
        if not isinstance(rules, list):
            print("Config file must include a 'rules' array.", file=sys.stderr)
            return 2
        for rule in rules:
            if not isinstance(rule, dict) or not rule.get("url"):
                continue
            out_dir = rule.get("out_dir", args.out_dir)
            title = rule.get("title", "")
            entries.append(run_download(rule["url"], out_dir, title))
    else:
        if not args.rule_url:
            print("rule_url is required when --config is not provided.", file=sys.stderr)
            return 2
        entries.append(run_download(args.rule_url, args.out_dir, args.rule_title))

    manifest_path = args.manifest or os.path.join(args.out_dir, "manifest.json")
    manifest = load_manifest(manifest_path)
    manifest_entries = manifest.get("entries", [])
    if not isinstance(manifest_entries, list):
        manifest_entries = []
    manifest_entries.extend(entries)
    manifest["entries"] = manifest_entries
    write_manifest(manifest_path, manifest)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
