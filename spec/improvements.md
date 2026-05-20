# Gap Analysis of This System + Improvement Plan

Generated: 2026-04-26

---

## The Core Problem

Every file in `profile/` is empty stubs. Without your actual data, this system
can produce structure but zero signal. The job matching quality is exactly as
good as the profile accuracy. Right now: zero.

---

## GAP INVENTORY

### GAP-01 | No profile data (CRITICAL — blocks everything else)

All of `profile/skills.md`, `profile/linkedin.md`, `profile/domains.md` are blank.

**What's missing:**
- Years of experience per domain
- Skill levels (EXPERT / PROFICIENT / FAMILIAR) filled in
- Which companies / projects / products you've worked on
- Education and certifications
- Current location and where you can work (visa status matters per country)
- Salary expectations per geography

**Impact:** Cannot run gap analysis, cannot optimize LinkedIn, cannot write "why me" pitches.

**Fix:** Fill `profile/questionnaire.md` (created this session). 30–60 min exercise.

---

### GAP-02 | No target role definition (CRITICAL)

We're using "senior/staff/principal" as a placeholder but haven't defined:
- Which specific role titles to target (e.g., "Staff Silicon Engineer" vs. "Principal AI Engineer")
- IC vs. management track
- Company size/stage preference (FAANG, scaleup, deep-tech startup)
- Sector priority order (chip design? AI? legal tech? fintech?)
- On-site / hybrid / remote requirement

**Impact:** LinkedIn search is unfocused; outreach has no anchor; gap analysis has no clear north star.

**Fix:** Answer the role-definition section in `profile/questionnaire.md`.

---

### GAP-03 | No evidence mapped (HIGH)

`evidence/projects.md` has one entry: this repo. Nothing else.

**What's missing:**
- Public GitHub work
- Publications, patents, conference talks
- Blog posts or LinkedIn articles
- Prior company work that can be referenced (at least anonymized)
- Any open-source contributions

**Impact:** Recruiters who Google you find nothing concrete. Skills table without evidence = unverifiable claims.

**Fix:** Spend 1 session inventorying everything that's already public, then plan what to build.

---

### GAP-04 | No market intelligence (HIGH)

We have job boards listed but have never actually analyzed what's in demand right now.

**What's missing:**
- Keyword frequency across 20+ real JDs for target roles
- Which skills appear in every JD vs. niche ones
- Salary benchmarks per role per geography
- Which companies are actively hiring vs. in a freeze
- What differentiates candidates who get calls vs. who don't

**Fix:** Run the market scan in `profile/market-scan.md` (template created this session).
Pull 20 JDs from target companies and tag requirements → frequency table.

---

### GAP-05 | No LinkedIn baseline (MEDIUM)

We don't know where you stand today, so we can't measure improvement.

**What's missing:**
- Current SSI (Social Selling Index) score — linkedin.com/sales/ssi
- Recruiter InMail count in last 30 days
- Profile view count (weekly)
- Search appearance count (weekly)
- Current headline and about text

**Fix:** 5-minute pull from LinkedIn analytics. Record in `profile/linkedin.md`.

---

### GAP-06 | No network inventory (MEDIUM)

Job offers come 60–70% through referrals. We have no map of who you know at target companies.

**What's missing:**
- Contacts at Google, Meta, Apple, Microsoft, Qualcomm, Synopsys, Cadence etc.
- Warm vs. cold connections per company
- Who to ask for referrals vs. who to ask for intel

**Fix:** `network/contacts.md` (created this session) — takes 20 min to fill in.

---

### GAP-07 | No interview prep system (MEDIUM)

Applied jobs → interviews will come. Nothing is built for this yet.

**What's missing:**
- STAR story bank (behavioral)
- Technical deep-dive topics per domain
- System design templates
- Company-specific research notes

**Fix:** `interview/` directory (created this session).

---

### GAP-08 | No ATS / resume layer (MEDIUM)

LinkedIn + GitHub are the primary vectors but companies also run ATS keyword screening.

**What's missing:**
- Resume tailored per role cluster (not one-size)
- ATS keyword density check per application
- Cover letter / cold email templates

