# Contributing to BVT Skills

Thanks for helping. Small, focused pull requests are the easiest to review.

## Good first contributions

- **A recipe for your framework** in `plugins/bvt-multi-language/skills/bvt-multi-language/references/platform-recipes.md`.
- **A glossary for your language** based on `assets/glossary.template.csv`.
- **A fix** for a script, a typo or a wrong instruction.
- **A new skill** that fits one of the plugins.

Not sure if an idea fits? Open a [Discussion](https://github.com/bitvault-developers/bvt-skills/discussions) first.

## How the repo is laid out

```text
.claude-plugin/marketplace.json        the marketplace: lists every plugin
plugins/<plugin>/.claude-plugin/       plugin.json and icon.png
plugins/<plugin>/skills/<skill>/       SKILL.md plus references/, scripts/, assets/
dist/                                  zips for the Claude app (built, not edited)
scripts/build-zips.sh                  rebuilds dist/
```

## Rules for skills

- Each skill folder works on its own: everything it needs is inside it.
- `SKILL.md` starts with `name` and `description`. The description says what the skill does and when to use it, in one or two sentences.
- Keep `SKILL.md` short and move long material into `references/`.
- No secrets, keys, real wallet addresses or personal data in examples. Keys come from environment variables.
- Scripts must not run anything paid or destructive without asking first.

## Before you open a pull request

```bash
claude plugin validate --strict .
for p in plugins/*; do claude plugin validate --strict "$p"; done
sh scripts/build-zips.sh
```

If you changed a script, run it once on a small sample and say what you ran in the pull request.

## License

By contributing you agree that your work is released under the [MIT License](LICENSE).
