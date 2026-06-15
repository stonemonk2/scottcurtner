---
# publish-control

Execute the scottcurtner.com publish protocol.
Claude Code (CC) executes all steps without asking for
confirmation, then produces a structured output log.

## Step 0 — Load Protocol from Wiki

Attempt to read `scottcurtner-website-publish-protocol.md`
from the Open Brain MCP wiki at:
https://raw.githubusercontent.com/stonemonk2/scottcurtner-wiki/main/scottcurtner-website-publish-protocol.md

If successful: follow that document as the authoritative
protocol for all execution steps.

If unreachable: log the following before executing anything,
then execute the hardcoded fallback protocol below:

  [FALLBACK] Wiki unreachable — executing hardcoded
             fallback protocol. Reason: [error or timeout]

Regardless of whether wiki loaded or fallback fired,
run a divergence check between the hardcoded fallback
steps in this skill and the wiki protocol, and log:

  [CHECK] Skill fallback vs wiki alignment:
          Wiki loaded: YES / NO
          Match: YES / NO
          If NO — [list each step that differs]

After all execution steps complete, prompt Scott to paste
the output log into Claude chat with:
"Paste this log into Claude chat and say:
Validate CC publish log against wiki protocol"

---

## Fallback Protocol (execute if wiki unreachable)

**1. sitemap.xml**
Add a <url> entry:
- <loc>: canonical URL provided
- <lastmod>: today's date YYYY-MM-DD
- <changefreq>: monthly
- <priority>: 0.8 for articles, 1.0 for index.html only
- Never include google3daeab9f4ca3935f.html

**2. llms.txt**
Add under ## Writing (newest-first):
- Format: - [Title](URL): Description.
- Description = the page's meta description content exactly

**3. index.html Writing section**
Add article card before first existing card (newest-first):
- Match existing article-card div pattern exactly
- Include article-date, article-title, article-excerpt, arrow
- Date format: Month YYYY · scottcurtner.com
- href must match canonical URL

**4. SEO check on new HTML file**
Confirm all present — add if missing:
- <link rel="canonical"> as first tag in <head>
- <meta name="description"> under 160 characters
- <title> under 60 characters
- og:title, og:description, og:url, og:type
- Inline SVG favicon
- Connect footer block before </body>
- Flag as [WARN] anything that cannot be auto-fixed

---

## Output Log Format

Produce this exact format after all steps complete:

PUBLISH RUN — [YYYY-MM-DD] — [Article Title]
[FALLBACK] Wiki unreachable — executing hardcoded fallback.
           Reason: [error] (only if fallback fired)
[CHECK] Skill fallback vs wiki alignment:
        Wiki loaded: YES / NO
        Match: YES / NO
        If NO — [list each step that differs]
[DONE] sitemap.xml — added [URL], lastmod [date]
[DONE] llms.txt — added entry under ## Writing
[DONE] index.html — article card added at position 1
[DONE] SEO check — canonical, OG tags, favicon,
        meta description, connect footer all present
[WARN] [anything flagged but not auto-fixed]
[SKIP] og:image — deferred pending hero image project
---
