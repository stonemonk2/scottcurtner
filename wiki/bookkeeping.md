# Bookkeeping System Wiki
Last updated: May 22, 2026

## Overview
Scott's personal bookkeeping system for a multi-property real estate rental portfolio. Built as a Quicken replacement using Python, Excel 365, and Plaid API. Manages 17 Wells Fargo accounts (plus Chase and BofA pending) across 7 rental properties plus personal finances.

**Current status:** Plaid production live ✅ | Agents 1 + 2 complete ✅ | 100% auto-categorization achieved ✅

---

## Project Evolution
| Date | Milestone |
|------|-----------|
| Early 2026 | Manual Excel bookkeeping — data entry by hand |
| May 3, 2026 | Built wf_import.py — CSV import with auto-categorization. 100% hit rate on checking + CC CSVs |
| May 3, 2026 | Added Source + PlaidTxnID columns to AllTransactions_Input. Ledger tab deleted — AllTransactions_Input is single source of truth |
| May 3, 2026 | Plaid Sandbox tested — 16 mock transactions pulled successfully |
| May 22, 2026 | Plaid Production live — plaid_link_server.py built, WF OAuth completed, 17 accounts connected under WellsFargo_All token |
| May 22, 2026 | plaid_to_import.py built — 299 transactions pulled, 100% auto-categorized |
| May 22, 2026 | AllTransactions_Input cleaned — unified single table, date-sorted, all property tabs updating correctly |

---

## Current State (May 22, 2026)
- **AllTransactions_Input:** Clean, unified single Excel table. ~500 rows covering Jan 1 – May 22, 2026
- **Property tabs:** All updating correctly via LET formulas from rngLedger
- **WF accounts:** All 17 connected via Plaid Production (WellsFargo_All token)
- **Auto-categorization:** 100% on both CSV and Plaid imports
- **Chase + BofA:** Not yet connected (includes 492 San Angelo account)
- **Scheduler:** Not yet built (Agent 3)
- **Duplicate detection in Plaid:** Not yet built (Agent 4)

---

## File Locations
- **Excel workbook:** `C:\Users\stone\OneDrive\Desktop\Stuff\Backup\Finances\00-Bookkeeping\Bookkeeping-2026-claude.xlsx`
- **Python scripts (bookkeeping):** same folder as workbook
- **Plaid scripts:** `C:\Users\stone\OneDrive\Desktop\Stuff\open-brain\Plaid\Sandbox\`
- **Plaid credentials:** `sandboxSecret.env` (Sandbox), `productionSecret.env` (Production)
- **Plaid tokens:** `tokens.json` (in Sandbox folder — contains live Production access tokens, never commit to GitHub)

---

## Excel Workbook Architecture

### Named Ranges (Name Manager)
- `rngLedger` → `=AllTransactions_Input!$A:$K` ← CRITICAL: must point here, not to old Ledger sheet
- `tblInput` → `=AllTransactions_Input!$C$2:$KS...`
- `EntityList` → `=Setup!$A$2:$A$9`

### Sheet List
| Sheet | Purpose |
|-------|---------|
| `AllTransactions_Input` | Master ledger — single source of truth |
| `CSV_Import` | Staging tab — review before pasting to AllTransactions_Input |
| `121SantaFe` | Property view — LET formula filter |
| `8178Humboldt` | Property view |
| `8173Humboldt` | Property view |
| `7587Fremont` | Property view |
| `492SanAngelo` | Property view |
| `330Leslie` | Property view |
| `JointRental` | Property view |
| `Personal` | Personal finances view |
| `RentTracker` | Dashboard — monthly cash flow |
| `Schedule_E` | Tax export |
| `Categories` | Category taxonomy |
| `Setup` | EntityList and config |
| `BalanceSheet` | Balance sheet |

### AllTransactions_Input Column Schema (A through K)
| Col | Field | Notes |
|-----|-------|-------|
| A | Source | WF_CSV, PLAID, MANUAL |
| B | PlaidTxnID | Blank for CSV imports; populated by Plaid — enables duplicate detection |
| C | Date | m/d/yyyy — apply consistent format via Ctrl+1 → Number → Date |
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

**Troubleshooting property tabs not updating:**
1. Check Name Manager (Ctrl+F3) — rngLedger must point to `=AllTransactions_Input!$A:$K`
2. Check formula column indices — Date=col 3, BaseEntity=col 4, Type=col 5, Category=col 6, Description=col 7, Amount=col 8, Method=col 9
3. Check AllTransactions_Input is a single unified table (not two separate tables) — if two tables exist, Table Design → Convert to Range on each, then delete blank rows between them

---

## Python Scripts

### wf_import.py — CSV Import Engine
**Purpose:** Reads WF CSV exports, auto-categorizes, writes CSV_Import staging sheet to Excel.
**Run:** `python wf_import.py YourExport.csv` or via WF_Importer.bat (drag-and-drop GUI)
**Location:** Same folder as Excel workbook

**CSV Format Detection:**
- Both checking and CC CSVs use same WF header: `DATE, DESCRIPTION, AMOUNT, CHECK #, STATUS`
- Credit card detected by filename containing "credit", "visa", or "creditcard"
- Amounts kept as original sign — no flipping needed

