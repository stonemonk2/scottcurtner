# Open Brain — Project Wiki
**Scott Curtner | Last compiled: May 18, 2026**
*Source: Open Brain entries. Update source entries in Open Brain, not this document.*

---

## What Is Open Brain?

A persistent AI memory system connecting Claude to a private Supabase database via a custom MCP server. Stores thoughts, tasks, notes, and memories permanently — searchable by meaning, not keywords. Claude retrieves relevant entries at the start of every conversation, making every session context-aware.

**Architecture:**
- **Database:** Supabase (PostgreSQL + pgvector) — free tier
- **AI gateway:** OpenRouter — embeddings and metadata extraction (~$10 lasts months)
- **MCP server:** Custom Edge Function deployed on Supabase — stonemonk2/OB1 fork (v1.2.0)
- **Wiki layer:** GitHub markdown wiki folder (stonemonk2/scottcurtner/wiki/) — compiled by Claude, committed via update_wiki MCP tool
- **Keep-alive:** GitHub Actions (twice weekly ping) + Supabase Edge Function
- **Tools (7):** capture_thought, search_thoughts, list_thoughts, thought_stats, update_thought, delete_thought, update_wiki

---

## Scott's Open Brain

- **Project ref:** bvrmwtlzxwcucpotweot
- **Built:** April 3, 2026 (following Nate Jones' guide, then extended)
- **MCP version:** v1.2.0 (extended with update/delete tools + update_wiki)
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
- **May 9, 2026** — LinkedIn article published (Clarice story)
- **May 10, 2026** — Cashton install (004) completed — beta tested public guide, found KA directory fix
- **May 2026** — Wiki layer built (GitHub markdown, update_wiki MCP tool, keyword auto-load)
- **May 2026** — Wiki article + LinkedIn article published
- **May 18, 2026** — Security framing strategy documented for product expansion

---

## Public Infrastructure

- **Setup Guide (Google Sheet):** docs.google.com/spreadsheets/d/1eS1n-Mkbo8SUsNTsoPakJQHv9Rl1FIxirC0cHywcjS8
- **30 Prompts Guide (Google Doc):** docs.google.com/document/d/1T4pKZyhGt-ADaLxUS9ajWwk1Qz-miR181rnQGUU1v74
- **Email gate:** 2nd-brain-community.beehiiv.com/subscribe
- **Blog article (Clarice):** scottcurtner.com/articles/clarice-2ndbrain/
- **Blog article (Wiki):** scottcurtner.com/articles/2nd-brain-wiki/
- **LinkedIn article (Clarice):** linkedin.com/pulse/my-daughter-heading-college-i-gave-her-ai-actually-scott-3wcqc
- **LinkedIn article (Wiki):** linkedin.com/pulse/ (published May 2026)
- **GitHub fork:** github.com/stonemonk2/OB1

---

## Security Architecture

### Current Security Stack (All Installs)

Open Brain is built with a three-layer security model covering both data at rest and data in motion:

**Layer 1 — Row Level Security (RLS)**
Every Supabase database has RLS enabled. Each user's rows are invisible to every other user. Even if two clients share an infrastructure instance, their data is cryptographically isolated at the database policy level. RLS is enforced by PostgreSQL itself — not by application logic that could be bypassed.

**Layer 2 — Encryption at Rest**
Supabase encrypts all data at the storage layer (AES-256). Thoughts, embeddings, metadata — all encrypted on disk. A breach of the physical storage layer does not expose readable data.

**Layer 3 — Encryption in Transit**
All communication between Claude, the MCP server, and the Supabase database travels over HTTPS/TLS. Data in motion is encrypted end-to-end. No plaintext transmission at any point in the stack.

**Layer 4 — GitHub Token Scoping (Wiki Layer)**
The update_wiki tool uses a GITHUB_TOKEN stored as a Supabase secret (never in code). Token should be scoped to minimum required permissions: contents:write on the specific repo only. No broader GitHub access granted.

---

### Security Considerations for Professional & Sensitive Use Cases

#### The Debbie Model — Client Data Pseudonymization

For clients who use Open Brain in a professional context involving third-party personal data (therapists, coaches, consultants, financial advisors, medical professionals), a pseudonymization protocol should be established at install time:

**The principle:** Client names and identifying details never enter the Open Brain database. Instead:

- Clients are assigned opaque identifiers (e.g., Client-001, Client-002)
- A separate mapping document (encrypted spreadsheet or private database) links identifiers to real names and contact details
- The mapping document lives outside the Open Brain system entirely
- Open Brain entries reference only the identifier: "Client-007 expressed concern about..." never "Jane Smith expressed concern about..."

**Why this matters even for small businesses:**
California Consumer Privacy Act (CCPA) applies to businesses meeting certain size/revenue thresholds — most solo practitioners are exempt. However, operating as if CCPA applies costs nothing and provides meaningful protection against:
- A breach of the AI memory system exposing client identities
- A subpoena or legal discovery request that sweeps in AI memory content
- Inadvertent disclosure if AI-generated content is shared or published

The pseudonymization model means a breach of Open Brain reveals only "Client-007 had a difficult session" — not a name, not a face, not a story.

**Applicable professions to flag at install time:**
- Therapists, counselors, social workers
- Financial advisors, accountants, CPAs
- Attorneys (attorney-client privilege considerations)
- Medical/dental/veterinary professionals (HIPAA considerations)
- Executive coaches, life coaches, consultants
- Real estate agents (client financial data)
- Any role involving NDA-covered information

#### GitHub Repository Privacy

The wiki layer stores compiled markdown in a GitHub repository. Default assumption for all installs: **private repository**. A private repo means:
- Wiki content is not publicly searchable or indexable
- Access requires GitHub authentication
- Even with a valid URL, unauthorized users cannot read content

For higher-security clients, consider: wiki stored in a separate private repo from any public-facing site, with deploy keys scoped to that repo only.

#### Self-Hosted Option (Future)

For clients in regulated industries (finance, healthcare, legal), a fully self-hosted deployment eliminates cloud provider trust requirements:
- Supabase self-hosted on a private VPS or on-premises server
- GitHub replaced with a self-hosted Gitea instance
- No data ever touches Supabase's cloud infrastructure
- Full audit trail of all database access

This is a premium tier offering — more setup complexity, but the right answer for a HIPAA-covered entity or a financial firm with strict data residency requirements.

---

### Product Security Positioning

Scott's CIA/CISA background is a natural differentiator in the personal AI memory market. Most competitors have not thought through a threat model. Key positioning points:

- "Built by a technology auditor" signals credibility to security-conscious clients
- Three-layer security model (RLS + at rest + in transit) is not marketing language — it's verifiable architecture
- Pseudonymization protocol for professional use is a genuine gap in the market
- Compliance posture (CCPA-ready, HIPAA-aware) without compliance overhead

---

## Stone Monk Technologies — Product Expansion (Wiki Add-On)

The wiki layer is a candidate premium add-on to the 2nd Brain build offering. Open threads:

**Client intake questionnaire design:** What questions identify the right wiki structure for a given client? Candidate questions include: What domains of your life/work need compiled context most? What decisions do you make repeatedly that would benefit from a full briefing? What retrieval failures frustrate you — when does your AI not know enough? How comfortable are you with a monthly maintenance pass?

**Security intake questions for professional clients:** Do you work with third-party personal data? Are you subject to any professional confidentiality obligations? Does your organization have data residency requirements? These answers determine whether standard install, pseudonymization protocol, or self-hosted deployment is appropriate.

**Monthly lint pass:** Once wiki layer is live for a client, a monthly maintenance prompt checks for contradictions, stale entries, missing cross-links, and orphaned pages. This is a natural upsell — ongoing maintenance retainer vs. one-time build fee.

---

## Open Tasks

- [ ] **Fix keep-alive pings** — update GitHub Actions workflow on all 4 installs (Scott, Tiffany, Clarice, Cashton) to query REST API (`GET /rest/v1/thoughts?select=id&limit=1`) instead of pinging Edge Function. Update stonemonk2/OB1 keep-alive.yml template at the same time.
- [ ] **Auto-update wiki-index.md** — modify update_wiki tool in index.ts so every wiki page write also updates wiki-index.md in the same GitHub commit. Execution: fetch index.ts → edit → upload via GitHub Desktop → redeploy Supabase Edge Function. (v1.3.0)
- [ ] **Complete Debbie install (005)** — use updated v3 installer. Apply pseudonymization protocol at install time given her professional context.
- [ ] **StoneMonk Excel v3 rebuild** — incorporate all Clarice + Cashton gotchas
- [ ] **Set up StoneMonk Google Drive + Beehiiv gate** — professional installer version
- [ ] **Write StoneMonk blog post** — PUBLIC, share on LinkedIn
- [ ] **Build stonemonk.com** — case studies/testimonials page after several installs
- [ ] **Write Cashton blog article** — get quote + photos from Cashton first
- [ ] **Monthly wiki lint pass** — target around 6th of each month alongside memory review. Prompt: read all wiki pages, check for contradictions, stale claims, missing cross-links, orphaned pages.
- [ ] **Stone Monk wiki add-on product design** — develop client intake questionnaire, security intake questions, pricing model (one-time build vs. maintenance retainer)

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
