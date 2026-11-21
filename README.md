# BVT Skills

Free skills and plugins for Claude, made by the [BitVault](https://bitvault.club) team.

| Plugin | What it does |
|---|---|
| **[bvt-multi-language](plugins/bvt-multi-language)** | Adds a language switcher and a full multilingual system to any website or app (React, Next.js, Vue, Svelte, Angular, Flutter, FlutterFlow, React Native, Android, iOS, Electron, Tauri, WordPress), translates it into as many languages as possible, and checks quality before release. Comes with 7 ready scripts. |
| **[bvt-save-token](plugins/bvt-save-token)** | Makes your Claude usage last longer: short replies, diff-only code, handoff notes for fresh chats, and an audit of what to switch off. |
| **[bvt-crypto-architecture](plugins/bvt-crypto-architecture)** | Two architecture playbooks: a centralized crypto exchange (ledger first, single-writer matching engine, safe build order) and a self-custody wallet (seed phrase, encrypted storage, 2FA, send flow) for web, mobile and browser extensions. |

## Install

### Claude Code

```text
/plugin marketplace add bitvault-developers/bvt-skills
/plugin install bvt-multi-language@bvt-skills
/plugin install bvt-save-token@bvt-skills
/plugin install bvt-crypto-architecture@bvt-skills
```

Install only the ones you need. Update later with `/plugin marketplace update bvt-skills`.

### Claude app (web, desktop, mobile)

1. Download the zip for the skill you want from the [`dist`](dist) folder:
   `bvt-multi-language.zip`, `bvt-save-token.zip`, `bvtex-exchange-architecture.zip`, `bvtwallet-architecture.zip`.
2. In Claude's settings, go to where you add skills and upload the zip.
3. Start a new chat. Claude uses the skill on its own when your request matches it.

### Other AI coding agents

Each skill is a plain folder with a `SKILL.md` file (the open Agent Skills format). Copy the folder from `plugins/<plugin>/skills/` into your agent's skills folder.

## Good to know

- **Nothing runs by itself.** The scripts in bvt-multi-language run only when you or Claude run them, and every paid translation run prints a cost estimate and waits for a yes.
- **Your keys stay yours.** Translation API keys are read from environment variables, never written into code or files.
- **Guidance, not a guarantee.** The architecture playbooks are engineering guidance. They are not a security audit and not legal advice: have a real exchange or wallet audited, and check the law in every country you serve.

## Contributing

Issues and pull requests are welcome. Keep each skill self-contained, keep secrets out of examples, and run `claude plugin validate .` before you open a pull request. To rebuild the zips in `dist/`, run `sh scripts/build-zips.sh`.

## Security

Found a security problem? Email support@bitvault.club instead of opening a public issue.

## License

[MIT](LICENSE) © 2026 BitVault Founding Team. Not affiliated with or endorsed by Anthropic. Claude is a trademark of Anthropic.
