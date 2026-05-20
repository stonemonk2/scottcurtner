# Scott Curtner — Wiki Index
**Last updated:** May 20, 2026
This index lists all wiki pages in the `stonemonk2/scottcurtner` GitHub repo under `/wiki/`. Each page is a reference document Claude loads on demand when relevant keywords appear in conversation.

---

## Wiki Pages

### 🌿 Garden Inventory
**File:** `garden-inventory.md`
**Load when:** garden, plants, planting, harvest, pruning, Guadalupe, backyard, front yard, front bed, blueberry, fruit trees, myoporum, jasmine, lily, daisy, avocado, agapanthus, gladiolus, roses, azalea, abutilon, cordyline, fern, orchid
**Description:** Complete plant inventory for 2260 Charleston Ave — all zones (backyard, front yard, front bed, front side entryway). Includes plant IDs, care notes, planting dates, observations, and open tasks. Guadalupe gardening service log also tracked here.

---

### 🏠 Home Maintenance
**File:** `home-maintenance.md`
**Load when:** home maintenance, perimeter spray, pest control, bifenthrin, Western Exterminators, pump sprayer, hazmat, eaves, foundation, house structure, shed, contracted services, DIY spray
**Description:** Home maintenance programs and equipment for 2260 Charleston Ave. Currently covers: DIY perimeter pest spraying program (replacing Western Exterminators), full equipment inventory, PPE protocol, application procedure, and open tasks. Contracted services log (excluding Guadalupe, who is tracked in garden-inventory.md).

---

### 💼 Resume & Career
**File:** `resume.md` *(if exists)*
**Load when:** resume, career, job search, AAIA, audit, GRC, Wells Fargo, Bank of America, technology audit, ISACA, CIA, CISA

---

### 🏡 Real Estate
**File:** `real-estate.md` *(if exists)*
**Load when:** real estate, rental, property, tenant, rent, 330 Leslie, 8178, 8173, 7587, 492, 121, portfolio, Colorado, Arizona
**Note:** Bookkeeping, Schedule E, and Zelle are intentionally excluded here — those trigger the bookkeeping wiki instead.

---

### 💰 Bookkeeping System
**File:** `bookkeeping.md`
**Load when:** bookkeeping, wf_import, wf_importer, CSV_Import, AllTransactions_Input, Plaid, plaid_link_server, plaid_to_import, plaid_sandbox_test, RentTracker, Schedule E, categorize, RULES, rngLedger, tblInput, Python bookkeeping, Excel ledger, transaction import, auto-categorization, plaid-python, StoneMonk, sandboxSecret, Zelle
**Description:** Complete reference for Scott's Python + Excel + Plaid bookkeeping system. Covers: Excel workbook architecture (AllTransactions_Input schema, named ranges, property tab LET formulas), wf_import.py (CSV auto-detection, categorization rules, SKIP logic, change log), Plaid setup (sandbox tested, production approved, Trial plan), multi-agent build plan for production connector, blog post notes, and property reference.

---

### 🌐 Websites & Content
**File:** `websites.md` *(if exists)*
**Load when:** scottcurtner.com, scurtner.com, stonemonk.com, GreatHome.us, GitHub Pages, DNS, article, blog, content pipeline, Cloudflare

---

### 🧠 Open Brain & MCP
**File:** `open-brain.md` *(if exists)*
**Load when:** Open Brain, MCP, Supabase, memory, wiki protocol, agent index, capture thought, save protocol

---

## Load Protocol
When Scott says **"check the wiki"** or **"load my [topic] wiki"** — fetch immediately and confirm: *"I've loaded your [topic] wiki."*
When keywords from the trigger list above appear in conversation — fetch the relevant wiki page before responding. Never ask Scott to re-explain what's in a wiki.
**Wiki base URL:** `https://raw.githubusercontent.com/stonemonk2/scottcurtner/main/wiki/`
