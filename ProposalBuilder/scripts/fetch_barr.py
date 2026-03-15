import os
import re
import time
import hashlib
import argparse
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urlunparse, urldefrag
from urllib.request import Request, urlopen


START_URLS = [
    "https://www.barr.com/projects",
    "https://www.barr.com/sector",
    "https://www.barr.com/service",
    "https://www.barr.com/insights",
]

ALLOWED_HOSTS = {"www.barr.com", "barr.com"}
ALLOWED_PREFIXES = ["/projects", "/project", "/sector", "/service", "/insights"]
FIRST_LEVEL_ONLY = {"/sector", "/service"}
SITEMAP_URLS = [
    "https://www.barr.com/sitemap.xml",
    "https://www.barr.com/sitemap-index.xml",
]

BLOCK_TAGS = {
    "p",
    "br",
    "li",
    "div",
    "section",
    "article",
    "header",
    "footer",
    "nav",
    "aside",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
}


class LinkTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.text_parts = []
        self._skip_depth = 0
        self._in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "nav", "footer", "header", "aside"):
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.links.append(v)
        if tag in BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "nav", "footer", "header", "aside"):
            if self._skip_depth > 0:
                self._skip_depth -= 1
        if tag == "title":
            self._in_title = False
        if tag in BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_data(self, data):
        if self._in_title and data:
            self.title += data.strip() + " "
        if self._skip_depth == 0 and data:
            self.text_parts.append(data)


def normalize_url(url: str) -> str:
    url, _ = urldefrag(url)
    if not url:
        return ""
    p = urlparse(url.strip())
    p = p._replace(query="")
    return urlunparse(p)