**Fix:** `resume/` directory stub created this session.

---

### ~~GAP-09 | Scraper not built~~ ✓ RESOLVED (Session 8)

`tools/job-scraper.py` built: Adzuna/Reed/Remotive APIs + Playwright for 10 company career pages.
Dedup via `job-tracker/seen.txt`. Weekly GH Actions cron in `.github/workflows/weekly-scraper.yml`.

---

### GAP-10 | Offer / negotiation not tracked (LOW — future)

No system for comparing offers, tracking negotiation rounds, or calculating total comp.

**Fix:** `job-tracker/offers.md` — add when first offer arrives.

---

## IMPROVEMENTS TO THE SYSTEM

### IMP-01 | Skill scoring needs more granularity

`EXPERT / PROFICIENT / FAMILIAR` is too coarse. Recruiters and hiring managers
need to see *recency* and *scale*:

Better schema:
```
| Skill | Level | Last used | Scale/context | Evidence |
```

Example:
```
| RTL Design | EXPERT | 2024 | 28nm SoC, 10M gate count | github.com/... |
```

### ~~IMP-02 | Gap analysis needs a numeric score~~ ✓ RESOLVED (Session 8)

`tools/matcher.py` outputs match% weighted by JD section (required 2×, preferred 1×).
Apply ≥60% | Stretch 40–59% | Skip <40%. Saved to `gap-analysis/jobs/match-{N}pct-latest.md`.

### ~~IMP-03 | Weekly cadence needs a trigger~~ ✓ RESOLVED (Session 8)

`.github/workflows/weekly-scraper.yml` — Monday 08:00 UTC cron + manual trigger.
Auto-commits `job-tracker/new-this-week.md` and `seen.txt`.

### IMP-04 | LinkedIn post pipeline needs content queue

1x/week posting requires a content backlog. Need:
- `linkedin/post-queue.md` — 8-week pipeline of post ideas
- Posts tied to evidence artifacts (build something → post about it)

### IMP-05 | Company research not tracked

Before applying to any company, need 30-min research: culture, tech stack, recent news, who's on the team. Currently no home for this.

**Add:** `gap-analysis/jobs/[company]-research.md` template section.

---

## PRIORITY ORDER

_Updated Session 9 — all code items complete; remaining actions require user input._

| Priority | Action | Status | Effort | Unlocks |
|----------|--------|--------|--------|---------|
| 1 | Fill `profile/questionnaire.md` A+C | ⬜ P0 BLOCKER | 15 min | Everything |
| 2 | Fill `profile/my-profile.yaml` | ⬜ P0 BLOCKER | 20–30 min | Matcher, pathfinder, narrator |
| 3 | Run first full pipeline on a real JD | ⬜ (after P0) | 30 min | First application |
| 4 | Pull LinkedIn baseline (SSI, views, InMails) | ⬜ P1 | 5 min | LinkedIn optimization |
| 5 | Inventory existing evidence (GitHub, pubs, etc.) | ⬜ P1 | 30 min | Evidence map |
| 6 | Fill network contacts (1st degree at target cos) | ⬜ P2 | 20 min | Referral pipeline |
| 7 | Run market scan (20 JDs → keyword frequency) | ⬜ P2 | 90 min | Gap analysis quality |
| — | Build scraper | ✅ Done (Session 8) | — | — |
| — | Skill decay in matcher | ✅ Done (Session 8) | — | — |
| — | JD section detection in matcher | ✅ Done (Session 8) | — | — |
| — | NetworkX learning pathfinder | ✅ Done (Session 9) | — | — |
| — | Claude API narrator | ✅ Done (Session 9) | — | — |

---

## QUESTIONS NEEDED (grouped by decision)

See `profile/questionnaire.md` for the full question set.
The 5 highest-leverage questions right now:

1. **What are your 3 target role titles?** (shapes everything)
2. **Which domain is your strongest, most recent, and most provable?** (shapes pitch)
3. **What geography are you in and can you work in CH/UK/EU/India freely?** (shapes applications)
4. **What's already public — GitHub, publications, talks?** (shapes evidence strategy)
5. **What's your target comp range per geography?** (shapes which roles are worth pursuing)
