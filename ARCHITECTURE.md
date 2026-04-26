# System Architecture

**apply** — Career Intelligence & Second Brain System  
Last updated: 2026-04-26

---

## 1. Purpose & Problem Statement

Standard job search is a flat, manual process:
- You write a generic CV
- You paste it into 50 portals
- You get keyword-rejected by ATS before a human sees it
- You don't know which skill gaps matter most
- You can't measure LinkedIn improvement

This system replaces that with a **knowledge-graph-backed, ontology-powered matching
pipeline** that:

1. Knows your skills with depth, recency, and evidence — not just a keyword list
2. Extracts requirements from any JD and scores your fit with partial credit for adjacent skills
3. Generates prioritized gap-close actions and learning paths
4. Tracks evidence artifacts that prove skills to recruiters
5. Optimizes LinkedIn as an inbound channel, not just a CV store
6. Aggregates and filters job feeds from 50+ sources down to roles worth your time

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL DATA SOURCES                            │
│                                                                         │
│  Job Boards          Company Careers       LinkedIn         GitHub      │
│  (Adzuna, Indeed,    (Synopsys, Cadence,   (profile,        (evidence,  │
│   Reed, Naukri,       ARM, Google, etc.)    SSI, InMail)     projects)  │
│   jobs.ch, ...)                                                         │
└──────────┬──────────────────┬───────────────────┬───────────┬──────────┘
           │                  │                   │           │
           ▼                  ▼                   ▼           ▼
