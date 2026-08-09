"""Verifies the scottcurtner.com publish protocol mechanically.

The filesystem is the source of truth: every article page that exists on
disk must appear on every metadata surface (sitemap.xml, llms.txt, the
homepage Writing section, the /articles/ hub) and carry the required SEO
tags. Turns the publish log's [DONE] lines from claims into checked facts.

Usage:  python scripts/check_site.py [check ...]
Checks: surfaces seo links tags robots   (default: all)
Exit:   0 clean, 1 violations found.
"""
import re
import sys
import html
import json
import pathlib
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.scottcurtner.com"
VERIFICATION_FILE = "google3daeab9f4ca3935f.html"

# Crawlers the protocol requires to keep Allow: / in robots.txt.
AI_CRAWLERS = [
    "OAI-SearchBot", "ChatGPT-User", "ClaudeBot",
    "Claude-User", "PerplexityBot", "Perplexity-User",
]

# Titles that run past 60 chars on purpose — the full phrasing carries the piece
# and Scott has accepted the SERP truncation. Reviewed 2026-08-04. A new long
# title still warns, which is the point: this records a decision, not a mute.
ACCEPTED_LONG_TITLES = {
    "articles/agentic-engineering/index.html",
    "articles/okf-freshness/index.html",
    "articles/publish-control/index.html",
    "articles/rewired-memory/index.html",
}

errors: list[str] = []
warnings: list[str] = []


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def discover_articles() -> list[tuple[pathlib.Path, str]]:
    """Every published article on disk, as (file, site-root-relative URL)."""
    found = []
    for page in sorted(ROOT.glob("articles/**/*.html")):
        rel = page.relative_to(ROOT).as_posix()
        if rel == "articles/index.html":
            continue  # the hub itself, not an article
        url = f"/{rel[:-len('index.html')]}" if page.name == "index.html" else f"/{rel}"
        found.append((page, url))
    for page in sorted(ROOT.glob("article-*.html")):
        found.append((page, f"/{page.name}"))
    return found


def check_surfaces(articles):
    """Each article must appear on all four metadata surfaces."""
    surfaces = {
        "sitemap.xml": read(ROOT / "sitemap.xml"),
        "llms.txt": read(ROOT / "llms.txt"),
        "index.html": read(ROOT / "index.html"),
        "articles/index.html": read(ROOT / "articles/index.html"),
    }
    for page, url in articles:
        for name, text in surfaces.items():
            # Surfaces reference articles four ways: absolute URL, root-relative,
            # relative to the site root (homepage), and relative to /articles/
            # (the hub). Accept any of them.
            candidates = [
                BASE + url, url, url.lstrip("/"), url.removeprefix("/articles/"),
            ]
            if not any(c in text for c in candidates):
                errors.append(f"{name}: missing entry for {url}")

    if VERIFICATION_FILE in surfaces["sitemap.xml"]:
        errors.append(f"sitemap.xml: must never list {VERIFICATION_FILE}")

    for m in re.finditer(r"<loc>([^<]+)</loc>", surfaces["sitemap.xml"]):
        loc = m.group(1)
        path = urlparse(loc).path
        target = ROOT / path.lstrip("/")
        if target.is_dir() or path.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            errors.append(f"sitemap.xml: <loc> points at missing file {loc}")


def check_seo(articles):
    """Required head tags and page furniture on every article."""
    for page, url in articles:
        text = read(page)
        where = page.relative_to(ROOT).as_posix()

        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        if not canonical:
            errors.append(f"{where}: no <link rel=\"canonical\">")
        elif canonical.group(1).rstrip("/") != (BASE + url).rstrip("/"):
            errors.append(
                f"{where}: canonical is {canonical.group(1)}, expected {BASE + url}"
            )

        title = re.search(r"<title>([^<]*)</title>", text)
        if not title:
            errors.append(f"{where}: no <title>")
        elif len(title.group(1)) > 60 and where not in ACCEPTED_LONG_TITLES:
            warnings.append(f"{where}: <title> is {len(title.group(1))} chars (limit 60)")

        desc = re.search(r'<meta name="description" content="([^"]*)"', text)
        if not desc:
            errors.append(f"{where}: no <meta name=\"description\">")
        elif len(desc.group(1)) > 160:
            warnings.append(
                f"{where}: meta description is {len(desc.group(1))} chars (limit 160)"
            )

        for prop in ("og:title", "og:description", "og:url", "og:type"):
            if f'property="{prop}"' not in text:
                errors.append(f"{where}: missing {prop}")

        if not re.search(r'<link rel="icon"', text):
            errors.append(f"{where}: no favicon")

        # The footer class has changed four times across the archive
        # (connect-, article-, site-, author-footer) and the three earliest
        # pages style the same block inline with no class at all. Check the
        # control the protocol actually cares about — a closing block that
        # lets a reader connect — not the markup of the week.
        has_block = any(
            m in text
            for m in (
                'class="connect-footer"', 'class="article-footer"',
                'class="site-footer"', 'class="author-footer"',
                "Connect on LinkedIn",
            )
        )
        if not (has_block and "linkedin.com/in/scottcurtner" in text):
            errors.append(f"{where}: no connect footer block")

        if (page.parent / "images").is_dir() and 'property="og:image"' not in text:
            warnings.append(f"{where}: has images/ but no og:image")