**SKIP rules (silently dropped):**
- `ONLINE PAYMENT THANK YOU` — CC payments already in checking
- `ONLINE TRANSFER TO CURTNER` — internal WF account transfers

**RULES change log:**
- 2026-04-20: Initial rules
- 2026-05-03: CC/checking format auto-detect; Source/PlaidTxnID columns; SKIP rules; 15+ new merchants; fixed categorize() missing return bug; tightened double-space patterns
- 2026-05-22: Added Plaid clean-name variants (Best Buy, Lowe's Home Improvement, CVS, Google One, Shake Shack, Philz Coffee, Ulta); JPMORGAN CHASE CHASE ACH (mortgage); DEPOSIT MADE IN A BRANCH (Jerry Downer rent); Singer Lewak (accounting); Information System Audit (ISACA); The Melt, Lunardi's (dining); Republic Trash (121 Santa Fe utilities); Comcast alternate format

**Workflow:**
1. Export CSV from Wells Fargo online banking
2. Drag onto WF_Importer app or run via command line
3. Review CSV_Import tab (red = needs review, orange = duplicate)
4. Copy columns A–L → paste values only → AllTransactions_Input
5. Property tabs auto-update

### wf_importer_app.py — GUI Wrapper
Tkinter drag-and-drop GUI. Double-click WF_Importer.bat to launch.

### plaid_link_server.py — Plaid OAuth Connector
**Purpose:** One-time authentication per bank institution. Launches local Flask web server at http://localhost:5000
**Run:** `python plaid_link_server.py` from Sandbox folder
**Saves to:** `tokens.json` — one entry per institution, covers all accounts at that institution

**WF connection status:**
- Nickname: `WellsFargo_All`
- Institution: Wells Fargo
- Accounts: 17 (all WF accounts)
- Connected: May 22, 2026

**WF Account Map (mask → BaseEntity):**
| Mask | Entity | Notes |
|------|--------|-------|
| 1283 | 8178 Humboldt | |
| 1424 | 8173 Humboldt | Jerry Downer deposits direct |
| 1432 | 7587 Fremont | |
| 1658 | SKIP | Old SBEF account — not Scott's |
| 3669 | 121 Santa Fe | Maricella moving out May 2026 |
| 3775 | Personal | Scott Only |
| 3817 | Personal | Jill and Scott (Premier Checking) |
| 7451 | Personal | Visa Signature credit card |
| 6346,9471,2091,6726,6875,7217,7658,7834,8223 | SKIP | Savings/investment/brokerage |

**Important WF note:** Account 1658 is an old SBEF (San Bruno Education Foundation) account Scott previously had access to. All transactions must be skipped — not personal bookkeeping.

### plaid_to_import.py — Plaid Transaction Importer
**Purpose:** Pulls real transactions from Plaid Production, categorizes, writes CSV_Import staging sheet.
**Run:** `python plaid_to_import.py --days 90` (Plaid default limit is 90 days)
**Location:** Sandbox folder (alongside tokens.json)

**Key behaviors:**
- Reads WellsFargo_All access token from tokens.json
- Plaid sign convention: positive = debit (expense), negative = credit (income) — opposite of WF CSV
- Uses same categorize() engine as wf_import.py
- Populates PlaidTxnID column B for future duplicate detection
- Adds AcctMask column (col M) for debugging — exclude when pasting to AllTransactions_Input (copy cols A–L only)
- Source field = "PLAID"

**Achieved:** 299/299 = 100% auto-categorization (May 22, 2026)

**Workflow:**
1. Run script (Excel must be closed)
2. Review CSV_Import tab
3. Copy columns A–L → paste values only → AllTransactions_Input (skip col M AcctMask)
4. Property tabs auto-update

---

## Plaid Integration

### Account Status
- **Team:** StoneMonk
- **Client ID:** 69de90dffe8792000e47340b
- **Status:** Production approved
- **Trial plan:** Up to 10 Items free (post April 15, 2026)
- **Pricing:** Subscription per Item (not per API call) — pull frequency doesn't affect cost
- **90-day limit:** Plaid default transaction history = 90 days. Historical Update access needed for further back.

### Connections
| Nickname | Institution | Accounts | Status |
|----------|------------|----------|--------|
| WellsFargo_All | Wells Fargo | 17 | ✅ Live |
| Chase_All | Chase | TBD | ⏳ Pending |
| BofA_All | Bank of America | TBD | ⏳ Pending |

### Plaid → AllTransactions_Input Field Mapping
| Plaid field | Column | Notes |
|-------------|--------|-------|
| `PLAID` literal | A: Source | |
| `transaction_id` | B: PlaidTxnID | |
| `date` | C: Date | |
| ACCOUNT_MAP lookup | D: BaseEntity | by account mask |
| sign of amount | E: Type | |
| categorize() engine | F: Category | |
| `name` | G: Description | Plaid returns clean merchant names |
| `abs(amount)` | H: Amount | |
| categorize() engine | I: Method | |
| categorize() engine | J: SplitRule | |
| blank | K: Notes | |

**Critical note — Plaid vs WF CSV merchant names:**
Plaid returns clean merchant names (`Best Buy`, `Lowe's Home Improvement`, `CVS`) while WF CSV returns raw bank strings (`BESTBUY`, `LOWES SAN BRUNO`, `CVS/PHARMACY`). Both scripts have parallel rules for both formats.

---

## Properties Reference
| Property | Entity Name | Notes |
|----------|-------------|-------|
| 2260 Charleston Ave, San Bruno CA | Joint Rental | 6-unit, shared utility splits (2260/6) |
| 330 Leslie St | 330 Leslie | |
| 492 San Angelo Ave | 492 San Angelo | HOA property — account at Chase or BofA |
| 121 Santa Fe Ave | 121 Santa Fe | Richmond CA — rent control applies |
| 7587 Fremont Blvd | 7587 Fremont | Chase mortgage |
| 8178 Humboldt Ave | 8178 Humboldt | |
| 8173 Humboldt Ave | 8173 Humboldt | Jerry Downer — deposits direct to WF ...1424 |

**Tenant notes:**
- Jerry Downer (8173 Humboldt): 3% annual rent increase. Deposits cash/check directly at WF branch — shows as "DEPOSIT MADE IN A BRANCH/STORE"
- Maricella (121 Santa Fe): Moved out end of May 2026
- 121 Santa Fe: Richmond CA rent control — check allowable increase each year before raising rent
- All leases have automatic annual increases (3–5%) except 121 Santa Fe

**WF follow-up:** Call Wells Fargo about BUSINESS CHECKING ...1658 — may be a closed account, currently SKIPped in Plaid import

---

## Roadmap

### Phase 1 — Complete Agents (current)
- [ ] Agent 3: Scheduler — automate Plaid pulls 2x/week (GitHub Actions or Windows Task Scheduler)
- [ ] Agent 4: Duplicate detection in plaid_to_import.py — check PlaidTxnID against AllTransactions_Input before writing
- [ ] Connect Chase + BofA via plaid_link_server.py
- [ ] Confirm 492 San Angelo appears in Chase or BofA

### Phase 2 — Blog Post + LinkedIn
- [ ] HTML article on scottcurtner.com: story arc + architecture overview, audit lens, cost comparison vs Quicken
- [ ] LinkedIn article teaser + supporting post
- [ ] Auditability section required per content pipeline protocol
- [ ] Tipping point trigger for Phase 3: TBD (define what "significant interest" looks like)

### Phase 3 — Only if demand warrants
- [ ] Config-driven refactor: personal data → config.json (gitignored) + config.template.json (public)
- [ ] Create public repo: stonemonk2/plaid-excel-bookkeeping (sanitized template, no personal data)
- [ ] README.md install guide with screenshots (in public repo)
- [ ] Private live system stays in stonemonk2/scottcurtner under /bookkeeping subfolder

---

## Blog Post Plan
**Title:** "Building a Quicken Replacement with Python, Excel, and Plaid"
**Status:** Draft — publish after Phase 1 complete
**Format:** HTML article on scottcurtner.com (not Google Docs)
**Story arc:** Technology auditor builds Quicken replacement for 17-20 account real estate portfolio using Python, Excel, and Plaid. Architecture overview just detailed enough for technical reader to pursue with their own AI. Cost comparison vs Quicken ~$12/month.
**Auditability section:** Required
**LinkedIn:** Article teaser + supporting post after publish