┌──────────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐
│  INGESTION LAYER │  │  JD STORE    │  │  LINKEDIN    │  │  EVIDENCE  │
│                  │  │              │  │  LAYER       │  │  LAYER     │
│ tools/           │  │ gap-analysis │  │              │  │            │
│ job-scraper.py   │  │ /jobs/*.md   │  │ profile/     │  │ evidence/  │
│ (planned)        │  │              │  │ linkedin.md  │  │ projects.md│
│                  │  │ job-tracker/ │  │              │  │            │
│ Adzuna API       │  │ new-this-    │  │ profile/     │  │ resume/    │
│ Indeed API       │  │ week.md      │  │ market-scan  │  │ *.pdf      │
│ Reed API         │  │              │  │ .md          │  │            │
│ Playwright       │  │              │  │              │  │            │
└──────────────────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘
                             │                  │                │
                             ▼                  │                │
┌────────────────────────────────────────────┐  │                │
│              ONTOLOGY LAYER                │  │                │
│                                            │  │                │
│  ontology/skills-graph.yaml                │  │                │
│  ┌─────────────────────────────────────┐   │  │                │
│  │  SkillNode                          │   │  │                │
│  │  ├── id, label                      │   │  │                │
│  │  ├── synonyms[]      (normalization)│   │  │                │
│  │  ├── domain          (clustering)   │   │  │                │
│  │  ├── level_descriptors              │   │  │                │
│  │  └── implies{skill_id: weight}      │   │  │                │
│  └─────────────────────────────────────┘   │  │                │
│                                            │  │                │
│  ontology/roles-graph.yaml                 │  │                │
│  ┌─────────────────────────────────────┐   │  │                │
│  │  RoleNode                           │   │  │                │
│  │  ├── id, label, title_synonyms[]    │   │  │                │
│  │  ├── required{skill_id: level}      │   │  │                │
│  │  ├── preferred{skill_id: level}     │   │  │                │
│  │  ├── domain_clusters[]              │   │  │                │
│  │  └── bridge_score_bonus             │   │  │                │
│  └─────────────────────────────────────┘   │  │                │
│                                            │  │                │
│  ontology/domains.yaml                     │  │                │
│  ┌─────────────────────────────────────┐   │  │                │
│  │  DomainNode                         │   │  │                │
│  │  ├── id, label, skills[]            │   │  │                │
│  │  ├── bridges_to{domain: weight}     │   │  │                │
│  │  └── unique_bridges[]               │   │  │                │
│  └─────────────────────────────────────┘   │  │                │
│                                            │  │                │
└────────────────────┬───────────────────────┘  │                │
                     │                          │                │
                     ▼                          │                │
┌────────────────────────────────────────────┐  │                │
│               PROFILE LAYER                │  │                │
│                                            │  │                │
│  profile/my-profile.yaml (machine)         │  │                │
│  ┌─────────────────────────────────────┐   │  │                │
│  │  ProfileSkill                       │   │  │                │
│  │  ├── skill_id → ontology node       │   │  │                │
│  │  ├── level (EXPERT/PROFICIENT/...)  │   │  │                │
│  │  ├── last_used (year)               │   │  │                │
│  │  └── evidence (url or text)         │   │  │                │
│  └─────────────────────────────────────┘   │  │                │
│                                            │  │                │
│  profile/skills.md (human-readable)        │  │                │
│  profile/domains.md (vertical deep-dives)  │  │                │
└────────────────────┬───────────────────────┘  │                │
                     │                          │                │
                     ▼                          ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          MATCHING ENGINE                                │
│                       tools/matcher.py                                  │
│                                                                         │
│  Input:  JD text (any format) + profile/my-profile.yaml                 │
│                                                                         │
│  Step 1: JD PARSING                                                     │
│    regex synonym scan → {skill_id: found}                               │
│    (planned: LLM extraction for required vs. preferred, seniority)      │
│                                                                         │
│  Step 2: SCORING per JD skill S                                         │
│    direct_score  = LEVEL_SCORE[profile[S].level]        # 0–3          │
│    implied_score = max over all T in profile:                           │
│                     LEVEL_SCORE[profile[T].level]                      │
│                     × skills_graph[T].implies.get(S, 0)                │
│    final_score   = max(direct_score, implied_score)                    │
│                                                                         │
│  Step 3: CLASSIFICATION                                                 │
│    STRONG  → final_score ≥ 2.5                                         │
│    PARTIAL → final_score 1.2–2.4                                       │
│    GAP     → final_score < 1.2                                         │
│                                                                         │
│  Step 4: MATCH %                                                        │
│    Σ final_score / Σ max_possible × 100                                │
│    Apply ≥ 60% | Stretch 40–59% | Skip < 40%                          │
│                                                                         │
│  Step 5: ROLE CLUSTER SUGGESTION                                        │
│    JD skill set ∩ roles-graph required/preferred → top 3 clusters      │
│                                                                         │
│  Output:  terminal report + gap-analysis/jobs/match-{N}pct-latest.md   │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
│  GAP LAYER      │  │  TRACKER LAYER   │  │  NETWORK LAYER  │
│                 │  │                  │  │                 │
│ learning/       │  │ job-tracker/     │  │ network/        │
│ roadmap.md      │  │ applications.md  │  │ contacts.md     │
│                 │  │ offers.md        │  │                 │
│ gap-analysis/   │  │                  │  │ interview/      │
│ jobs/*.md       │  │                  │  │ prep.md         │
└─────────────────┘  └──────────────────┘  └─────────────────┘
           │                   │                   │
           └───────────────────┴───────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         OUTPUT LAYER                                    │
│                                                                         │
│  LinkedIn          Resume              GitHub              Outreach     │
│  (headline,        (cluster PDFs,      (evidence repos,    (DMs, cold   │
│   about, posts,     ATS-optimized)      READMEs, demos)     emails)     │
│   SSI improvement)                                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Model

### 3.1 Skill Node (ontology/skills-graph.yaml)

```yaml
skill_id:
  label: str                        # canonical display name
  synonyms: list[str]               # all JD terms that map to this node
  domain: str                       # which domain cluster owns this skill
  level_descriptors:
    EXPERT: str                     # what EXPERT looks like in practice
    PROFICIENT: str
    FAMILIAR: str
  implies:
    other_skill_id: float           # 0.0–1.0 transfer weight
  required_by: list[str]            # role IDs that need this skill
```

**Key design choice**: `implies` is a directed weighted edge. `A implies B: 0.7`
means knowing A gives you 70% of B — but NOT vice versa. This models the
real asymmetry of skill transfer: RTL implies FPGA knowledge, but FPGA alone
does not imply full RTL capability.

### 3.2 Profile Skill (profile/my-profile.yaml)

```yaml
skill_id:
  level: EXPERT | PROFICIENT | FAMILIAR | (empty)
  last_used: int                    # year
  evidence: str                     # URL or free text
```

Mapped 1-to-1 to ontology skill IDs. Empty level = treated as 0 in scoring.

**Known limitation**: `last_used` is recorded but not yet used in scoring.
A skill used in 2015 should decay. See Section 6 — Open Design Questions.

### 3.3 Role Node (ontology/roles-graph.yaml)

```yaml
role_id:
  label: str
  seniority: list[str]
  title_synonyms: list[str]         # all titles that mean this role
  required: {skill_id: level}       # must-have
  preferred: {skill_id: level}      # nice-to-have (lower weight in scoring)
  domain_clusters: list[str]
  bridge_score_bonus: float         # added to match% for rare cross-domain combos
  target_companies: list[str]
  geographies: list[str]
```

### 3.4 Domain Node (ontology/domains.yaml)

```yaml
domain_id:
  label: str
  skills: list[str]
  bridges_to:
    other_domain_id: float          # 0.0–1.0 domain-level transfer weight
```

`bridges_to` is a higher-level layer above skill-level implies edges.
Used for: detecting which domains a JD belongs to, and surfacing
role clusters that Raja's domain combination unlocks.

### 3.5 JD (gap-analysis/jobs/*.md)

Currently: Markdown files authored by Claude after gap analysis.
Planned: structured YAML front-matter + free text body.

```markdown
---
company: str
role_title: str
date: YYYY-MM-DD
source_url: str
match_pct: float
status: RESEARCH | READY | APPLIED | SCREENING | INTERVIEW | OFFER | REJECTED
---
[gap table + why-me bullets]
```

### 3.6 Application (job-tracker/applications.md)

Currently a Markdown table. Planned upgrade: YAML rows that matcher.py
can read to generate weekly pipeline health reports.

---

## 4. Processing Flows

### Flow 1: JD → Match Score (implemented)

```
1. User runs: python tools/matcher.py --jd jd.txt
2. Load ontology (skills-graph.yaml, roles-graph.yaml)
3. Load profile (my-profile.yaml)
4. JD PARSING:
   - For each skill node in ontology:
     - Check if any synonym appears in JD text (word boundary regex)
     - If yes: add skill_id to jd_skills
5. SCORING:
   - For each jd_skill:
     a. direct_score = LEVEL_SCORE[profile[jd_skill].level]
     b. implied_score = max over all profile skills T:
          LEVEL_SCORE[profile[T].level] × skills_graph[T].implies.get(jd_skill, 0)
     c. final_score = max(direct_score, implied_score)
6. CLASSIFICATION:
   - STRONG / PARTIAL / GAP per threshold
7. MATCH %:
   - Σ final / Σ max × 100
8. OUTPUT:
   - Terminal report
   - gap-analysis/jobs/match-{N}pct-latest.md
```

### Flow 2: Weekly Job Discovery (planned — tools/job-scraper.py)

```
1. Cron triggers weekly
2. Adzuna API → filter by keyword list + location list
3. Indeed API  → same filters
4. Reed API    → UK-only
5. Playwright  → scrape 10 target company career pages
6. Deduplicate by (company, title) hash
7. For each new role:
   a. Run Flow 1 (matcher) silently
   b. If match_pct ≥ 60: add to job-tracker/new-this-week.md (APPLY tier)
   c. If 40–59%:          add to new-this-week.md (STRETCH tier)
   d. Else: discard
8. Append to job-tracker/applications.md with status=RESEARCH
```

### Flow 3: LinkedIn Optimization (manual + Claude-assisted)

```
1. User fills: profile/linkedin.md (current headline, about, URL)
2. User pulls:  SSI score, profile views, InMails (5 min manual)
3. User runs: Claude session with:
   "Read context.md, sessions.md, profile/linkedin.md, profile/skills.md.
    Optimize my LinkedIn headline and about for [target role]."
4. Claude outputs: optimized headline variants, about section, keyword list
5. User applies on LinkedIn, records SSI after 2 weeks in market-scan.md
6. Repeat monthly — track SSI trend
```

### Flow 4: Gap → Learn → Prove (manual)

```
1. Matcher identifies GAP skill S
2. User checks learning/roadmap.md for existing entry for S
3. If not there: Claude session →
   "Skill gap: [S]. Suggest fastest credibility path + evidence artifact."
4. Claude writes entry to learning/roadmap.md
5. User completes learning artifact (project, course, contribution)
6. User updates:
   - profile/my-profile.yaml: level + evidence URL for S
   - evidence/projects.md: new row for the artifact
   - profile/skills.md: level updated
7. Re-run matcher on same JD → verify score improved
```

### Flow 5: Network → Referral (manual)

```
1. Find target role via Flow 1 or 2
2. Check network/contacts.md for warm contacts at that company
3. If warm: send referral request (template in contacts.md)
4. If cold: engage on LinkedIn 2–3 times, then DM
5. Log outreach in contacts.md outreach log
6. If referral confirmed: apply via company ATS + note referral name
7. Update job-tracker/applications.md: status → APPLIED (referred)
```

---

## 5. Ontology Graph: Key Properties

### 5.1 The implies graph is a DAG (directed acyclic graph)

No cycles: RTL → FPGA → [nothing back to RTL].
This keeps scoring deterministic — no circular credit loops.

### 5.2 Implied score is capped by the source skill's level

If you have RTL at FAMILIAR (score 1) and it implies FPGA at 0.55,
your implied FPGA score = 1 × 0.55 = 0.55.

If you have RTL at EXPERT (score 3), implied FPGA = 3 × 0.55 = 1.65 (PARTIAL).

This correctly models that expert-level adjacent knowledge gives more credit
than beginner-level adjacent knowledge.

### 5.3 Domain bridges are a separate, higher-level layer

Skill-level implies: RTL → FPGA (skill-to-skill)
Domain-level bridge: hardware → embedded: 0.70 (domain-to-domain)

Domain bridges are used for:
- Detecting which role cluster a JD belongs to
- Surfacing non-obvious role matches ("you're in hardware domain → check AI hardware roles")
- NOT used in the match% score (score uses skill-level implies only)

### 5.4 Unique bridges in domains.yaml

These are the rare cross-domain combinations that produce a bridge_score_bonus
in roles-graph.yaml. Raja's 4 identified bridges:

| Bridge | Rarity | Bonus |
|--------|--------|-------|
| hardware × AI | VERY_RARE | +15% |
| hardware × AI × systems | EXTREMELY_RARE | (to be quantified) |
| AI × legal_tech | RARE | +20% |
| AI × fintech | RARE | +15% |

Bonus is added to match% only when both domains are represented in the profile
at PROFICIENT or above. Rewards genuine cross-domain depth, not superficial exposure.

---

## 6. Open Design Questions (for review)

These are architectural decisions not yet resolved. Each one is a design choice
with tradeoffs — review and decide before building Phase 2.

### Q1. Should last_used decay the skill score?

**Current**: `last_used` is recorded but ignored in scoring.

**Option A — Hard cutoff**: Skills not used in 5+ years → cap at FAMILIAR regardless of level.
- Pro: realistic. RTL from 2015 isn't EXPERT today.
- Con: may undervalue durable conceptual knowledge.

**Option B — Decay function**: `effective_score = level_score × decay(years_since_used)`
- `decay(y) = 1.0 if y ≤ 2, 0.8 if y ≤ 5, 0.6 if y ≤ 10, 0.4 if y > 10`
- Pro: continuous, more nuanced.
- Con: adds complexity; decay rate is a parameter to tune.

**Option C — No decay**: Trust the user to self-assess accurately.
- Pro: simple.
- Con: user may overstate stale skills; recruiters will probe in interviews.

**Recommendation**: Option B with a note in the gap report: "RTL claimed EXPERT, last used 2019 → effective score 1.8 (decay applied). Consider a refresh project."

---

### Q2. Required vs. preferred in JD — should they be weighted differently?

**Current**: All JD skills extracted as a flat list. No distinction between
"Required: 5+ years Python" and "Nice to have: exposure to Go".

**Option A — Binary extraction (current)**: All skills equal weight.
- Pro: simple. Works for quick screening.
- Con: a GAP on a "nice to have" skill drives match% down just as much as a GAP on a "required" skill.

**Option B — LLM-powered JD parsing**: Send JD to Claude API.
Ask: "Extract required vs. preferred skills, and flag minimum years of experience per skill."
Return structured JSON → feed into matcher.
- Pro: much more accurate. Handles complex JD language.
- Con: API cost (~$0.01/JD), adds LLM dependency, slower.

**Option C — Heuristic section detection**: Regex for "Required:", "Must have:",
"Nice to have:", "Preferred:" headers → weight required skills 1.5×.
- Pro: no API cost, faster than LLM.
- Con: JD formatting is inconsistent; many JDs don't use these headers.

**Recommendation**: Option C as a quick improvement now; Option B when running the scraper at scale (50+ JDs/week). Cost at $0.01/JD × 50/week = $0.50/week — trivial.

---

### Q3. Single profile or per-role-cluster profiles?

**Current**: One `my-profile.yaml`. All skills, all levels, one truth.

**Problem**: For a chip design role, you want to emphasize hardware EXPERT skills.
For an AI role, you want to emphasize LLM/agents. The same skill set
reads differently depending on which narrative you're telling.

**Option A — Single profile + role-specific narrative generation**:
Profile is source of truth. Claude generates the narrative angle per role cluster.
- Pro: one file to maintain; no inconsistency risk.
- Con: matcher doesn't know which skills to emphasize.

**Option B — Per-cluster profile overlays**:
`my-profile.yaml` = base. `my-profile-hardware.yaml` = override with hardware skills foregrounded.
- Pro: matcher can load the right overlay per JD cluster.
- Con: duplication; can get out of sync.

**Option C — Weight multipliers per cluster**:
`roles-graph.yaml` already has `domain_clusters`. Add a scoring multiplier:
"if this role is in hardware cluster, multiply hardware skill scores by 1.2".
- Pro: single profile, cluster-aware scoring. No duplication.
- Con: slightly more complex scoring logic.

**Recommendation**: Option C. Implement `focus_bonus: {domain: multiplier}` in roles-graph.yaml.

---

### Q4. Should the ontology be static YAML or a graph database?

**Current**: Static YAML files loaded into memory per run. No persistence.

**Option A — Stay YAML (current)**:
- Pro: human-readable, Claude-readable, Git-versioned, zero infra.
- Con: no graph traversal queries, no multi-hop inference (A→B→C).
  Currently only 1-hop implies edges are used.

**Option B — Neo4j or similar graph DB**:
- Pro: Cypher queries enable multi-hop ("which roles are reachable from my skills in ≤ 2 hops?"), efficient traversal, persistent state.
- Con: infra overhead, not human-readable, not Claude-readable without tooling.

**Option C — NetworkX in-memory graph (Python)**:
Load YAML → build NetworkX DiGraph → run BFS/DFS for multi-hop paths.
No external infra. Pure Python.
- Pro: enables multi-hop inference, shortest path to a role, gap bridging chains.
- Con: skills graph rebuilt from YAML every run (fast enough for this scale).

**Recommendation**: Option C for Phase 2. The YAML stays as source of truth and human interface. NetworkX gives you graph algorithms without infra. Example: `shortest_path(current_skills, target_role_required_skills)` → ordered learning plan.

---

### Q5. Where does Claude fit in the pipeline?

**Current**: Claude is the operator. It reads files, writes files, runs analysis in chat.
The matcher.py script is the only automated component.

**Option A — Claude as conversational operator (current)**:
Human pastes JD into chat → Claude reads context.md + skills.md + ontology → writes analysis.
- Pro: maximum intelligence, handles ambiguity, writes narrative.
- Con: requires human to be present; not automated; each session costs tokens.

**Option B — Claude API in the pipeline**:
job-scraper.py calls Claude API for: JD parsing (required vs. preferred), gap narrative, "why me" bullets, LinkedIn post generation.
- Pro: automated, consistent, high quality.
- Con: API cost ($0.01–0.05 per JD depending on model); requires API key in env.

**Option C — Hybrid**: Automated pipeline uses regex matcher (free, fast) for screening.
Only roles that pass the 60% threshold get sent to Claude API for narrative generation.
- Pro: cost-efficient; only spend API budget on roles worth applying to.
- Con: regex matcher may miss some nuance in screening.

**Recommendation**: Option C. Keeps cost low (typically 5–10 roles pass the 60% threshold per week), maximizes quality where it matters.

---

### Q6. How to handle the LinkedIn SSI optimization loop?

LinkedIn's SSI score is a proxy for recruiter visibility. The factors:
1. Professional brand (profile completeness, content posting)
2. Finding the right people (connection quality)
3. Engaging with insights (commenting, sharing)
4. Building relationships (InMail response rate)

**What's missing from the current system**:
- No tracking of which LinkedIn posts got engagement
- No A/B testing of headline variants
- No correlation between SSI changes and recruiter InMail volume
- No automation of the posting cadence

**Proposed addition**: `linkedin/analytics-log.md` — weekly record of SSI, profile views,
InMails, post impressions. After 8 weeks you have a correlation signal.

---

## 7. Component Status

| Component | Status | Location | Completeness |
|-----------|--------|----------|-------------|
| Ontology — Skills Graph | Built | ontology/skills-graph.yaml | ~70% (add more AI/legal/fintech skills) |
| Ontology — Roles Graph | Built | ontology/roles-graph.yaml | ~80% |
| Ontology — Domains | Built | ontology/domains.yaml | ~90% |
| Matching Engine | Built | tools/matcher.py | ~60% (no decay, no required/preferred split) |
| Profile (machine) | Stub | profile/my-profile.yaml | 0% — needs user data |
| Profile (human) | Stub | profile/skills.md | 0% — needs user data |
| JD Store | Empty | gap-analysis/jobs/ | 0% — no real JDs analyzed yet |
| Job Scraper | Designed | job-sources/scraping.md | 0% — not built |
| LinkedIn Layer | Stub | profile/linkedin.md | 0% — needs user data |
| Market Scan | Stub | profile/market-scan.md | 0% — no JDs scanned |
| Evidence Map | Stub | evidence/projects.md | 5% — one entry (this repo) |
| Network Contacts | Stub | network/contacts.md | 0% — needs user data |
| Interview Prep | Stub | interview/prep.md | 0% — needs STAR stories |
| Resume Clusters | Planned | resume/ | 0% — no CVs yet |
| Learning Roadmap | Stub | learning/roadmap.md | 0% — no gaps identified yet |
| Job Tracker | Stub | job-tracker/applications.md | 0% — no applications yet |

**Critical path to first application**:
`my-profile.yaml` → `matcher.py` on a real JD → gap-analysis/jobs/[role].md → apply

---

## 8. File Dependency Map

```
context.md ←── read every session (stable background)
sessions.md ←── read every session (handoff state)

profile/my-profile.yaml
  ├── feeds → tools/matcher.py (scoring)
  ├── syncs with → profile/skills.md (human-readable view)
  └── drives → profile/linkedin.md (narrative)

ontology/skills-graph.yaml
  ├── feeds → tools/matcher.py (synonym lookup + implies edges)
  └── cross-refs → ontology/roles-graph.yaml (required_by)

ontology/roles-graph.yaml
  ├── feeds → tools/matcher.py (role cluster suggestion)
  └── cross-refs → ontology/domains.yaml (domain_clusters)

tools/matcher.py
  ├── reads → profile/my-profile.yaml
  ├── reads → ontology/skills-graph.yaml
  ├── reads → ontology/roles-graph.yaml
  └── writes → gap-analysis/jobs/match-{N}pct-latest.md

gap-analysis/jobs/*.md
  ├── drives → learning/roadmap.md (gap actions)
  ├── drives → evidence/projects.md (evidence gaps)
  └── drives → job-tracker/applications.md (application pipeline)

learning/roadmap.md
  └── completion → updates profile/my-profile.yaml + evidence/projects.md

evidence/projects.md
  ├── publishes to → GitHub (repos)
  └── publishes to → LinkedIn (posts, featured section)
```

---

## 9. Phase Plan

### Phase 1 — Foundation (current)
- [x] Repo structure
- [x] Ontology (skills + roles + domains)
- [x] Matcher script (basic)
- [x] Job source catalog
- [ ] Profile data (BLOCKER)

### Phase 2 — Automation
- [ ] Job scraper (Adzuna + Indeed APIs + Playwright)
- [ ] Weekly cron + digest file
- [ ] LLM JD parsing (required vs. preferred split)
- [ ] Skill decay in scoring
- [ ] LinkedIn analytics log

### Phase 3 — Intelligence
- [ ] NetworkX graph → multi-hop inference, shortest learning path
- [ ] Role cluster auto-detection from JD (not just synonym match)
- [ ] Claude API in pipeline (gap narrative + why-me bullets, automated)
- [ ] Resume auto-generation per role cluster from profile YAML

### Phase 4 — Scale
- [ ] ESCO ontology integration (map Raja's skills to EU standard)
- [ ] Salary intelligence auto-pull (Glassdoor/Levels.fyi)
- [ ] LinkedIn SSI correlation dashboard
- [ ] Offer comparison model

---

## 10. Technology Choices — Rationale

| Choice | Rationale |
|--------|-----------|
| YAML for ontology | Human-readable, Claude-readable, Git-diffable. No DB needed at this scale. |
| Markdown for all docs | Renders on GitHub; readable in any editor; Claude can read and write natively. |
| Python for tooling | Best ecosystem for NLP, YAML, Playwright, API clients. |
| Regex synonym matching | Zero cost, zero latency, zero dependency. Sufficient for Phase 1. |
| Git for all state | Full audit trail; sync across machines; GitHub renders it all. |
| No database | The data volume (one person's job search) does not justify a DB. Files are the DB. |
| Claude as operator | Maximum reasoning quality for gap analysis and narrative. Not replaceable by code. |

---

## 11. What This System Is Not

- Not an ATS (applicant tracking system) — it's a pre-ATS intelligence layer
- Not a resume builder (it feeds inputs to a resume; it doesn't generate PDFs)
- Not a recruiter-side tool — it's entirely candidate-side
- Not a job board — it aggregates and filters, does not host listings
- Not a production service — it's a personal tool; reliability > uptime

---

## Review Questions for Raja

1. **Decay (Q1)**: Should stale skills decay in the match score? Which decay model fits how you think about your own currency in each domain?

2. **JD parsing (Q2)**: Is regex synonym matching good enough for screening, or do you want LLM extraction from day one? (Cost: ~$0.50/week at 50 JDs)

3. **Profile clusters (Q3)**: Single profile or per-role-cluster overlays? The Option C weight multiplier is the cleanest approach — does that feel right?

4. **Graph traversal (Q4)**: Worth adding NetworkX for multi-hop paths? The main payoff is "shortest learning path to role X" — is that useful to you?

5. **Claude in pipeline (Q5)**: Hybrid approach (regex screens, Claude narrates for passed roles) — or do you want to stay fully manual (chat-based) for now?

6. **Missing domains**: Are there skill domains I've missed entirely? Any specific technologies or verticals not covered in skills-graph.yaml?

7. **Role clusters**: Are the 14 role clusters in roles-graph.yaml the right set? Any missing (e.g., Developer Relations, Solutions Architect, Technical Program Manager)?

8. **Geography**: The system covers CH, UK, Germany, Netherlands, India. Any others? (France, Singapore, UAE, US with sponsorship?)
