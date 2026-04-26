# apply

> Chip design → embedded → systems → backend → frontend → AI/ML  
> Domains: Legal AI · Finance AI · Silicon/EDA · AI Hardware · Video Analytics · Industrial AI · TinyML  
> Second brain · evidence engine · job search intelligence

---

## What this is

A personal career operating system — not a CV store, not a job board.
Three systems in one, all connected:

| System | What it does | Key files |
|--------|-------------|-----------|
| **Job search engine** | Ontology-powered JD matching, gap analysis, application pipeline | `ontology/`, `tools/matcher.py`, `gap-analysis/`, `job-tracker/` |
| **Second brain** | Captures learning, cross-domain bridges, insights | `second-brain/`, `lesson-plans/`, `learning/` |
| **Evidence engine** | Produces GitHub repos, articles, videos, OS contributions | `content/`, `github-projects/`, `open-source/`, `evidence/` |

**The flywheel**:
```
Gap analysis → Lesson plan → Build project → Publish content → Update profile → Apply
      ↑                                                                         |
      └─────────────────── New JD reveals new gap ─────────────────────────────┘
```

---

## Start a new Claude session

```
Read sessions.md and context.md, then continue from Session 7.
```

Two files. Full context. Load more only as the task needs.

---

## Current state (Session 7 — 2026-04-26)

**Fully built and usable:**
- Ontology: 45+ skill nodes, 14 role clusters, 10 domains, weighted bridge edges
- Matcher: `python tools/matcher.py --jd file.txt` (needs profile filled first)
- Job sources: 50+ company career pages, 30+ aggregators, search strategy, scraping guide
- 5 lesson plans: LP-001 (RAG), LP-002 (Agents), LP-003 (cocotb), LP-007 (Legal NLP), LP-013 (Video Analytics)
- 8 GitHub project specs: GP-01 through GP-08
- Content engine: 50+ ideas, 4 post templates, Medium/YouTube/LinkedIn trackers
- Open source: Tier 1/2/3 targets, maintainer roadmap, contribution log
- Second brain: 15 cross-domain bridges, learning log, 5 durable principles

**Blocked on (P0):**
- `profile/my-profile.yaml` — skill levels empty → matcher blind
- `profile/questionnaire.md` Sections A+C — target roles + geography undefined

---

## Full file tree

