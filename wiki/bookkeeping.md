# Bookkeeping System Wiki
Last updated: May 23, 2026

## Overview
Scott's personal bookkeeping system for a multi-property real estate rental portfolio. Built as a Quicken replacement using Python, Excel 365, and Plaid API. Manages 17+ accounts across Wells Fargo, Chase, and Bank of America covering 7 rental properties plus personal finances.

**Current status:** Plaid production live ✅ | All agents complete ✅ | 100% auto-categorization ✅ | WF + BofA connected ✅ | Chase pending OAuth approval (est. 24hrs from May 23)

---

## Project Evolution
| Date | Milestone |
|------|-----------|
| Early 2026 | Manual Excel bookkeeping — data entry by hand |
| May 3, 2026 | Built wf_import.py — CSV import with 100% auto-categorization |
| May 3, 2026 | Added Source + PlaidTxnID columns. Ledger tab deleted — AllTransactions_Input is single source of truth |
| May 3, 2026 | Plaid Sandbox tested successfully |
| May 22, 2026 | Plaid Production live — WF OAuth completed, 17 accounts under WellsFargo_All token |
| May 22, 2026 | plaid_to_import.py built — 299 WF transactions, 100% auto-categorized |
| May 22, 2026 | AllTransactions_Input cleaned — unified single table, all property tabs updating |
| May 23, 2026 | Agent 4 (duplicate detection) complete — PlaidTxnID checked before import |
| May 23, 2026 | BofA connected — BofA_All token, 2 accounts (both SKIP — minimal activity) |
| May 23, 2026 | Chase OAuth submitted for review — est. 24 hours. 492 San Angelo lives at Chase (...3979) |
| May 23, 2026 | Scheduler (Agent 3) cancelled — manual weekend workflow is sufficient |

---

## Current State (May 23, 2026)
- **AllTransactions_Input:** Clean unified single table, ~500 rows, Jan 1 – May 23, 2026
- **Property tabs:** All updating correctly via LET formulas from rngLedger
- **WF accounts:** All 17 connected via Plaid Production (WellsFargo_All token)
- **BofA accounts:** Connected (BofA_All token) — both accounts SKIPped (minimal activity)
- **Chase:** OAuth in review — connect after approval, will add 492 San Angelo (...3979)
- **Auto-categorization:** 100% on both CSV and Plaid imports
- **Duplicate detection:** Active — PlaidTxnID checked against AllTransactions_Input col B before import

---

## Weekend Bookkeeping Workflow
1. Close Excel workbook
2. `cd "C:\Users\stone\OneDrive\Desktop\Stuff\open-brain\Plaid\Sandbox"`
3. `python plaid_to_import.py --days 90`
4. If "Writing to Excel: 0" → nothing new, done
5. If new rows → open Excel, review CSV_Import tab (red = needs review)
6. Copy cols A–L → paste values only → AllTransactions_Input (skip col M AcctMask)
7. Property tabs auto-update

---

