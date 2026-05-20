# Bookkeeping System Wiki
Last updated: May 20, 2026

## Overview
Scott's personal bookkeeping system for a multi-property real estate rental portfolio. Built as a Quicken replacement using Python, Excel 365, and Plaid API. Manages 17–20 Wells Fargo, Chase, and Bank of America accounts across 7 rental properties plus personal finances.

---

## File Locations
- **Excel workbook:** `C:\Users\stone\OneDrive\Desktop\Stuff\Backup\Finances\00-Bookkeeping\Bookkeeping-2026-claude.xlsx`
- **Python scripts:** same folder as workbook
- **Plaid sandbox files:** `C:\Users\stone\OneDrive\Desktop\Stuff\open-brain\plaid\sandbox\`
- **Plaid credentials:** `sandboxSecret.env` (Client ID + Sandbox/Production secrets)

---

## Excel Workbook Architecture

### Named Ranges (Name Manager)
- `rngLedger` → `=AllTransactions_Input!$A:$K` (full column range, source of truth)
- `tblInput` → `=AllTransactions_Input!$C$2:$KS...` (starts at Date column)
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
| A | Source | WF_CSV, PLAID, MANUAL, ZELLE |
| B | PlaidTxnID | Blank for CSV imports; populated by Plaid |
| C | Date | m/d/yyyy |
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

---

## Python Scripts

### wf_import.py — Main Import Engine
**Purpose:** Reads WF CSV exports, auto-categorizes transactions, writes staging sheet to Excel.

**Run:** `python wf_import.py YourExport.csv` or via `WF_Importer.bat` (drag-and-drop GUI)

**CSV Format Detection:**
- Both checking and credit card CSVs now use same WF header format: `DATE, DESCRIPTION, AMOUNT, CHECK #, STATUS`
- Credit card detected by filename containing "credit", "visa", or "creditcard"
- Credit card amounts: kept as original sign (negative = charge, positive = payment)
- Checking amounts: already correctly signed

**Key functions:**
- `categorize(desc, amount)` — returns (type, entity, category, method, split_rule)
- `run(csv_path)` — main entry point
- SKIP rule type: silently drops rows (CC payments, internal transfers)

**RULES change log:**
- 2026-04-20: Initial rules — rent income, payroll, utilities, landscaping, maintenance, travel, charity, dining, entertainment
- 2026-05-03: Added CC/checking format auto-detect; Source/PlaidTxnID columns; SKIP rules for ONLINE PAYMENT THANK YOU and ONLINE TRANSFER TO CURTNER; new merchants: IHOP/CHILI/STARBUCKS/TOMO SUSHI, FTD, SP SPRING AND MULBERRY, APARTMENTS.COM, GOOGLE ONE, TALKSPACE, CA DMV, CAPUCHINO PTO; fixed categorize() missing return bug; tightened double-space patterns (HELEN, CLARICE, COMCAST, PAYROLL)

**Import workflow:**
1. Export CSV from Wells Fargo online banking
2. Drag onto WF_Importer app or run via command line
3. Review CSV_Import staging tab (red = needs review, orange = possible duplicate)
4. Copy reviewed rows → paste values only → AllTransactions_Input
5. Property tabs auto-update via LET formulas

**Achieved:** 100% auto-categorization on both checking and credit card CSVs (May 2026)

### wf_importer_app.py — GUI Wrapper
Tkinter drag-and-drop GUI. Double-click WF_Importer.bat to launch. Calls wf_import.run().

---

## Plaid Integration

### Account Status
- **Team:** StoneMonk
- **Client ID:** 69de90dffe8792000e47340b
- **Status:** Approved for Production (as of May 2026)
- **Trial plan:** Up to 10 Production Items free (post April 15, 2026)
- **Pricing model:** Transactions = subscription per Item (connected account), not per API call

### Sandbox Setup
- Installed: `plaid-python` v39.2.0, `python-dotenv` v1.2.2
- Credentials: `sandboxSecret.env` (PLAID_CLIENT_ID + PLAID_SANDBOX_SECRET)
- Test script: `plaid_sandbox_test.py` — successfully pulled 16 mock transactions (May 3, 2026)
- Test institution: `ins_109508` (First Platypus Bank)

### Production Plan — Next Steps
1. **Agent 1:** Build `plaid_link_server.py` — Flask app for OAuth bank authentication, stores access tokens per account
2. **Agent 2:** Build `plaid_to_import.py` — maps Plaid JSON to AllTransactions_Input schema
3. **Agent 3:** Build scheduler — GitHub Actions or Windows Task Scheduler for 2x/week pulls
4. **Agent 4:** Build test harness — validates Plaid output matches WF CSV categorization

### Plaid → AllTransactions_Input Field Mapping
| Plaid field | AllTransactions_Input column |
|-------------|------------------------------|
| `transaction_id` | B: PlaidTxnID |
| `date` | C: Date |
| (lookup table) | D: BaseEntity |
| sign of amount | E: Type (negative=Expense, positive=Income) |
| `category[0]` → rules | F: Category |
| `name` | G: Description |
| `abs(amount)` | H: Amount |
| `payment_channel` | I: Method |
| (blank) | J: SplitRule |
| `PLAID` | A: Source |

### Cost Estimate
- Accounts 1–10: Free (Trial plan)
- Accounts 11–20: Per-Item monthly subscription (exact rate requires production access application)
- Pull frequency doesn't affect cost — subscription model
- vs Quicken: ~$12/month flat

---

## Properties Reference
| Property | Entity Name | Notes |
|----------|-------------|-------|
| 2260 Charleston Ave, San Bruno CA | Joint Rental | 6-unit building, shared utility splits (2260/6) |
| 330 Leslie St | 330 Leslie | |
| 492 San Angelo Ave | 492 San Angelo | HOA property |
| 121 Santa Fe Ave | 121 Santa Fe | Richmond CA |
| 7587 Fremont Blvd | 7587 Fremont | |
| 8178 Humboldt Ave | 8178 Humboldt | |
| 8173 Humboldt Ave | 8173 Humboldt | |

---

## Blog Post Plan
**Title:** "Building a Quicken Replacement with Python, Excel, and Plaid"
**Status:** Draft — publish after Plaid production connection working end-to-end
**Story arc:** Technology auditor builds Quicken replacement for 17-20 account real estate portfolio. One post, not two. End with real cost comparison vs Quicken ~$12/month.
**Auditability section:** Required per content pipeline protocol.
