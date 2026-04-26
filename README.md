# apply — Raja GHV's Job Search Command Center

> Technologist & generalist: chip design → embedded → systems → backend → frontend → AI/ML  
> Vertical domains: AI-assisted Legal/Compliance, AI-assisted Finance

## What this repo does

1. **Gap analysis** — paste any JD, get a skill-by-skill gap map with evidence requirements
2. **Evidence tracking** — map every skill to a public proof recruiters can verify
3. **Learning roadmap** — prioritized plan to close gaps fast
4. **LinkedIn optimization** — keyword strategy, headline copy, engagement playbook
5. **Application pipeline** — track every role from research to offer

## Quick start for a new Claude session

```
Read sessions.md and context.md, then continue from the last open session.
```

That's it. Two files. Full context. Minimal tokens.

## Repo structure

```
apply/
├── context.md              ← stable background (read every session)
├── sessions.md             ← per-session handoff log (read every session)
├── prompts.md              ← all prompts, indexed and reusable
├── README.md               ← this file
├── profile/
│   ├── skills.md           ← full skills inventory
│   ├── linkedin.md         ← LinkedIn optimization copy
│   └── domains.md          ← vertical domain deep-dives
├── gap-analysis/
│   ├── template.md         ← reusable JD gap analysis template
│   └── jobs/               ← one file per role analyzed
├── evidence/
│   └── projects.md         ← skill → proof map
├── learning/
│   └── roadmap.md          ← gap → learning plan
└── job-tracker/
    └── applications.md     ← application pipeline
```

## Token-reduction protocol

| What to load | When |
|-------------|------|
| `context.md` + `sessions.md` | Every session, always |
| `profile/skills.md` | When doing gap analysis or LinkedIn work |
| `gap-analysis/jobs/[file]` | When working on a specific role |
| `evidence/projects.md` | When building or mapping evidence |
| `learning/roadmap.md` | When planning skill development |

Do NOT load all files at once — load only what the current task needs.
