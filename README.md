# apply — Raja GHV's Job Search Command Center

> Technologist & generalist: chip design → embedded → systems → backend → frontend → AI/ML  
> Vertical domains: AI-assisted Legal/Compliance, AI-assisted Finance  
> GitHub: [rajaghv-dev](https://github.com/rajaghv-dev)

---

## What this system does

An ontology-powered, gap-analysis-first job search system. Not a CV store. Not a job board.
A personal intelligence layer that sits between you and every job application.

1. **Skill ontology** — 45+ skill nodes with synonym normalization, weighted transfer edges, and role cluster mappings
2. **Gap analysis** — paste any JD → get match%, STRONG/PARTIAL/GAP per skill, ordered gap-close actions
3. **Partial credit matching** — knowing RTL doesn't just match "RTL" — it also implies partial credit for FPGA, timing, hardware verification
4. **Evidence tracking** — every skill linked to a public proof recruiters can verify
5. **LinkedIn optimization** — keyword strategy, headline copy, SSI improvement tracking
6. **Job discovery** — 50+ career pages + 30+ aggregators catalogued; scraper designed (build next)
7. **Application pipeline** — track every role from discovery to offer

---

## Quick start for a new Claude session

```
Read sessions.md and context.md, then continue from Session [N].
```

Two files. Full context. Minimal tokens.

---

## Key documents (read these first)

| File | What it is |
|------|-----------|
| `ARCHITECTURE.md` | Full system design, data model, processing flows, open design questions |
| `TODO.md` | Prioritized to-do list (P0 blockers → P3 future) |
| `context.md` | Stable background — who Raja is, what this system is for |
| `sessions.md` | Per-session handoff log — what was done, what's next |
| `_memory/open-questions.md` | Unresolved design questions awaiting Raja's answers |

---

## Repo structure

```
apply/
├── ARCHITECTURE.md         ← full system design (read this to understand everything)
├── TODO.md                 ← prioritized to-do list
├── context.md              ← stable background (load every session)
├── sessions.md             ← session handoff log (load every session)
├── prompts.md              ← all prompts indexed + reusable templates
├── gaps-and-improvements.md← system gap audit
│
├── profile/
│   ├── my-profile.yaml     ← machine-readable skills → feeds matcher.py  ★ FILL THIS
│   ├── skills.md           ← human-readable skills table
│   ├── linkedin.md         ← LinkedIn copy (headline, about, keywords)
│   ├── domains.md          ← vertical domain deep-dives
│   ├── questionnaire.md    ← questions to answer to unlock the system  ★ FILL THIS
│   └── market-scan.md      ← JD keyword frequency + salary benchmarks
│
├── ontology/
│   ├── skills-graph.yaml   ← 45+ skill nodes, synonyms, weighted implies edges
│   ├── roles-graph.yaml    ← 14 role clusters, required/preferred, title synonyms
│   └── domains.yaml        ← 8 domains, cross-domain bridges, unique bridges
│
├── tools/
│   └── matcher.py          ← JD text → match score + gap report
│
├── gap-analysis/
│   ├── template.md         ← reusable JD analysis template
│   └── jobs/               ← one .md file per role analyzed
│
├── job-sources/
│   ├── company-careers.md  ← direct career URLs (50+ companies, CH/UK/EU/India)
│   ├── aggregators.md      ← job boards by region
│   ├── search-strategy.md  ← weekly search routine + LinkedIn saved search templates
│   └── scraping.md         ← scraping vs API analysis + recommended free setup
│
├── evidence/
│   └── projects.md         ← skill → proof map
│
├── learning/
│   └── roadmap.md          ← gap → ordered learning plan
│
├── network/
│   └── contacts.md         ← contact map + referral outreach template
│
├── interview/
│   └── prep.md             ← STAR bank, technical deep-dives, company research
│
├── resume/
│   └── README.md           ← cluster strategy (5 role clusters) + ATS checklist
│
├── job-tracker/
│   └── applications.md     ← application pipeline tracker
│
└── _memory/                ← Claude memory (in-repo copy — nothing local-only)
    ├── MEMORY-INDEX.md
    ├── user-profile.md
    ├── project-apply-repo.md
    ├── session-protocol.md
    ├── arch-decisions.md   ← 8 architecture decisions + rationale
    └── open-questions.md   ← 8 design questions awaiting answers
```

---

## Run the matcher

```bash
pip install pyyaml
python tools/matcher.py --jd path/to/jd.txt
# or pipe:
cat jd.txt | python tools/matcher.py
```

Requires `profile/my-profile.yaml` to be filled in. See `profile/questionnaire.md`.

---

## Token-reduction load guide

| Task | Load these files |
|------|-----------------|
| Every session | `context.md` + `sessions.md` |
| Gap analysis | + `ontology/skills-graph.yaml` + `profile/my-profile.yaml` |
| LinkedIn work | + `profile/linkedin.md` + `profile/skills.md` |
| Architecture | + `ARCHITECTURE.md` |
| Planning | + `TODO.md` |
| Specific role | + `gap-analysis/jobs/[role].md` |

Never load all files at once.