```
apply/
│
├── ARCHITECTURE.md           ← system design (read before structural changes)
├── TODO.md                   ← prioritized action list (P0 first)
├── context.md                ← stable background — load every session
├── sessions.md               ← session handoff log — load every session
├── prompts.md                ← all prompts P001–P007 + reusable templates
├── gaps-and-improvements.md  ← system gap audit (10 gaps, 5 improvements)
│
├── profile/                  ← FILL THESE — all empty stubs
│   ├── my-profile.yaml       ← machine-readable skills (feeds matcher) ★ P0 BLOCKER
│   ├── skills.md             ← human-readable skills table
│   ├── linkedin.md           ← LinkedIn copy + baseline metrics
│   ├── domains.md            ← 10 vertical domains with targets + evidence slots
│   ├── questionnaire.md      ← 7-section question set (A–G) ★ P0 BLOCKER (A+C)
│   └── market-scan.md        ← JD keyword frequency + salary benchmarks
│
├── ontology/                 ← the matching engine's knowledge base
│   ├── skills-graph.yaml     ← 45+ skill nodes, synonyms, weighted implies edges
│   ├── roles-graph.yaml      ← 14 role clusters, title synonyms, bridge bonuses
│   └── domains.yaml          ← 10 domains, bridge weights, 4 unique bridge combos
│
├── tools/
│   └── matcher.py            ← JD text → match% + STRONG/PARTIAL/GAP report
│
├── lesson-plans/             ← structured learning modules (daily schedule → artifact → done)
│   ├── README.md             ← 15-plan index with effort/priority/status
│   ├── LP-001-rag-pipeline.md
│   ├── LP-002-llm-agents.md
│   ├── LP-003-cocotb.md
│   ├── LP-007-legal-nlp.md
│   └── LP-013-video-analytics.md
│
├── second-brain/             ← knowledge capture + cross-domain bridges
│   ├── README.md             ← system design + flywheel
│   ├── knowledge-map.md      ← 15 documented cross-domain bridges
│   ├── learning-log.md       ← timestamped learning entries + resource library
│   ├── insights.md           ← 5 durable cross-domain principles
│   └── connections.md        ← bridge registry (used / unpublished)
│
├── content/                  ← content creation engine
│   ├── README.md             ← flywheel, ROI table, 4 pillars, cadence
│   ├── pipeline.md           ← IDEA→PUBLISHED workflow + weekly schedule
│   ├── ideas.md              ← 50+ ideas (Bridge/Tutorial/Landscape/Career/Quick)
│   ├── medium.md             ← 12 articles tracked + template
│   ├── linkedin-posts.md     ← post queue + 4 templates + hashtag clusters
│   └── youtube.md            ← 10 videos tracked + production checklist
│
├── github-projects/          ← planned evidence repos
│   ├── README.md             ← pipeline + index (GP-01 through GP-09)
│   └── ideas.md              ← 8 project specs with tech stack + done criteria
│
├── open-source/              ← contribution strategy
│   ├── README.md             ← contributor → maintainer path
│   ├── targets.md            ← Tier 1/2/3 projects with entry points
│   ├── log.md                ← contribution tracker
│   └── maintainer-roadmap.md ← 18-month per-project path
│
├── evidence/
│   ├── platform-tracker.md   ← all-platform evidence registry
│   └── projects.md           ← skill → proof map
│
├── gap-analysis/
│   ├── template.md           ← reusable JD analysis template
│   └── jobs/                 ← one .md per role analyzed
│
├── job-sources/
│   ├── company-careers.md    ← 50+ direct career URLs (CH, UK, EU, India)
│   ├── aggregators.md        ← 30+ boards by region + specialist boards
│   ├── search-strategy.md    ← weekly routine + LinkedIn search templates + cold DM
│   └── scraping.md           ← scraping vs API, costs, recommended free setup
│
├── job-tracker/
│   └── applications.md       ← pipeline tracker
│
├── network/
│   └── contacts.md           ← contact map + referral template
│
├── interview/
│   └── prep.md               ← STAR bank + technical deep-dives + company research
│
├── resume/
│   └── README.md             ← 5-cluster strategy + ATS checklist
│
├── learning/
│   └── roadmap.md            ← gap → learning plan (feeds from gap analysis)
│
└── _memory/                  ← Claude memory (in-repo — nothing local-only)
    ├── MEMORY-INDEX.md
    ├── user-profile.md
    ├── project-apply-repo.md
    ├── session-protocol.md
    ├── arch-decisions.md     ← AD-01 through AD-12
    └── open-questions.md     ← Q1 through Q12
```

---

## Run the matcher

```bash
pip install pyyaml
python tools/matcher.py --jd path/to/jd.txt
# or pipe:
cat jd.txt | python tools/matcher.py
```

Requires `profile/my-profile.yaml` filled. See `profile/questionnaire.md`.

---

## Token-reduction load guide

| Task | Load these files |
|------|-----------------|
| Every session (always) | `context.md` + `sessions.md` |
| Gap analysis | + `ontology/skills-graph.yaml` + `profile/my-profile.yaml` |
| LinkedIn work | + `profile/linkedin.md` + `profile/skills.md` |
| Lesson plan execution | + `lesson-plans/LP-NNN-*.md` |
| Content creation | + `content/ideas.md` + `content/pipeline.md` |
| Open source work | + `open-source/targets.md` + `open-source/log.md` |
| Architecture decisions | + `ARCHITECTURE.md` + `_memory/arch-decisions.md` |
| Planning | + `TODO.md` + `_memory/open-questions.md` |
| Specific role | + `gap-analysis/jobs/[role].md` |

Never load all files at once.
