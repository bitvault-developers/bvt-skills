# BVT Skill Loaders

43 small skills that load popular open-source skill packs on demand. Each loader fetches one upstream project **at a fixed commit that was reviewed before publishing**, then hands over to that project's own SKILL.md. Nothing is copied from the upstream projects: each one keeps its own licence, and these loaders are unofficial and not affiliated with them.

Why loaders instead of copies: you always get the project's real instructions, the version is pinned (no surprise updates), and the skill list Claude keeps in context stays small.

| Skill | Loads | Pinned | What it does |
|---|---|---|---|
| `agent-reach` | [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | `c70ae6d` | Read-only access to Reddit, X, YouTube subtitles, GitHub, LinkedIn jobs and more via one CLI on the user's computer. |
| `api-anything` | [goodnight000/api-anything](https://github.com/goodnight000/api-anything) | `9641e54` | Get data from a website through its own underlying requests instead of a browser: a shared catalog of ~114 sites (Reddit, YouTube, GitHub, Google… |
| `automation-recommender` | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | `0412be7` | Analyze a codebase and recommend automations: hooks, subagents, skills, plugins and MCP servers. |
| `blender` | [EL4CTEO/blender-skills](https://github.com/EL4CTEO/blender-skills) | `389f28a` | Real 3D with Blender, run headless: modeling, PBR materials, lighting, Cycles photoreal renders, animation, geometry nodes, simulations, VFX… |
| `cli-anything` | [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) | `34f5195` | CLI-Anything (HKUDS): give it any software's GitHub repo and it builds a command-line tool an AI agent can drive, plus ready-made CLIs for 79 apps… |
| `composio` | [ComposioHQ/skills](https://github.com/ComposioHQ/skills) | `c4b2700` | Composio's official skill: use 1000+ apps (Gmail, Slack, GitHub, Notion, Sheets…) through Composio, or build agents and apps with its SDK,… |
| `day-trader` | [Jakeschincariol/day-trader-skill](https://github.com/Jakeschincariol/day-trader-skill) | `3d0f4ef` | 11 day-trading skills (stock analysis, scanner, news, risk sizing, entry/exit timing, alerts, congressional-trade tracker, broker order executor). |
| `diagram-design` | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | `0cf73c3` | Create editorial technical diagrams as HTML/SVG/PNG: architecture, flowchart, sequence, state, ER/schema, timeline, swimlane, org chart, Sankey,… |
| `earshot` | [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot) | `4ac3d2a` | Add real, licensed sound to code-made videos and animations: cue lists, SFX/foley/ambience, music edited to picture, a deterministic mixer,… |
| `ecc` | [affaan-m/ECC](https://github.com/affaan-m/ECC) | `4adeee6` | 328 skills and 72 specialist agent playbooks for coding, security, testing, research, content and ops. |
| `expo` | [expo/skills](https://github.com/expo/skills) | `a9e5bd3` | Expo's official skills for Expo and React Native apps: Expo Router, native UI, data fetching, upgrades, EAS Build, EAS Update, app store… |
| `firebase` | [firebase/agent-skills](https://github.com/firebase/agent-skills) | `b76be96` | Firebase's official skills: Firestore, Auth, security rules (writing and auditing), Remote Config, Analytics, App Hosting, Data Connect, Cloud… |
| `firecrawl` | [firecrawl/skills](https://github.com/firecrawl/skills) | `1d4b072` | Firecrawl's official 37 skills: scrape, search, crawl, map, monitor, research and workflows (SEO audit, competitor intel, lead gen, site clone). |
| `gamedev` | [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | `c6ca6c4` | Godot, Unity, Unreal, Roblox, three.js, Phaser and more. |
| `gsap` | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | `aed9cfd` | GreenSock's official GSAP skills: core tweens, timelines, ScrollTrigger scroll animations, plugins, React and framework use, and performance. |
| `gstack` | [garrytan/gstack](https://github.com/garrytan/gstack) | `306ff23` | Garry Tan's 70+ skills for planning, CEO/eng/design plan reviews, code review, QA, shipping, retros, docs and design. |
| `hallmark` | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | `4f6a46c` | Design skill for new websites and pages that look designed, not AI-generated. |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) | `0ef9fe5` | Rewrite AI-sounding text so it reads like a person wrote it, without changing what it says. |
| `hyperframes` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | `be67089` | HeyGen's HyperFrames: write HTML, render frame-exact video. |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `e89e3ad` | Design, critique, audit, polish or improve a frontend interface (sites, dashboards, app UI, forms, iOS/Android screens): hierarchy, layout, type,… |
| `langchain` | [langchain-ai/langchain-skills](https://github.com/langchain-ai/langchain-skills) | `126c384` | LangChain's official skills for building AI agents: LangChain and LangGraph fundamentals, RAG, middleware, persistence and memory, Deep Agents,… |
| `last30days` | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | `6894d44` | Research what people are saying about any topic in the last 30 days across Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub and the… |
| `openverse-sounds` | [Openverse API](https://api.openverse.org) (WordPress/openverse) | — | Search Openverse (WordPress/openverse) for free Creative Commons sound effects and music, with license and credit for each. |
| `openzeppelin` | [OpenZeppelin/openzeppelin-skills](https://github.com/OpenZeppelin/openzeppelin-skills) | `584262a` | OpenZeppelin's official skills for secure smart contracts: set up Solidity projects with OpenZeppelin Contracts, write secure contracts, and plan… |
| `opuscar` | [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | `3a7132b` | Lemo-Opuscar (the OPUSCAR 98 reel): 99 code-made film styles. |
| `playwright-browser` | [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) | `dd47a6a` | Browser automation with Playwright: test websites and web apps, fill forms, log in, take screenshots, check responsive layouts and links, and… |
| `ponytail` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `ebd8654` | Lazy senior dev mode, the smallest change that fully solves the task, plus review, audit, debt and gain skills. |
| `posthog` | [PostHog/skills](https://github.com/PostHog/skills) | `7dcf60c` | PostHog's official skills (350+): product analytics, funnels, session replays, error tracking, feature flags, experiments, dashboards and adding… |
| `rea-video` | [JuneYaooo/rea-video](https://github.com/JuneYaooo/rea-video) | `78160e0` | Reverse-engineer any video shot by shot (filmed, AI, 3D, animation or code), its sound, captions and edit, and plan the remake. |
| `react-native-callstack` | [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills) | `59e9d17` | Callstack's React Native skills: performance best practices, React Navigation, upgrading React Native, testing, brownfield migration, libraries… |
| `real-sfx` | [Clipwing/skills](https://github.com/Clipwing/skills) | `edbefcb` | Clipwing real-sfx: sound-design motion videos with real recorded sound effects placed on the exact frame, keeping music and voice. |
| `reanimate` | [NiazMorshed2007/reanimate](https://github.com/NiazMorshed2007/reanimate) | `3f7a55a` | Copy an animation from a website, screen recording, mp4, gif or Lottie into your code, then film both and compare until they match. |
| `reverse-engineer-anything` | [morluto/rea](https://github.com/morluto/rea) | `144843c` | Reverse engineer shipped apps and binaries with REA: native, Electron/JavaScript, Android, packaged, firmware and browser targets. |
| `scrapling` | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | `95cf901` | Web scraping with the Scrapling Python library: fetch pages, parse with adaptive selectors, run sessions and spiders for research data. |
| `skill-library` | 7 public collections (see SKILL.md) | `9ef0c3c` | On-demand library of about 780 skills (engineering, DevOps, product, executive advisors, finance, stock and crypto trading, web3/DeFi/NFT,… |
| `strix` | [usestrix/strix](https://github.com/usestrix/strix) | `a1ccf77` | Find, prove and fix security holes in web apps, APIs and code you own. |
| `task-observer` | [rebelytics/one-skill-to-rule-them-all](https://github.com/rebelytics/one-skill-to-rule-them-all) | `046b8f2` | Notes user corrections, judgement calls and repeated workflows during multi-step work, then turns them into skill improvements or new-skill ideas. |
| `threejs` | [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) | `0e18186` | Three.js skills: scene fundamentals, React Three Fiber, geometry, materials, textures, lighting, shaders, animation, loaders, interaction,… |
| `threejs-graphics` | [scottstts/Threejs-Awesome-Graphics-Agent-Skills](https://github.com/scottstts/Threejs-Awesome-Graphics-Agent-Skills) | `53eb5a2` | High-end Three.js visuals: bloom, shadows, ambient occlusion, colour grading, water, clouds, atmosphere, procedural materials, terrain,… |
| `trailofbits-security` | [trailofbits/skills](https://github.com/trailofbits/skills) | `e4dd0bb` | Trail of Bits security skills: smart contract and token integration review, audit prep, code maturity, secure workflows, Semgrep/CodeQL, fuzzing,… |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `3a13158` | UI/UX design intelligence for web, mobile and desktop: styles, palettes, font pairings, UX rules, charts and stack-specific guidance. |
| `vercel-react` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | `1a2c79d` | Vercel's official skills: React and Next.js performance best practices, component composition patterns, view transitions, web design and writing… |
| `watch-video` | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) | `03ceb42` | Let Claude watch a video from a URL or local file: downloads it, extracts frames, pulls the transcript, and answers questions about what's in it. |

`openverse-sounds` is our own skill: it searches the free Openverse audio API for Creative Commons sounds and gives the licence and credit line for each.

## Install

```text
/plugin install bvt-skill-loaders --marketplace bitvault-developers/bvt-skills
```

Or, in your terminal:

```bash
claude plugin install bvt-skill-loaders --marketplace bitvault-developers/bvt-skills
```

For the Claude app, download single skills as zips from the [latest release](https://github.com/bitvault-developers/bvt-skills/releases/latest) or the [`dist`](../../dist) folder and upload them where you add skills in Claude's settings.

## How a loader works

1. It runs a short `git` sparse fetch of the pinned commit into `~/.skill-src/<name>` (once per session).
2. It finds the right upstream skill and tells Claude to read and follow it.
3. It never switches to a newer upstream version unless you ask, and stops if the fetch fails.

Needs `git` and network access to GitHub. Some upstream projects need their own tools or accounts (API keys for Firecrawl, PostHog or Composio, Blender as a Python module, Playwright browsers); the loaders say when and ask before installing anything.

## Important

Each upstream project is its owner's work under its own licence; check it before commercial use. Pinned commits were reviewed when added; review again before you change a pin.
