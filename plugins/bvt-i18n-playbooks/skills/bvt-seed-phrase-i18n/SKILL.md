---
name: bvt-seed-phrase-i18n
description: Governs language handling for BIP-39 seed phrases in BitVault wallets. Use when implementing wallet creation, mnemonic generation, seed import or recovery in a localized app, or when anyone proposes offering the recovery phrase in a language other than English.
---

# Seed Phrase Localization — the hard rule

## Generate English wordlist mnemonics only. Always.

BIP-39 defines wordlists in ten languages (English, Japanese, Korean, Chinese Simplified, Chinese Traditional, Spanish, French, Italian, Czech, Portuguese), and the specification **strongly discourages using any of them except English**, because the vast majority of BIP-39 wallets support English only.

## Why this is a fund-loss issue, not a preference
A mnemonic is tied to the wordlist that generated it — the same words map to different indices in different languages. A phrase generated from the Spanish wordlist **cannot be recovered in a wallet that only knows English**, and the user will not discover this until they try to restore, possibly years later, possibly after losing the device.

Worse: multi-language implementations that accept mixed input can silently derive a **different wallet** from a phrase containing one substituted word, with no error. The funds are not lost — they are in a wallet nobody knows the address of.

## What to do instead
**Localize the instructions, never the words.**
- All surrounding copy — "Write these 12 words down", "Never share them", the verification prompts, error messages — is fully translated.
- The 12 words themselves render in English, in Latin script, in every locale including Hindi, Arabic and Japanese.
- Add a locale-appropriate explanation of *why* the words are English: they are a technical standard, not English text, and they must be recorded exactly as shown.

## Import
- Validate against the **English wordlist only**.
- If a submitted word matches a non-English BIP-39 wordlist, do not "helpfully" accept it. Show a specific message: this phrase was created in another language and BitVault supports English recovery phrases only. Do not attempt a conversion.
- Normalise input (trim, collapse whitespace, lowercase, NFKD) before validation, but never transliterate.

## Rendering in RTL locales
The word list is LTR content inside a possibly-RTL layout. Wrap it in bidi isolation and force `direction: ltr` on the container, or the numbering and word order display scrambled (see `bvt-rtl-layout`). A seed phrase shown in the wrong order is a support catastrophe.

## Also do not localize
Derivation paths, keystore JSON field names, or any error string that a user might paste into another wallet for diagnosis.

## If someone asks for localized wordlists
The answer is no, and the reason is interoperability, not effort. Record the request and move on.