def json_ld_nodes(text: str, where: str) -> list:
    """Every JSON-LD node on a page, flattened out of any @graph. Unparseable is a violation."""
    nodes = []
    for m in re.finditer(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S
    ):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            errors.append(f"{where}: JSON-LD does not parse ({e.msg} at line {e.lineno})")
            continue
        for item in data if isinstance(data, list) else [data]:
            nodes.extend(item.get("@graph", [item]) if isinstance(item, dict) else [])
    return nodes


def check_schema(articles):
    """The homepage declares the site entity; any page with a dek carries matching FAQ schema.

    Step 5 of the protocol has always required these. Nothing verified them, so the
    publish log's SEO line was asserting them the same way it used to assert surfaces.
    """
    home = read(ROOT / "index.html")
    home_types = {n.get("@type") for n in json_ld_nodes(home, "index.html")}
    if not home_types & {"Person", "Organization"}:
        errors.append("index.html: no Person or Organization JSON-LD (site entity schema)")
    if "WebSite" not in home_types:
        warnings.append("index.html: no WebSite JSON-LD node")

    for page, url in articles:
        text = read(page)
        where = page.relative_to(ROOT).as_posix()
        nodes = json_ld_nodes(text, where)

        dek = re.search(
            r'<div class="quick-answer">\s*<h2>(.*?)</h2>', text, re.S
        )
        if not dek:
            continue  # no quick-answer dek, so no FAQ schema is owed

        # Entities in the markup ("agent&rsquo;s") must compare equal to the plain
        # text a schema question carries, so unescape before matching.
        heading = html.unescape(re.sub(r"<[^>]+>", "", dek.group(1)))
        heading = re.sub(r"\s+", " ", heading).strip()
        faq = [n for n in nodes if n.get("@type") == "FAQPage"]
        if not faq:
            errors.append(f"{where}: has a quick-answer dek but no FAQPage JSON-LD")
            continue

        questions = [
            q.get("name", "")
            for n in faq
            for q in (n.get("mainEntity") or [])
            if isinstance(q, dict)
        ]
        if not any(q.strip() == heading for q in questions):
            errors.append(
                f"{where}: FAQ question does not match the dek heading "
                f"(schema {questions!r} vs dek {heading!r})"
            )


def check_links():
    """Every relative href/src resolves to a file that exists."""
    for page in sorted(ROOT.glob("**/*.html")):
        if any(part in {".git", "drafts", ".claude"} for part in page.parts):
            continue
        where = page.relative_to(ROOT).as_posix()
        for m in re.finditer(r'(?:href|src)="([^"]+)"', read(page)):
            url = m.group(1)
            if url.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            path_part = unquote(urlparse(url).path)
            if not path_part:
                continue
            if path_part.startswith("/"):
                target = ROOT / path_part.lstrip("/")
            else:
                target = page.parent / path_part
            target = target.resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{where}: broken link {url}")


def check_tags():
    """Malformed closing anchors and leftover milestone terms."""
    for page in sorted(ROOT.glob("**/*.html")):
        if any(part in {".git", "drafts", ".claude"} for part in page.parts):
            continue
        where = page.relative_to(ROOT).as_posix()
        text = read(page)
        n = len(re.findall(r"<\\a>", text))
        if n:
            errors.append(f"{where}: {n} malformed closing tag(s) <\\a>")
        if page.parts[-2:][0] != "learning" and "learning" not in page.parts:
            continue
        for m in re.finditer(r"\bM[1-4]\b", text):
            errors.append(f"{where}: leftover milestone term {m.group(0)}")


def check_robots():
    """AI search crawlers stay allowed; verification file stays disallowed."""
    path = ROOT / "robots.txt"
    if not path.exists():
        errors.append("robots.txt: missing")
        return
    text = read(path)
    groups = {}
    current = None
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("user-agent:"):
            current = line.split(":", 1)[1].strip()
            groups[current] = []
        elif line and current:
            groups[current].append(line)

    for crawler in AI_CRAWLERS:
        if crawler not in groups:
            errors.append(f"robots.txt: no group for {crawler}")
        elif "Allow: /" not in groups[crawler]:
            errors.append(f"robots.txt: {crawler} lost its 'Allow: /'")

    for name, rules in groups.items():
        if not any(VERIFICATION_FILE in r for r in rules):
            errors.append(f"robots.txt: {name} group does not disallow {VERIFICATION_FILE}")

    if f"Sitemap: {BASE}/sitemap.xml" not in text:
        errors.append("robots.txt: no Sitemap line")


def main() -> int:
    requested = sys.argv[1:] or ["surfaces", "seo", "links", "tags", "robots"]
    articles = discover_articles()
    print(f"check_site: {len(articles)} article pages discovered under {ROOT}\n")

    if "surfaces" in requested:
        check_surfaces(articles)
    if "seo" in requested:
        check_seo(articles)
        check_schema(articles)
    if "links" in requested:
        check_links()
    if "tags" in requested:
        check_tags()
    if "robots" in requested:
        check_robots()

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")

    print()
    if errors:
        print(f"FAIL - {len(errors)} violation(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS - 0 violations, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