## File Locations
- **Excel workbook:** `C:\Users\stone\OneDrive\Desktop\Stuff\Backup\Finances\00-Bookkeeping\Bookkeeping-2026-claude.xlsx`
- **Bookkeeping scripts:** same folder as workbook (`wf_import.py`, `wf_importer_app.py`, `WF_Importer.bat`)
- **Plaid scripts:** `C:\Users\stone\OneDrive\Desktop\Stuff\open-brain\Plaid\Sandbox\`
- **Plaid files:** `sandboxSecret.env`, `productionSecret.env`, `tokens.json` (NEVER commit to GitHub)

---

## Excel Workbook Architecture

### Named Ranges (Name Manager — Ctrl+F3)
- `rngLedger` → `=AllTransactions_Input!$A:$K` ← CRITICAL: must point here
- `tblInput` → `=AllTransactions_Input!$C$2:$KS...`
- `EntityList` → `=Setup!$A$2:$A$9`

### AllTransactions_Input Column Schema (A through K)
| Col | Field | Notes |
|-----|-------|-------|
| A | Source | WF_CSV, PLAID, MANUAL |
| B | PlaidTxnID | Blank for CSV; populated by Plaid — enables duplicate detection |
| C | Date | m/d/yyyy — format all dates consistently via Ctrl+1 |
| D | BaseEntity | Property name or Personal |
| E | Type | Income or Expense |
| F | Category | From Categories sheet taxonomy |
| G | Description | Raw merchant/transaction description |
| H | Amount | Absolute value (always positive) |
| I | Method | Visa, Zelle, Direct Withdrawal, Wells Bill Pay, etc. |
| J | SplitRule | e.g. 2260/6 for shared utility splits |
| K | Notes | Manual notes |

### Property Tab LET Formula Template
Replace `[PROPERTY]` with exact property name in two places:
```excel
=LET(d,rngLedger,jr,FILTER(d,INDEX(d,,4)="[PROPERTY]","No Data"),dateCol,INDEX(jr,,3),typeCol,INDEX(jr,,5),catCol,INDEX(jr,,6),descCol,INDEX(jr,,7),amtCol,INDEX(jr,,8),methCol,INDEX(jr,,9),isExp,typeCol="Expense",isInc,typeCol="Income",data,HSTACK(dateCol,IF(SEQUENCE(ROWS(jr)),"[PROPERTY]"),typeCol,IF(isExp,catCol,""),IF(isExp,amtCol,""),IF(isInc,catCol,""),IF(isInc,amtCol,""),methCol,descCol),headers,{"Date","Entity","Type","Expense Category","Expense Amount","Income Category","Income Amount","Method","Comment"},VSTACK(headers,SORTBY(data,dateCol,1,typeCol,-1)))
```
Property names: `121 Santa Fe`, `8178 Humboldt`, `8173 Humboldt`, `7587 Fremont`, `492 San Angelo`, `330 Leslie`, `Joint Rental`, `Personal`

### Troubleshooting Property Tabs Not Updating
1. Check Name Manager (Ctrl+F3) — rngLedger must = `=AllTransactions_Input!$A:$K`
2. Check formula column indices — Date=3, BaseEntity=4, Type=5, Category=6, Description=7, Amount=8, Method=9
3. Check AllTransactions_Input is ONE unified table (not two) — Table Design → Convert to Range on each, delete blank rows between them, re-add filter with Ctrl+Shift+L

---

## Python Scripts

### wf_import.py — CSV Import Engine
**Location:** Same folder as Excel workbook
**Run:** `python wf_import.py YourExport.csv` or via WF_Importer.bat

**CSV format:** Both checking and CC use same WF header (DATE, DESCRIPTION, AMOUNT, CHECK #, STATUS). CC detected by filename containing "credit"/"visa"/"creditcard".

**SKIP rules:** ONLINE PAYMENT THANK YOU, ONLINE TRANSFER TO CURTNER

**RULES changelog:**
- 2026-04-20: Initial rules
- 2026-05-03: CC/checking auto-detect; Source/PlaidTxnID; SKIP rules; 15+ new merchants; fixed categorize() return bug; double-space patterns
- 2026-05-22: Plaid clean-name variants (Best Buy, Lowe's, CVS, Google One, Shake Shack, Philz, Ulta); JPMORGAN CHASE ACH; DEPOSIT MADE IN A BRANCH; Singer Lewak; ISACA; The Melt; Lunardi's; Republic Trash; Comcast alternate format

**Workflow:** Export CSV → drag to WF_Importer app → review CSV_Import (red=review, orange=dupe) → copy cols A–L → paste values only → AllTransactions_Input

### plaid_link_server.py — Plaid OAuth Connector
**Location:** Plaid Sandbox folder
**Run:** `python plaid_link_server.py` → open http://localhost:5000
**Purpose:** One-time authentication per bank institution. Saves access tokens to tokens.json.

**OAuth notes:**
- Redirect URI registered: `http://localhost:5000/oauth-callback`
- Data Transparency use cases published: "Track and manage your finances", "Prepare your taxes", "Do business accounting and tax preparation"
- Chase requires OAuth registration (submitted May 23, est. 24hr review)
- BofA and WF connect without extra steps

### plaid_to_import.py — Plaid Transaction Importer
**Location:** Plaid Sandbox folder
**Run:** `python plaid_to_import.py --days 90` (Plaid limit = 90 days)

**Key behaviors:**
- Reads all tokens from tokens.json
- Checks PlaidTxnID against AllTransactions_Input col B — skips dupes
- Plaid sign convention: positive=debit(expense), negative=credit(income) — opposite of WF CSV
- AcctMask col M is debug only — exclude when pasting to AllTransactions_Input (copy A–L only)
- Source = "PLAID"

**Output counters:**
- Skipped (invest): brokerage/IRA/savings accounts
- Skipped (dupes): already in AllTransactions_Input ← key metric
- Skipped (rules): SKIP rules (CC payments, internal transfers)
- Writing to Excel: new transactions to review

---

## Plaid Integration

### Connected Tokens (tokens.json)
| Nickname | Institution | Accounts | Status |
|----------|------------|----------|--------|
| WellsFargo_All | Wells Fargo | 17 | ✅ Live |
| BofA_All | Bank of America | 2 | ✅ Connected (both SKIP) |
| Chase_All | Chase | ~3 | ⏳ OAuth in review (submitted May 23) |

