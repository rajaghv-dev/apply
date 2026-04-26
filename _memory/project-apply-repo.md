---
name: apply repo — job search command center
description: GitHub repo rajaghv-dev/apply — full system map and cold-start instructions
type: project
---

Repo: https://github.com/rajaghv-dev/apply (public)
Local: /home/raja/apply
Git: initialized, remote = origin, branch = main

**Purpose**: Systematic job search — ontology-powered gap analysis, evidence tracking,
LinkedIn optimization, automated job discovery.

**Cold-start (two files only)**:
- `context.md` — stable background about Raja and the project
- `sessions.md` — per-session handoff log; read the latest session's "Open" items

**Full file map**:
```
ARCHITECTURE.md         full system design + open questions + review questions
TODO.md                 prioritized to-do list (P0/P1/P2/P3)
context.md              stable background (load every session)
sessions.md             session handoff log (load every session)
prompts.md              all prompts indexed (P001–P003 + reusable templates)
gaps-and-improvements.md system gap audit (10 gaps, 5 improvements)

profile/
  my-profile.yaml       machine-readable skills (feeds matcher.py) — EMPTY
  skills.md             human-readable skills table — EMPTY
  linkedin.md           LinkedIn optimization copy — EMPTY
  domains.md            vertical domain deep-dives — EMPTY
  questionnaire.md      questions to fill in to unlock the system
  market-scan.md        JD keyword frequency + salary benchmarks — EMPTY

ontology/
  skills-graph.yaml     45+ skill nodes, synonyms, implies edges
  roles-graph.yaml      14 role clusters, required/preferred skills, title synonyms
  domains.yaml          8 domains, cross-domain bridge weights, unique bridges

tools/
  matcher.py            JD text → match score report (needs profile/my-profile.yaml filled)

gap-analysis/
  template.md           reusable JD analysis template
  jobs/                 one .md file per role analyzed — EMPTY

evidence/projects.md    skill → proof map (one entry: this repo)
learning/roadmap.md     gap → learning plan — EMPTY
job-tracker/
  applications.md       application pipeline tracker — EMPTY

network/contacts.md     contact map + referral outreach template — EMPTY
interview/prep.md       STAR story bank, technical deep-dives, company research — EMPTY
resume/README.md        cluster strategy (5 clusters) + ATS checklist

job-sources/
  company-careers.md    direct career URLs for 50+ companies (CH, UK, EU, India)
  aggregators.md        job boards by region
  search-strategy.md    weekly search routine + LinkedIn saved search templates
  scraping.md           scraping vs API analysis + recommended free setup

_memory/                in-repo copy of Claude memory (mirrors ~/.claude/...)
```

**Current blocker**: profile/my-profile.yaml is empty → matcher.py produces no signal.
P0 item: fill skill levels (20 min).
