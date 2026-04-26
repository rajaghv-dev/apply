---
name: Session cold-start protocol
description: How to minimize token usage — what to load, what to update, end-of-session ritual
type: feedback
---

## Cold-start ritual (paste at top of every new session)
```
Read sessions.md and context.md, then continue from Session [N].
```
Two files = full context. Load nothing else until the task demands it.

## What to load per task type
| Task | Files to load |
|------|--------------|
| Any session | context.md + sessions.md (always) |
| Run gap analysis | + ontology/skills-graph.yaml + profile/my-profile.yaml |
| LinkedIn work | + profile/linkedin.md + profile/skills.md |
| Lesson plan work | + lesson-plans/LP-NNN-*.md |
| Content creation | + content/ideas.md + content/pipeline.md |
| Open source | + open-source/targets.md + open-source/log.md |
| Architecture decisions | + ARCHITECTURE.md + _memory/arch-decisions.md |
| Planning / TODO | + TODO.md + _memory/open-questions.md |
| Specific role | + gap-analysis/jobs/[role].md |
| Evidence mapping | + evidence/platform-tracker.md + evidence/projects.md |

**Rule**: Load only what the current task needs. Never load all files at once.

## End-of-session ritual (do before closing)
1. `sessions.md` — add new session entry: goal / done / open / key decisions
2. `TODO.md` — tick done items, add new items discovered
3. `prompts.md` — log new prompts as P00N
4. `_memory/` — update any stale memory files (especially project-apply-repo.md)
5. `_memory/arch-decisions.md` — add entry if a design decision was made
6. `context.md` — update if something in "Current Blockers" or "What's fully built" changed
7. Commit + push

## Memory vs. session file distinction
- **context.md**: stable facts about identity, system purpose, what's built. Update rarely.
- **sessions.md**: ephemeral per-session log. Update every session.
- **_memory/**: Claude's persistent knowledge. Update when decisions are made or profile changes.
- **TODO.md**: current action list. Update every session.

## Token budget guidance
- sessions.md + context.md ≈ 1,500–2,000 tokens (always worth loading)
- Each additional file ≈ 500–3,000 tokens (load selectively)
- Never load: ontology YAML files (large), full ideas.md, full ARCHITECTURE.md unless specifically needed
