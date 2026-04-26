---
name: Session cold-start protocol
description: How to minimize token usage across sessions — what to load, how to hand off
type: feedback
---

User explicitly wants minimal token consumption across sessions.

**Why**: Raja runs multiple Claude sessions. Replaying full conversation history is wasteful.
Two files give full context. Everything else is loaded on demand.

**Cold-start ritual (paste at top of every new session)**:
```
Read sessions.md and context.md, then continue from Session [N].
```

**What to load per task**:
| Task | Files to load |
|------|--------------|
| Any session | context.md + sessions.md (always) |
| Gap analysis | + ontology/skills-graph.yaml + profile/my-profile.yaml |
| LinkedIn work | + profile/linkedin.md + profile/skills.md |
| Architecture work | + ARCHITECTURE.md |
| Specific role | + gap-analysis/jobs/[role].md |
| Evidence/learning | + evidence/projects.md + learning/roadmap.md |
| TODO/planning | + TODO.md |

**Do NOT load all files at once.** Load only what the current task needs.

**End-of-session ritual**:
1. Update sessions.md: add new session entry (goal / done / open / key decisions)
2. Update TODO.md: tick off completed items, add new ones discovered
3. Update prompts.md: log the session's new prompts as P00N
4. Commit and push all changes

**Memory update rule**:
If a design decision is made that changes the architecture, update:
- ARCHITECTURE.md (canonical)
- _memory/arch-decisions.md (log entry)
- sessions.md (key decisions section of that session)