### WF Account Map (mask → BaseEntity)
| Mask | Entity | Notes |
|------|--------|-------|
| 1283 | 8178 Humboldt | |
| 1424 | 8173 Humboldt | Jerry Downer deposits direct at branch |
| 1432 | 7587 Fremont | |
| 1658 | SKIP | Old SBEF account |
| 3669 | 121 Santa Fe | Maricella moved out May 2026 |
| 3775 | Personal | Scott Only checking |
| 3817 | Personal | Jill and Scott Premier Checking |
| 7451 | Personal | Visa Signature CC |
| 6346,9471,2091,6726,6875,7217,7658,7834,8223 | SKIP | Savings/investment/brokerage |

### BofA Account Map
| Mask | Entity | Notes |
|------|--------|-------|
| 3153 | SKIP | Adv Tiered Interest Chkg — personal, minimal activity |
| 4123 | SKIP | Advantage Savings — personal, minimal activity |

### Chase Account Map (add after OAuth approved)
| Mask | Entity | Notes |
|------|--------|-------|
| 3979 | 492 San Angelo | Total Checking — operating account |
| 5022 | SKIP | Mortgage Loan — 7587 Fremont ($122k, $1,659/mo) |
| 2020 | SKIP | Mortgage Loan — 8173 Humboldt ($135k, $1,810/mo) |

**To activate Chase after OAuth approved:**
1. Run plaid_link_server.py → connect Chase → nickname Chase_All
2. Verify masks in tokens.json
3. Uncomment Chase entries in ACCOUNT_MAP in plaid_to_import.py
4. Run `python plaid_to_import.py --days 90` — 492 San Angelo transactions will appear

### Plaid Dashboard Settings
- **Redirect URI:** http://localhost:5000/oauth-callback (saved)
- **Data Transparency:** Published with 3 use cases
- **Client ID:** 69de90dffe8792000e47340b
- **Pricing:** Subscription per Item — pull frequency doesn't affect cost
- **Trial plan:** Up to 10 Items free

---

## Properties & Mortgages Reference
| Property | Entity | Bank | Notes |
|----------|--------|------|-------|
| 2260 Charleston Ave, San Bruno CA | Joint Rental | WF | 6-unit, splits 2260/6 |
| 330 Leslie St | 330 Leslie | WF | |
| 492 San Angelo Ave | 492 San Angelo | Chase (...3979) | HOA property |
| 121 Santa Fe Ave | 121 Santa Fe | WF (...3669) | Richmond CA rent control |
| 7587 Fremont Blvd | 7587 Fremont | WF (...1432) | Chase mortgage ...5022 |
| 8178 Humboldt Ave | 8178 Humboldt | WF (...1283) | |
| 8173 Humboldt Ave | 8173 Humboldt | WF (...1424) | Chase mortgage ...2020; Jerry Downer deposits direct |

**Tenant notes:**
- Jerry Downer (8173 Humboldt): 3% annual increase. Deposits at WF branch → "DEPOSIT MADE IN A BRANCH/STORE"
- Maricella (121 Santa Fe): Moved out end of May 2026
- 121 Santa Fe: Richmond CA rent control — check allowable % before raising rent
- All leases: 3–5% automatic annual increases except 121 Santa Fe
- WF follow-up: Call about BUSINESS CHECKING ...1658 — may be closed account

---

## Future Tasks
- [ ] Connect Chase_All after OAuth approved (est. May 24) — activate 492 San Angelo
- [ ] Consider closing BofA accounts (minimal activity, separate from main WF relationship)
- [ ] Bank Account Dashboard — all accounts with balances + transaction subview (discuss architecture)
- [ ] Windows Desktop App — one-click bookkeeping session launcher with guided checklist post-sync
- [ ] Call WF about BUSINESS CHECKING ...1658

## Roadmap Phases
**Phase 1 — Complete (May 23, 2026)** ✅
- wf_import.py at 100% categorization
- Plaid production live (WF, BofA connected; Chase pending)
- All 4 agents complete (connector, normalizer, scheduler cancelled, duplicate detection)

**Phase 2 — Blog Post + LinkedIn**
- HTML article on scottcurtner.com after Chase connected
- Story arc: tech auditor builds Quicken replacement with Claude + Plaid
- Audit lens + architecture overview + cost comparison vs Quicken ~$12/month
- LinkedIn article teaser + supporting post
- Tipping point for Phase 3: someone reaches out wanting to build it

**Phase 3 — Only if demand warrants**
- Config-driven refactor (personal data → config.json, gitignored)
- Public repo: stonemonk2/plaid-excel-bookkeeping (sanitized template)
- README install guide in public repo

---

## Blog Post Notes
**Title:** "Building a Quicken Replacement with Python, Excel, and Plaid"
**Format:** HTML on scottcurtner.com (not Google Docs)
**Publish trigger:** After Chase connected and first 492 San Angelo transactions imported
**Must include:** Auditability section per content pipeline protocol
