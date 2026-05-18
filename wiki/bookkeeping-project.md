# Bookkeeping Project Wiki
**Scott Curtner | Last compiled: May 2026**
*Source: Open Brain entries. Update source entries in Open Brain, not this document.*

---

## Project Summary

A no-subscription, fully private, locally-run real estate bookkeeping system built iteratively with AI assistance. Covers 6 rental properties, 8 tenants, across CA/CO/AZ. No QuickBooks, no cloud sync, no monthly fees.

**Tagline:** Built by a non-developer real estate investor using Excel + Python + AI — and it works.

---

## Tech Stack

| Component | Tool | Notes |
|-----------|------|-------|
| Spreadsheet | Excel 365 | LET/FILTER/VSTACK/HSTACK dynamic formulas |
| Import script | Python 3.14 (`wf_import.py`) | Regex-based auto-categorization |
| GUI app | `wf_importer_app.py` | tkinter + tkinterdnd2, drag-and-drop |
| Launcher | `Run WF Importer.bat` | Batch launcher — avoids VS opening .py files |
| Bank feed | Plaid API | Sandbox tested ✅ — production pending |
| IDE | Visual Studio (terminal) | Windows PC |
| Data enrichment | Open Brain | Quick Zelle rent payment capture |

---

## Spreadsheet Architecture

**Single source of truth:** `AllTransactions_Input` tab

**Columns (A–K):**
`Source | PlaidTxnID | Date | BaseEntity | Type | Category | Description | Amount | Method | SplitRule | Notes`

**Named ranges:**
- `rngLedger` → AllTransactions_Input A:K
- `tblInput` → AllTransactions_Input C2:K...
- `EntityList` → Setup A2:A9

**Property tabs (auto-update via LET formula):**
121SantaFe | 8178Humboldt | 8173Humboldt | 7587Fremont | 492SanAngelo | 330Leslie | JointRental | Personal

**Other key tabs:**
- `RentTracker` — tenant payment status dashboard, Conrad Villicana running balance
- `Schedule E` — IRS tax export mapped to Lines 3, 5, 7, 9–12, 14, 16–21 (one column per property)
- `CSV_Import` — staging tab for wf_import.py output (orange = duplicate, red = unmatched)

---

## Workflow

```
Download WF CSV
      ↓
Drag onto wf_importer_app.py GUI
      ↓
wf_import.py auto-categorizes via regex
      ↓
Review CSV_Import staging tab
(orange = duplicate, red = needs manual category)
      ↓
Paste confirmed rows into AllTransactions_Input
      ↓
Property tabs + RentTracker + Schedule E update automatically
```

---

## Accomplishments — Features Built

### ✅ Core Bookkeeping System
Multi-property Excel workbook with per-property tabs, AllTransactions_Input as single source of truth. LET formula template auto-filters and displays income/expense by property.

### ✅ RentTracker Dashboard
Dynamic rent status tab showing all 8 tenants' monthly payment status using SUMIFS formulas. Color-coded ✓ Paid / ✗ Outstanding. Special section for Conrad Villicana (Unit B, 121 Santa Fe) — 12-month running balance table starting from $530 overdue balance.

### ✅ Schedule E Tax Export Tab
IRS Schedule E mapped to official tax form lines. One column per property plus totals. Ready to hand to CPA or enter directly on taxes.

### ✅ CSV Import Script (wf_import.py)
- Auto-detects checking vs credit card CSV format (new WF header format)
- Populates Source=WF_CSV on every imported row
- SKIP logic: CC payments + internal WF transfers silently dropped (no double-counting)
- 15+ merchant regex rules with type, entity, category, method, SplitRule attributes
- SplitRule field auto-tags shared property expenses (e.g., '2260/6')
- 100% auto-categorization achieved on both CC and checking CSVs

### ✅ Windows GUI App (wf_importer_app.py)
Drag-and-drop Windows app. Blue drop zone turns green on file selection. Runs import in background thread to keep UI responsive. Graceful error handling.

### ✅ BAT Launcher
Simple batch file launcher — prevents Visual Studio opening .py files on double-click.

### ✅ Duplicate Detection Module (completed April 20, 2026)
Flags duplicate when date + amount + description all match — against both existing AllTransactions_Input rows AND within the same CSV. Duplicates highlighted orange. Three-field match prevents false positives on recurring same-amount payments.

### ✅ Plaid Sandbox Connected (May 3, 2026)
- 16 mock transactions pulled successfully
- StoneMonk Plaid account approved for Production
- Spreadsheet upgraded: Source + PlaidTxnID columns added
- plaid_to_import.py normalizer architecture designed

---

## Memorable Debug Moments (great article material)

**The #SPILL! Rabbit Hole:**
Adding column AutoFilters to property tabs broke dynamic LET array formulas — causing #SPILL! errors and missing April transactions. Claude went deep on XML surgery (unzipping .xlsx, editing sheet XML, removing calcChain.xml). Gemini identified the real fix in one shot: AutoFilter headers were blocking the spill range — solution was simply to delete all rows below last data row, then re-paste formula. Honest "Gemini 1, Claude 0" moment worth including in the article.

**Better practice going forward:** Use a helper column or separate summary table for sorting/filtering instead of applying AutoFilter directly on top of dynamic array formula output ranges.

**Other fixes logged:**
- Repaired truncated ZIP/EOCD in Excel file preventing openpyxl from loading
- Fixed categorize() missing return statement bug
- Fixed truncated f-string syntax error from mid-line edit glitch
- Windows date formatting: no %-m strftime flag on Windows — use `f"{date.month}/{date.day}/{date.year}"`

---

## Open Tasks

### Plaid Production Integration
- [ ] Build `plaid_link_server.py` (Flask app to authenticate real bank accounts)
- [ ] Store production access tokens securely per account
- [ ] Connect first real WF account in production
- [ ] Build `plaid_to_import.py` normalizer (maps Plaid output to AllTransactions_Input schema)
- [ ] Run scheduled pull across all 20 accounts
- [ ] Document final cost per account (estimated $16–$48/month vs Quicken ~$12/month)

### System Enhancements
- [ ] Re-import all historical transactions via CSV (Ledger tab deleted — AllTransactions_Input is now single source of truth)
- [ ] Explore scheduling/triggering automatic Plaid pulls (daily vs on-demand)
- [ ] Secure storage for Plaid access_token on Windows (local config file approach)

### Article / Publishing
- [ ] Write "How I Built a Real Estate Bookkeeping System with Excel + Python" — publish to scottcurtner.com AND GreatHome.us
- [ ] Write "Building a Quicken Replacement with Python, Excel, and Plaid" — publish AFTER Plaid production connection confirmed working end-to-end

---

## Article Angle (when ready to write)

**Hook:** "A non-developer real estate investor builds a practical, low-cost bookkeeping system using Excel + Python — without QuickBooks, without subscriptions, without cloud sync."

**Key story beats:**
1. The problem: 6 properties, 8 tenants, manual CSV downloads
2. The system: Excel + Python + AI = surprisingly powerful
3. The RentTracker and Schedule E as the payoffs
4. The #SPILL! rabbit hole — honest debugging story
5. The Plaid evolution: from manual CSV to automated bank feeds
6. The payoff: every transaction auto-categorized to the right IRS Schedule E line

**Publishing targets:** scottcurtner.com + GreatHome.us + LinkedIn

---

*To update: log bookkeeping events and milestones in Open Brain tagged "bookkeeping," then ask Claude to recompile.*
