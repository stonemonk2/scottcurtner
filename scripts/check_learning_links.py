"""Checks the learning/ HTML tree: relative links resolve, no malformed
closing anchor tags, no leftover M1-M4 milestone terms."""
import re
import sys
import pathlib
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path("learning")
checks = sys.argv[1:] or ["links", "tags", "terms"]
failures = []

for page in sorted(ROOT.rglob("*.html")):
    text = page.read_text(encoding="utf-8")

    if "links" in checks:
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            url = m.group(1)
            if url.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = unquote(urlparse(url).path)
            if not path_part:
                continue
            if path_part.startswith("/"):
                target = pathlib.Path.cwd() / path_part.lstrip("/")
            else:
                target = page.parent / path_part
            target = target.resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                failures.append(f"{page}: broken link {url}")

    if "tags" in checks:
        if re.search(r"<\\a>", text):
            n = len(re.findall(r"<\\a>", text))
            failures.append(f"{page}: {n} malformed closing tag(s) <\\a>")

    if "terms" in checks:
        for m in re.finditer(r"\bM[1-4]\b", text):
            failures.append(f"{page}: leftover milestone term {m.group(0)}")

print(f"{len(failures)} failure(s)")
for f in failures:
    print(" -", f)
sys.exit(1 if failures else 0)
