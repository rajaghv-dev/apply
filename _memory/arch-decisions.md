---
name: Architecture Decisions Log
description: Key design decisions made, with rationale — so future sessions don't re-debate settled questions
type: project
---

## AD-01 | YAML for ontology (not a graph DB)
**Decision**: Skill graph stored as YAML files, not Neo4j or SQLite.
**Why**: Human-readable, Claude-readable, Git-diffable. Data volume (one person's job search) doesn't justify a DB. NetworkX can be layered on top of YAML if graph traversal is needed.
**Status**: DECIDED. Revisit only if skills graph > 500 nodes.

## AD-02 | Markdown for all docs (not Notion, Confluence, etc.)
**Decision**: Every document is a .md file in Git.
**Why**: Renders on GitHub. Claude reads and writes it natively. No external dependency.
**Status**: DECIDED.

## AD-03 | Single profile, not per-cluster overlays
**Decision**: One `profile/my-profile.yaml` as source of truth.
Per-cluster emphasis handled via `focus_bonus` multipliers in roles-graph.yaml (to implement).
**Why**: Avoids duplication and drift. One file to maintain.
**Status**: DECIDED (Option C from ARCHITECTURE.md Q3). focus_bonus not yet implemented.

## AD-04 | Regex synonym matching for JD parsing (Phase 1)
**Decision**: JD parsed via regex word-boundary synonym lookup against skills-graph.yaml.
**Why**: Zero cost, zero latency, zero dependency. Sufficient for Phase 1 manual workflow.
**When to upgrade**: When scraper runs 50+ JDs/week → LLM parsing for required/preferred split.
**Status**: DECIDED for Phase 1. Phase 2: implement heuristic section detection first (Q2 Option C), then LLM if needed.

## AD-05 | Git is the only storage layer
**Decision**: No database. Files are the database.
**Why**: Full audit trail, sync across machines, GitHub renders all content.
All state lives in repo — nothing on local machine only.
**Status**: DECIDED. User explicitly requested this.

## AD-06 | Claude is the reasoning engine, not just a writer
**Decision**: Claude reads ontology + profile + JD and produces gap analysis, narrative, "why me" bullets.
Code (matcher.py) handles scoring. Claude handles reasoning and narrative.
**Why**: Gap analysis requires judgment about which gaps matter, not just arithmetic.
**Status**: DECIDED.

## AD-07 | Apply threshold = 60%, Stretch = 40–59%, Skip < 40%
**Decision**: Match% thresholds for application decisions.
**Why**: 60% is the point where direct + implied skills cover the core JD requirements.
Below 40% means too many hard gaps to close quickly.
**Status**: DECIDED. Thresholds are tunable once we have data (calibrate after first 10 JDs).

## AD-08 | Nothing left on local machine only
**Decision**: All Claude memory, all context, all session state lives in the Git repo.
_memory/ directory in repo mirrors ~/.claude/projects/.../memory/
**Why**: User explicitly requested. Machines are ephemeral; Git is permanent.
**Status**: DECIDED (Session 5, 2026-04-26).
