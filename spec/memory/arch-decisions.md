---
name: Architecture Decisions Log
description: Key design decisions made with rationale — prevents re-debating settled questions
type: project
---

## AD-01 | YAML for ontology (not a graph DB)
**Decision**: Skill graph stored as YAML files (skills-graph.yaml, roles-graph.yaml, domains.yaml).
**Why**: Human-readable, Claude-readable, Git-diffable. No infra. NetworkX layers on top if needed.
**Status**: DECIDED. Revisit only if skills graph > 500 nodes.

## AD-02 | Markdown for all documents
**Decision**: Every doc is a .md file in Git. No Notion, Confluence, Google Docs.
**Why**: Renders on GitHub. Claude reads and writes natively. Zero external dependency.
**Status**: DECIDED.

## AD-03 | Single profile, not per-cluster overlays
**Decision**: One `profile/my-profile.yaml` as source of truth.
Per-cluster emphasis via `FOCUS_BONUS = 1.15` multiplier in matcher.py on direct_score for skills whose domain matches the top detected role cluster.
**Why**: Avoids duplication and drift. One file to maintain.
**Status**: DECIDED + IMPLEMENTED (Session 11). `get_focus_domains()` in matcher.py detects top role cluster from JD skills, applies ×1.15 to direct scores in that domain.

## AD-04 | Regex synonym matching for JD parsing (Phase 1)
**Decision**: JD parsed via word-boundary regex against skills-graph.yaml synonyms.
**Why**: Zero cost, zero latency, zero dependency. Sufficient for Phase 1 manual workflow.
**When to upgrade**: 50+ JDs/week via scraper → heuristic section detection (Option C) first, then LLM.
**Status**: DECIDED for Phase 1.

## AD-05 | Git is the only storage layer
**Decision**: No database. Files are the database. All state in repo.
**Why**: Full audit trail, sync across machines, GitHub renders everything.
**Status**: DECIDED. User explicitly requested all state in Git.

## AD-06 | Claude is the reasoning engine, not just a writer
**Decision**: Claude reads ontology + profile + JD → gap analysis, narrative, "why me" bullets.
matcher.py handles arithmetic scoring. Claude handles judgment and narrative.
**Why**: Gap analysis requires judgment about which gaps matter and how to frame them.
**Status**: DECIDED.

## AD-07 | Apply threshold = 60%, Stretch = 40–59%, Skip < 40%
**Decision**: Match% thresholds for application decisions.
**Why**: 60% = core JD requirements covered via direct + implied skills.
**Status**: DECIDED. Calibrate after first 10 JDs (may need adjustment).

## AD-08 | Nothing left on local machine only
**Decision**: All Claude memory, session state, context → Git repo.
`_memory/` in repo mirrors `~/.claude/projects/.../memory/`
**Why**: User explicitly requested. Machines are ephemeral; Git is permanent.
**Status**: DECIDED (Session 5).

## AD-09 | Lesson plans as primary driver of evidence production
**Decision**: Don't build projects ad hoc. Every project flows from a lesson plan.
Lesson plan → build artifact → update profile/my-profile.yaml → log in evidence/platform-tracker.md.
**Why**: Without a structured plan, learning is unfocused and artifacts are shallow.
Lesson plans have explicit done criteria (can be marked DONE with confidence).
**Status**: DECIDED (Session 6).

## AD-10 | Second brain integrated into the job search loop
**Decision**: `second-brain/` is not a separate system — it feeds the job search engine.
Learning log → content ideas → GitHub projects → evidence → profile update → match score improvement.
**Why**: Continuous skill development and job search reinforce each other via the flywheel.
**Status**: DECIDED (Session 6).

## AD-11 | 10 vertical domains, not 3
**Decision**: Domains expanded from 3 (legal, fintech, hardware) to 10.
Added: AI Hardware, Video Analytics/CCTV, Industrial AI, Embedded AI/TinyML, Autonomous Systems, Telecom, Healthcare AI.
**Why**: The generalist breadth enables targeting more role clusters. Video analytics + industrial AI
are large deployed markets that combine hardware + AI — rare cross.
**Status**: DECIDED (Session 6). Depth of experience per domain TBD — user to fill questionnaire.

## AD-12 | Content channels prioritized: LinkedIn first, Medium second, YouTube third
**Decision**: Post order of operations: LinkedIn (2-3×/week, 30 min each) → Medium (2×/month, 3 hrs) → YouTube (1×/month, 6 hrs).
**Why**: LinkedIn has the shortest feedback loop to recruiter visibility. Medium has SEO. YouTube has the highest trust signal but highest production cost.
**Status**: DECIDED (Session 6). Adjust after measuring SSI response.

## AD-13 | Test suite as regression guard
**Decision**: All tool functions are covered by pytest tests in `tests/`. Run `pytest tests/ -q` before any future tool changes.
**Why**: 11 tools interact (matcher feeds narrator, pathfinder reads roles-graph). Tests prevent regressions when patching one tool from breaking another.
**Status**: DECIDED (Session 11). 81 tests, 100% passing at merge.
