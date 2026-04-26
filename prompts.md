# Prompts Index

All prompts used with Claude in this project, indexed for reuse and audit.

---

## P001 — 2026-04-26 | Repo Bootstrap

**Prompt**:
> make a repo n update my github; for searching and applying for jobs, to identify whats the gap between my skills profile, and job requirements, how to improve or learn the skill, and produce enough evidences to convince the recruiters, i have knowledge and experience from chip design to apps as u know, and some vertical domains like ai assisted domains like legal/compliance and finance, im a technologist, and generalist, i can connect my linked in and provide other details, want to win in my linkedin ratings, and get a call, etc, add all my prompts in prompts.md and your discussions n context in context.md, update my repo

**Context**: First session. No prior state. GitHub: rajaghv-dev.

**Output**: Full repo scaffolded and pushed to GitHub.

---

## P002 — 2026-04-26 | Session/Memory Design

**Prompt**:
> have memory and sessions md file so that you can later start n different sessions, n reduce token consumption, add all thats necessary to reduce token consumption

**Output**: sessions.md created with handoff protocol; context.md scoped to stable facts only; token-reduction instructions added to sessions.md.

---

## P004 — 2026-04-26 | Ontology Strategy

**Prompt**:
> do u think ontology can help here? then whats the strategy n usefulness?

**Output**: ontology/README.md (strategy + 6 use cases + 3-phase plan), skills-graph.yaml (45+ nodes), roles-graph.yaml (14 clusters), domains.yaml (8 domains + unique bridges), tools/matcher.py (JD scorer), profile/my-profile.yaml (stub).

---

## P005 — 2026-04-26 | Architecture Document

**Prompt**:
> add to the context of this repo in enough detail n for me to review, and come up with arch

**Output**: ARCHITECTURE.md — 11 sections covering system overview, ASCII component diagram, data model, 5 processing flows, ontology graph properties, 6 open design questions with options + recommendations, component status table, file dependency map, 4-phase build plan, tech rationale, 8 review questions.

---

## P006 — 2026-04-26 | Priority TODO + Repo Consolidation

**Prompt**:
> come up with the priority to do list now, and update session n memory md files in the repo accordingly, make all these files as part of the repo, dont leave anything to local machine.

**Output**: TODO.md (P0/P1/P2/P3 tiers + done list), _memory/ directory in repo (user-profile, project-apply-repo, session-protocol, arch-decisions, open-questions), README.md fully updated with all new files.

---

## Gap Analysis Prompt Template

Paste this at the start of a gap analysis session:

```
Read sessions.md and context.md.
Here is a JD I want to analyze:

[PASTE JD HERE]

1. Map each requirement to my skills in profile/skills.md — mark: STRONG / PARTIAL / GAP
2. For each GAP, suggest the fastest path to credibility (course, project, open-source contribution)
3. For each PARTIAL, identify what evidence artifact would upgrade it to STRONG
4. Draft a 3-bullet "why me" tailored to this JD
5. Save output to gap-analysis/jobs/[company]-[role].md and update sessions.md
```

## LinkedIn Optimization Prompt Template

```
Read context.md and profile/linkedin.md.
Current headline: [PASTE]
Target role: [PASTE]
Optimize:
1. Headline (120 chars, keyword-rich, human-readable)
2. About section (first 3 lines visible before "see more" — must hook)
3. Top 5 skills to pin
4. Featured section strategy
Save to profile/linkedin.md
```

## P003 — 2026-04-26 | Job Scraping / API Strategy

**Prompt**:
> to scrap or thru api calls to identify as a recruiter, and its costs, but i want to apply for jobs

**Context**: User wants to automate job discovery — scraping vs. official APIs, understand costs, goal is to surface relevant roles and apply.

**Output**: See `job-sources/scraping.md` for full analysis of scraping vs. API options, costs, and recommended approach.

---

## Evidence Generation Prompt Template

```
Read context.md and evidence/projects.md.
Skill gap: [SKILL]
Generate:
1. A minimal project idea that demonstrates this skill in <1 week
2. How to frame it on LinkedIn and GitHub for recruiter impact
3. Keywords to embed in the README for ATS/search
Save to evidence/projects.md
```
