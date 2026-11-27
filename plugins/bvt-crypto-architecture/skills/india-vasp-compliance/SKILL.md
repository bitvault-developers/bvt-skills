---
name: india-vasp-compliance
description: Translates India virtual digital asset regulatory obligations into engineering requirements. Use when implementing know-your-customer and anti-money-laundering checks, the Travel Rule, tax withholding, sanctions screening or transaction reporting for a crypto exchange or wallet serving Indian users. This is engineering guidance and not legal advice; output must be reviewed by qualified counsel and a chartered accountant.
---

# India VASP Compliance → Engineering Requirements

**Not legal advice.** Every rule below must be confirmed with counsel/CA before production. India's tax law recodification means **section numbers must be re-verified at build time**.

## Status
A VDA service provider is a **reporting entity under the PMLA** (Ministry of Finance notification, 7 March 2023; FIU-IND AML/CFT guidelines from 10 March 2023, updated 8 January 2026). The obligation is **activity-based, not presence-based** — serving Indian users triggers it regardless of where you are incorporated.

## Schema requirements (design these in from migration one)
```
users:        kyc_status, kyc_level, verified_at, pep_flag, risk_score,
              sanctions_checked_at, source_of_funds
transactions: originator_name, originator_address, originator_id,
              beneficiary_name, beneficiary_address, counterparty_vasp,
              travel_rule_status, tds_withheld, tds_deposited_ref
reports:      str_id, filed_at, subject_user, narrative, status
```
Retrofitting these into a live ledger is far worse than carrying them from the start.

## Travel Rule — **zero threshold in India**
Unlike the FATF-suggested ~USD/EUR 1,000 de-minimis, **India applies no threshold**. Full originator and beneficiary information must be collected, verified and transmitted **for every VDA transfer**, before or at the time of transfer.
- Block the transfer if required fields are missing — do not queue and hope.
- Transfers to **unhosted wallets** are treated as higher risk: additional verification of control, and enhanced record-keeping.
- Counterparty VASP must be identified and its status recorded.

## Tax withholding
- **1% TDS at the transaction point** (§194S, Finance Act 2022, effective 1 July 2022). Deduct, deposit, and surface in the user's Form 26AS / AIS. **Applies to crypto-to-crypto barter**, not only crypto-to-fiat.
- Thresholds: **₹50,000 per financial year for "specified persons"** (small individuals/HUFs) and **₹10,000 for everyone else** — sources conflict on which applies to whom, so **confirm the mapping with a CA before coding it**.
- **30% flat tax + 4% cess** on gains (§115BBH, from 1 April 2022). No loss set-off, no carry-forward, only cost of acquisition deductible. Users report via **Schedule VDA** in ITR-2/ITR-3.
- Provide downloadable per-user tax statements; this is a support-load reducer as much as a compliance one.

## Sanctions screening
Screen **at onboarding, on KYC refresh, on every list update, and before every transfer** against:
- UNSC consolidated lists — ISIL/Al-Qaida (1267/1989/2253) and Taliban (1988), **verified daily**
- UAPA §51A domestic designations
- WMD Act §12A proliferation-financing list

On a match: **freeze immediately**, do not tip off the customer, and report to **FIU-IND and the Ministry of Home Affairs**. Log the screening event with the list version — you must be able to prove when you screened and against what.

## Governance and reporting
- Appoint a **Designated Director** and a **separate Principal Officer** (two people, not one).
- File **STRs within 7 working days** of forming suspicion; also CTRs and counterfeit/cross-border reports as applicable.
- **Retain records ≥5 years.**
- Maintain written, board-approved AML/CFT policy, risk assessment, and training records — the documents are themselves an obligation.

## Forward-looking
OECD **CARF** crypto reporting (~2027) is not yet in force but will require counterparty and account reporting; design the schema so it can be produced.
