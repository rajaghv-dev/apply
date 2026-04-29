# Context — apply

## Identity
- **GitHub**: rajaghv-dev | **Email**: rajaghv.dev@gmail.com
- **Stack depth**: RTL/VLSI → embedded firmware → OS/systems → backend → frontend → ML/AI
- **Thesis**: "From transistor to transformer" — the principles don't change, the substrate does
- **Mode**: Active job search + continuous skill development + reputation building

## Vertical Domains (10)
| Domain | Status | Key differentiator |
|--------|--------|-------------------|
| Chip Design / Silicon / EDA | [TO-FILL depth] | RTL, VLSI, DFT, SoC — rare in AI era |
| AI Hardware / ML Accelerators | [TO-FILL depth] | Can speak RTL and LLM in same sentence |
| Embedded / Firmware | [TO-FILL depth] | RTOS, drivers, bring-up |
| AI-Assisted Legal / Compliance | [TO-FILL depth] | Legal domain + LLM engineering |
| AI-Assisted Finance / FinTech | [TO-FILL depth] | Finance domain + ML/agents |
| Video Analytics / Computer Vision | [TO-FILL depth] | Edge deployment + hardware intuition |
| Industrial AI / Smart Manufacturing | [TO-FILL depth] | OT/IT bridge, hardware safety mindset |
| Embedded AI / TinyML | [TO-FILL depth] | MCU + inference, full on-device stack |
| Autonomous Systems / Robotics | [TO-FILL depth] | Embedded + RTOS + perception |
| Systems / Cloud / Backend | [TO-FILL depth] | OS internals, distributed systems |

## Job Search Goals
- Target levels: Senior IC, Staff, Principal — open to Tech Lead / Architect
- Geographies: Switzerland, UK, Germany, Netherlands, India, Remote-EU
- Format: gap analysis per JD → lesson plan → evidence artifact → apply

## System Purpose
This repo is simultaneously:
1. **Job search engine** — ontology-powered JD matching, gap analysis, application tracking
2. **Second brain** — captures learning, insights, cross-domain connections
3. **Evidence engine** — produces GitHub repos, Medium articles, LinkedIn posts, YouTube videos, open-source contributions
4. **Reputation system** — content flywheel → LinkedIn inbound → recruiter calls

## Flywheel
```
Gap analysis → Lesson plan → Build project → Write about it → Publish → Update profile → Apply
      ↑                                                                              |
      └──────────────────────── New JD reveals new gap ─────────────────────────────┘
```

## Session Cold-Start
```
Read sessions.md and context.md, then continue from Session [N].
```
That's all. Two files. Load more only as the task needs.

## File Map (abbreviated — full tree in README.md)
```
apply/
├── ARCHITECTURE.md     full system design (read before making structural changes)
├── TODO.md             prioritized action list (P0 blockers first)
├── requirements.txt    pyyaml, requests, playwright, networkx, anthropic, matplotlib, pytest
├── context.md          THIS FILE — stable background
├── sessions.md         per-session handoff (what was done, what's next)
├── prompts.md          all prompts indexed (P001–P007 + reusable templates)
│
├── .github/workflows/
│   └── weekly-scraper.yml   Monday 08:00 UTC cron — scrape + auto-commit
│
├── profile/            skills, LinkedIn copy, domain deep-dives, questionnaire
├── ontology/           skills graph, roles graph, domains — the matching engine's brain
├── tools/              11 tools — all complete, 81 tests passing
│   ├── matcher.py      JD → match% + decay + section detection + domain focus bonus
│   ├── pathfinder.py   NetworkX Dijkstra → shortest learning path to any role
│   ├── narrator.py     Claude Haiku (prompt-cached) → gap narrative + recruiter msg
│   ├── job-scraper.py  Adzuna/Reed/Remotive/Playwright → new-this-week.md
│   ├── log-linkedin.py append weekly SSI/views/inmails snapshot
│   ├── ssi-dashboard.py  matplotlib 2×2 LinkedIn trend chart → PNG
│   ├── resume-gen.py   cluster-specific resume stubs from profile YAML
│   ├── market-scan.py  batch JD skill frequency → profile/market-scan.md
│   ├── esco-map.py     map skills to EU ESCO standard URIs
│   ├── salary-pull.py  2025 salary benchmarks + optional LinkedIn scrape
│   └── offer-compare.py  total comp + CoL-adjusted comparison table
├── tests/              pytest suite — 81 tests, 100% passing
│
├── lesson-plans/       15 structured learning modules (objectives → resources → artifact → done)
├── second-brain/       knowledge map, learning log, insights, cross-domain connections
├── content/            content engine (ideas, pipeline, Medium, LinkedIn, YouTube)
├── github-projects/    8 planned projects with full specs
├── open-source/        contribution strategy, targets, maintainer roadmap, log
├── evidence/           platform tracker, projects map
│
├── gap-analysis/       JD analysis template + per-role files + narration outputs
├── job-sources/        company careers, aggregators, search strategy, scraping
├── job-tracker/        applications pipeline, new-this-week.md, seen.txt
├── network/            contacts, referral outreach
├── interview/          STAR bank, technical prep, company research
├── resume/             cluster strategy, ATS checklist
├── learning/           roadmap (feeds from gap analysis)
│
└── _memory/            Claude memory (in-repo — nothing local-only)
```

## Current Blockers (P0)
1. `profile/my-profile.yaml` — all skill levels blank → matcher/pathfinder/narrator all run blind
2. `profile/questionnaire.md` Sections A+C — target roles and geography not defined

## What's fully built and ready to use
**All code complete — 11 tools, 81 tests, 100% passing. Zero remaining code items.**

- **Core pipeline**: `matcher.py --jd <file>` → `pathfinder.py --role <id>` → `narrator.py`
- **Job discovery**: `job-scraper.py` (Adzuna/Reed/Remotive/Playwright) + GH Actions weekly cron
- **LinkedIn loop**: `log-linkedin.py` → `ssi-dashboard.py` (weekly snapshot + chart)
- **Resume**: `resume-gen.py` → cluster-specific stubs per role (14 clusters)
- **Market intel**: `market-scan.py` (batch JD freq) + `salary-pull.py` (2025 benchmarks)
- **Decisions**: `offer-compare.py` (total comp + CoL-adjusted) + `esco-map.py` (EU ESCO URIs)
- Ontology: 45+ skill nodes, 14 role clusters, 10 domains, weighted implies edges
- Job sources: 50+ company career pages, 30+ aggregators, search strategy
- 5 lesson plans (LP-001 RAG, LP-002 Agents, LP-003 cocotb, LP-007 Legal NLP, LP-013 Video)
- 8 GitHub project specs (GP-01 through GP-08)
- Content engine: 50+ ideas, templates, trackers for Medium/LinkedIn/YouTube
- Open source: Tier 1/2/3 targets, maintainer roadmap, contribution log
- Second brain: 15 cross-domain bridges, learning log, 5 durable principles