def is_allowed(url: str) -> bool:
    p = urlparse(url)
    if p.scheme not in ("http", "https"):
        return False
    if p.netloc not in ALLOWED_HOSTS:
        return False
    if not any(p.path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        return False
    for prefix in FIRST_LEVEL_ONLY:
        if p.path.startswith(prefix):
            suffix = p.path[len(prefix):].strip("/")
            if not suffix:
                return True
            return len(suffix.split("/")) <= 1
    return True


def textify(html: str) -> str:
    parser = LinkTextParser()
    parser.feed(html)
    raw = "".join(parser.text_parts)
    lines = [re.sub(r"\s+", " ", line).strip() for line in raw.split("\n")]
    lines = [ln for ln in lines if ln]
    text = "\n".join(lines)
    title = re.sub(r"\s+", " ", parser.title).strip()
    return text, parser.links, title


def safe_filename(url: str) -> str:
    p = urlparse(url)
    base = (p.path or "index").strip("/")
    if not base:
        base = "index"
    base = re.sub(r"[^a-zA-Z0-9_-]+", "_", base)
    if len(base) > 120:
        base = base[:120]
    h = hashlib.md5(url.encode("utf-8")).hexdigest()[:8]
    return f"{base}_{h}.txt"


def fetch(url: str, user_agent: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": user_agent})
    with urlopen(req, timeout=timeout) as resp:
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return ""
        return resp.read().decode("utf-8", errors="ignore")

def fetch_xml(url: str, user_agent: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": user_agent})
    with urlopen(req, timeout=timeout) as resp:
        content_type = resp.headers.get("Content-Type", "")
        if "xml" not in content_type and "text" not in content_type:
            return ""
        return resp.read().decode("utf-8", errors="ignore")

def parse_sitemap(xml: str) -> list:
    return re.findall(r"<loc>(.*?)</loc>", xml, flags=re.IGNORECASE)

def collect_sitemap_urls(user_agent: str, timeout: int) -> list:
    urls = set()
    for sm_url in SITEMAP_URLS:
        try:
            xml = fetch_xml(sm_url, user_agent, timeout)
        except Exception:
            continue
        if not xml:
            continue
        locs = parse_sitemap(xml)
        for loc in locs:
            loc = normalize_url(loc)
            if loc.endswith(".xml"):
                try:
                    sub_xml = fetch_xml(loc, user_agent, timeout)
                except Exception:
                    continue
                for sub_loc in parse_sitemap(sub_xml):
                    sub_loc = normalize_url(sub_loc)
                    if is_allowed(sub_loc):
                        urls.add(sub_loc)
            else:
                if is_allowed(loc):
                    urls.add(loc)
    return sorted(urls)

def strip_boilerplate(lines: list, boilerplate_set: set) -> list:
    return [ln for ln in lines if ln not in boilerplate_set]

def build_boilerplate_set(texts: list, threshold: float) -> set:
    if not texts:
        return set()
    counts = {}
    total = len(texts)
    for lines in texts:
        seen = set()
        for ln in lines:
            if len(ln) < 20:
                continue
            key = ln.lower()
            if key in seen:
                continue
            counts[key] = counts.get(key, 0) + 1
            seen.add(key)
    cutoff = max(2, int(total * threshold))
    return {k for k, v in counts.items() if v >= cutoff}


def crawl(
    start_urls,
    out_dir,
    max_pages,
    delay,
    user_agent,
    timeout,
    use_sitemap,
    min_chars,
    min_words,
):
    os.makedirs(out_dir, exist_ok=True)
    visited = set()
    queue = collect_sitemap_urls(user_agent, timeout) if use_sitemap else list(start_urls)
    if not queue:
        queue = list(start_urls)
    for u in start_urls:
        if u not in queue:
            queue.append(u)
    saved = 0
    texts_for_cleanup = []
    content_hashes = set()
    allow_short = set(start_urls)
    while queue and saved < max_pages:
        url = normalize_url(queue.pop(0))
        if not url or url in visited:
            continue
        visited.add(url)
        if not is_allowed(url):
            continue
        try:
            html = fetch(url, user_agent, timeout)
            if not html:
                continue
            text, links, title = textify(html)
            words = text.split()
            if url not in allow_short:
                if not text or len(text) < min_chars or len(words) < min_words:
                    continue
            if not text and title:
                text = title
            content_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
            if content_hash in content_hashes:
                continue
            content_hashes.add(content_hash)
            if text:
                path = os.path.join(out_dir, safe_filename(url))
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text + "\n")
                texts_for_cleanup.append(path)
                saved += 1
            for link in links:
                next_url = normalize_url(urljoin(url, link))
                if next_url and next_url not in visited and is_allowed(next_url):
                    queue.append(next_url)
            if delay > 0:
                time.sleep(delay)
        except Exception:
            continue
    return texts_for_cleanup


def cleanup_boilerplate(files: list, threshold: float) -> int:
    texts = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f.read().splitlines() if ln.strip()]
            texts.append(lines)
        except Exception:
            texts.append([])
    boilerplate = build_boilerplate_set(texts, threshold)
    cleaned = 0
    for path, lines in zip(files, texts):
        new_lines = strip_boilerplate(lines, boilerplate)
        if new_lines != lines:
            cleaned += 1
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_lines) + "\n")
            except Exception:
                continue
    return cleaned


def main():
    parser = argparse.ArgumentParser(description="Fetch barr.com pages into context/web as .txt")
    parser.add_argument("--out", default=os.path.join("context", "web"), help="Output folder")
    parser.add_argument("--max-pages", type=int, default=5000, help="Max pages to fetch")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between requests (seconds)")
    parser.add_argument("--timeout", type=int, default=20, help="Request timeout (seconds)")
    parser.add_argument("--user-agent", default="ProposalBuilderBot/1.0", help="User-Agent header")
    parser.add_argument("--use-sitemap", action="store_true", help="Seed crawl from sitemap.xml")
    parser.add_argument("--min-chars", type=int, default=200, help="Minimum extracted chars to save")
    parser.add_argument("--min-words", type=int, default=50, help="Minimum extracted words to save")
    parser.add_argument("--cleanup", action="store_true", help="Remove boilerplate lines after crawl")
    parser.add_argument("--boilerplate-threshold", type=float, default=0.3, help="Line frequency threshold")
    args = parser.parse_args()

    saved_files = crawl(
        START_URLS,
        args.out,
        args.max_pages,
        args.delay,
        args.user_agent,
        args.timeout,
        args.use_sitemap,
        args.min_chars,
        args.min_words,
    )
    if args.cleanup and saved_files:
        cleanup_boilerplate(saved_files, args.boilerplate_threshold)


if __name__ == "__main__":
    main()
