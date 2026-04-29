---
name: apply repo — career intelligence system
description: GitHub repo rajaghv-dev/apply — full system map, cold-start, current state (Session 9)
type: project
---

Repo: https://github.com/rajaghv-dev/apply (public)
Local: /home/raja/apply
Git: main branch, remote = origin

**Purpose**: Job search engine + second brain + evidence engine + reputation system.
The flywheel: gap analysis → lesson plan → build project → publish content → update profile → apply.

**Cold-start (two files only)**:
```
Read sessions.md and context.md, then continue from Session 9.
```

**Current blockers** (P0):
- `profile/my-profile.yaml` — skill levels all blank → all tools run blind
- `profile/questionnaire.md` Sections A+C — target roles + geography undefined

**Code status (Session 9)**: ALL Phase 2 + Phase 3 core code complete.
- `tools/matcher.py` — skill decay (tiered last_used) + JD section detection (required 2×, preferred 1×)
- `tools/pathfinder.py` — NetworkX Dijkstra: shortest learning path from profile to any role
- `tools/narrator.py` — Claude Haiku (prompt-cached): gap narrative + why-me + recruiter message; needs ANTHROPIC_API_KEY
- `tools/job-scraper.py` — Adzuna/Reed/Remotive/Playwright → new-this-week.md + seen.txt dedup
- `requirements.txt` — pyyaml, requests, playwright, networkx, anthropic
- `.github/workflows/weekly-scraper.yml` — Monday 08:00 UTC cron; needs ADZUNA_APP_ID, ADZUNA_APP_KEY, REED_API_KEY as repo secrets

**Remaining code** (gated on profile data or design decisions):
- P3-2: Domain focus bonus in matcher (Q3 answer needed)
- P3-5: Resume cluster generation (needs my-profile.yaml filled first)

---

## Full file map (Session 9 state)

```
ARCHITECTURE.md           system design — Phase 2+3 complete, component status updated
TODO.md                   P0/P1/P2/P3 action list + done log (all Session 8+9 items ticked)
requirements.txt          pyyaml, requests, playwright, networkx, anthropic
context.md                stable background — load every session
sessions.md               per-session handoff — load every session
prompts.md                all prompts P001–P007 + reusable templates
gaps-and-improvements.md  10 gaps + 5 improvements (GAP-09, IMP-02, IMP-03 resolved)

.github/workflows/
  weekly-scraper.yml      GH Actions cron: Monday 08:00 UTC; scrape + auto-commit

profile/
  my-profile.yaml         machine-readable skills → feeds all tools [EMPTY — P0 blocker]
  skills.md               human-readable skills table [EMPTY]
  linkedin.md             LinkedIn copy + baseline metrics [EMPTY]
  domains.md              10 vertical domain deep-dives + target companies
  questionnaire.md        7-section question set (A–G) [EMPTY — P0 blocker]
  market-scan.md          JD keyword frequency + salary benchmark template [EMPTY]

ontology/
  skills-graph.yaml       45+ skill nodes, synonyms, weighted implies edges, level descriptors
  roles-graph.yaml        14 role clusters, required/preferred skills, title synonyms, bridge bonuses
  domains.yaml            10 domains, cross-domain bridge weights, 4 unique_bridges

tools/
  matcher.py              JD → match% + STRONG/PARTIAL/GAP + decay notes + section weights + role clusters
  pathfinder.py           NetworkX Dijkstra → shortest learning path from profile skills to any role
  narrator.py             Claude Haiku (prompt-cached) → gap narrative + why-me + recruiter message
  job-scraper.py          Adzuna/Reed/Remotive/Playwright → new-this-week.md + seen.txt dedup

lesson-plans/
  README.md               15-plan index with effort/priority/status
  LP-001-rag-pipeline.md  RAG fundamentals — 5 days
  LP-002-llm-agents.md    LLM agents + tool use — 5 days
  LP-003-cocotb.md        Python hardware verification — 5 days
  LP-007-legal-nlp.md     Legal NLP + contract analysis — 5 days
  LP-013-video-analytics.md Video analytics + edge CV — 7 days
  [LP-004–006, 008–012, 014–015 stubs in README, full files not yet written]

second-brain/
  README.md               system design + flywheel diagram
  knowledge-map.md        15 cross-domain bridges with content angles
  learning-log.md         protocol + resource library per domain
  insights.md             5 durable cross-domain principles
  connections.md          bridge registry (published / unpublished)

content/
  README.md               flywheel, content types ROI, 4 pillars, cadence targets
  pipeline.md             IDEA→PUBLISHED workflow + weekly schedule + quality checklists
  ideas.md                50+ content ideas (Bridge/Tutorial/Landscape/Career/Quick)
  medium.md               12 articles tracked + article template
  linkedin-posts.md       post queue + 4 templates + hashtag clusters
  youtube.md              10 videos tracked + production checklist

github-projects/
  README.md               project pipeline + index (GP-01 through GP-08)
  ideas.md                8 project specs with tech stack + done criteria

open-source/
  README.md               contributor → maintainer path
  targets.md              Tier 1 (cocotb, LangChain, OpenLane), Tier 2, Tier 3, own projects
  log.md                  contribution tracker [EMPTY]
  maintainer-roadmap.md   18-month per-project path

evidence/
  platform-tracker.md     all-platform evidence registry [EMPTY]
  projects.md             skill → proof map [one entry: this repo]

gap-analysis/
  template.md             reusable JD analysis template
  jobs/                   match-{N}pct-latest.md + narration-{N}pct-{date}.md [EMPTY — no JDs run yet]

job-sources/
  company-careers.md      50+ direct career URLs (CH, UK, EU, India)
  aggregators.md          30+ boards by region + specialist boards
  search-strategy.md      weekly routine + LinkedIn saved search templates + cold DM
  scraping.md             scraping vs API analysis + recommended free setup

job-tracker/
  applications.md         pipeline tracker [EMPTY]
  new-this-week.md        latest scraper output [auto-generated]
  seen.txt                dedup hash registry [auto-generated]

network/
  contacts.md             contact map + referral template [EMPTY]

interview/
  prep.md                 STAR bank, technical deep-dives, company research [EMPTY]

resume/
  README.md               5-cluster strategy + ATS checklist

learning/
  roadmap.md              gap → learning plan [EMPTY — feeds from gap analysis]

_memory/
  MEMORY-INDEX.md         index (this file + siblings)
  user-profile.md         who the user is
  project-apply-repo.md   THIS FILE
  session-protocol.md     cold-start + load guide
  arch-decisions.md       AD-01 through AD-12
  open-questions.md       Q1 through Q12
```
