---
name: bvt-regulatory-translation
description: Handles translation of crypto legal, risk and regulatory content including white papers, disclosures and terms across jurisdictions. Use when translating a white paper, risk disclosure, terms of service or marketing communication for a regulated market, or when deciding whether content may be machine translated. This is engineering and process guidance, not legal advice.
---

# Regulatory & Legal Translation

**Not legal advice.** Every rule below is a process control; the content itself must be reviewed by qualified counsel in each jurisdiction.

## The obligation is language-specific
Under the EU's MiCA regime, a crypto-asset white paper must be published in **an official language of the home Member State** (or of the host Member State), must be fair, clear and not misleading, and — since the implementing regulation — must be machine-readable **XHTML with Inline XBRL tagging** against the ESMA taxonomy. PDF-only submission no longer satisfies the requirement.

The obligation attaches to a **public offer or admission to trading**, not to marketing activity alone. Marketing communications are separately regulated and the issuer remains liable for what a regional partner publishes in translation.

## Version divergence is the real risk
If the German translation of a risk disclosure uses softer language than the English original, or a technical term is rendered differently across the French and Spanish versions, that is **a material inconsistency with liability attached — not a drafting error.**

Controls:
1. **Lock the source document** before translation begins. No parallel edits.
2. **Centralized term base** shared across every language pair and every surface (app, listing, docs, white paper).
3. **Qualified legal linguists** per language pair — not the general UI translation vendor.
4. **Version-lock**: every translation records the exact source version hash it derives from. A source change invalidates every downstream translation until re-reviewed.
5. **Change log** per language, reviewable by counsel.
6. Apply the same **XBRL tagging** across versions so regulators see structurally identical documents.

## Machine translation policy
**Public/free NMT endpoints are not acceptable for regulated content** — they create a governance gap you cannot defend in an audit, and some free tiers retain content in a shared translation memory. Regulated documents go through a controlled workflow with named human reviewers and a retained audit trail.

AI-assisted drafting is fine as a first pass **inside** that controlled workflow, with human legal review before publication. The distinction is provenance and auditability, not the technology.

## What counts as regulated content here
White paper · risk disclosures · terms of service · privacy policy · KYC/AML notices · fee schedules · the in-app `security` namespace · any marketing communication making a claim about returns, safety or custody.

## India
FIU-IND-registered entities must maintain documented AML/KYC procedures and user-facing notices. Where a market expects local-language disclosure, the translated version is the one the user relies on — treat it as authoritative for that user, not as a courtesy copy.

## Practical rule
If a sentence describes what happens to someone's money, who is liable, or what cannot be reversed, it does not go through the automated pipeline. It goes through the legal workflow, in every language, with a named reviewer and a recorded source version.
