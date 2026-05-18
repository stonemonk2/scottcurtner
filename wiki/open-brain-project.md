# Open Brain — Project Wiki
**Scott Curtner | Last compiled: May 2026**
*Source: Open Brain entries. Update source entries in Open Brain, not this document.*

---

## What Is Open Brain?

A persistent AI memory system connecting Claude to a private Supabase database via a custom MCP server. Stores thoughts, tasks, notes, and memories permanently — searchable by meaning, not keywords. Claude retrieves relevant entries at the start of every conversation, making every session context-aware.

**Architecture:**
- **Database:** Supabase (PostgreSQL + pgvector) — free tier
- **AI gateway:** OpenRouter — embeddings and metadata extraction (~$10 lasts months)
- **MCP server:** Custom Edge Function deployed on Supabase — stonemonk2/OB1 fork (v1.1.0)
- **Keep-alive:** GitHub Actions (twice weekly ping) + Supabase Edge Function
- **Tools (6):** capture_thought, search_thoughts, list_thoughts, thought_stats, update_thought, delete_thought

---

## Scott's Open Brain

- **Project ref:** bvrmwtlzxwcucpotweot
- **Built:** April 3, 2026 (following Nate Jones' guide, then extended)
- **MCP version:** v1.1.0 (extended with update/delete tools)
- **Status:** Live ✅

---

## Installs Completed

| # | Person | Relationship | Date | Status |
|---|--------|-------------|------|--------|
| 001 | Scott Curtner | Self | April 3, 2026 | Live ✅ |
| 002 | Tiffany | Friend | April 2026 | Live ✅ |
| 003 | Clarice Curtner | Daughter | May 3, 2026 | Live ✅ |
| 004 | Cashton Curtner | Son | May 10, 2026 | Live ✅ |
| 005 | Debbie | Friend | Pending | Not started |

---

## Key Milestones

- **April 3, 2026** — Scott's own Open Brain built and deployed
- **April 18, 2026** — Extended with update_thought and delete_thought tools (v1.1.0)
- **April 26, 2026** — "I Gave My AI the Ability to Edit Its Own Memory" article published
- **May 3, 2026** — Clarice install (003) completed + blog article published
- **May 9, 2026** — Beehiiv email gate live (2nd-brain-community.beehiiv.com)
- **May 9, 2026** — LinkedIn article published
- **May 10, 2026** — Cashton install (004) completed — beta tested public guide, found KA directory fix
- **May 2026** — Wiki layer started (GitHub markdown, this repo)

---

## Public Infrastructure

- **Setup Guide (Google Sheet):** docs.google.com/spreadsheets/d/1eS1n-Mkbo8SUsNTsoPakJQHv9Rl1FIxirC0cHywcjS8
- **30 Prompts Guide (Google Doc):** docs.google.com/document/d/1T4pKZyhGt-ADaLxUS9ajWwk1Qz-miR181rnQGUU1v74
- **Email gate:** 2nd-brain-community.beehiiv.com/subscribe
- **Blog article:** scottcurtner.com/articles/clarice-2ndbrain/
- **LinkedIn article:** linkedin.com/pulse/my-daughter-heading-college-i-gave-her-ai-actually-scott-3wcqc
- **GitHub fork:** github.com/stonemonk2/OB1

---

## Open Tasks

- [ ] Fix keep-alive pings — current GitHub Actions workflow pings Edge Function URL, not database directly. Must update to REST API query: `GET /rest/v1/thoughts?select=id&limit=1` with anon key. Affects all 4 installs.
- [ ] Complete Debbie install (005) using updated v3 installer
- [ ] StoneMonk Excel v3 rebuild (all Clarice + Cashton gotchas)
- [ ] Set up StoneMonk Google Drive + Beehiiv gate (professional installer version)
- [ ] Write StoneMonk blog post — PUBLIC, share on LinkedIn
- [ ] Build stonemonk.com case studies/testimonials page (after several installs)
- [ ] Write Cashton blog article (get quote + photos from Cashton first)
- [ ] Update stonemonk2/OB1 keep-alive.yml template with correct REST API ping

---

## Known Gotchas (Installer Reference)

1. Project name defaults to "[Name]'s Project" — change to "open-brain" before Create
2. SQL copy-paste double-quote bug — double-click cell → Ctrl+A → Ctrl+C
3. Double-quote inside policy name gets extra quotes
4. OpenRouter needs $10 credits BEFORE session — enable auto top-up
5. --no-verify-jwt flag is CRITICAL on every deploy
6. VS Code Deno prompt — answer N twice
7. Keep-alive.ts must be named index.ts for Supabase Edge Functions
8. Keep-alive Edge Function needs its own deno.json
9. supabase logout → login → projects list BEFORE each new install
10. Deploy must run from correct project folder
11. GitHub repo: click "Skip this and set up a workflow yourself →" on Quick Setup page
12. Must click "Commit changes" TWICE in GitHub workflow creation
13. SUPABASE_URL secret = full MCP Server URL (not just base Supabase URL)
14. Claude memory between chats must be enabled in Settings → Memory
15. KA directory must be created before Invoke-WebRequest: `New-Item -ItemType Directory -Path "supabase\functions\open-brain-keepalive" -Force`
16. Verify file landed before deploy: `Get-Item supabase\functions\open-brain-keepalive\index.ts`

---

*To update this wiki: add milestones and tasks to Open Brain, then ask Claude to recompile.*
