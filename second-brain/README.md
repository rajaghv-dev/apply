# Second Brain — System Design

## What this is

A personal knowledge management system integrated with the job search engine.
Everything you learn feeds into everything you build, which becomes evidence,
which becomes content, which grows your reputation, which gets you calls.

```
Learn → Build → Document → Publish → Share → Reputation → Calls → Offers
  ↑                                                                    |
  └────────────────── Gaps from JD analysis ──────────────────────────┘
```

## Structure

```
second-brain/
├── README.md           ← this file — system design
├── knowledge-map.md    ← cross-domain concept connections (the generalist's moat)
├── learning-log.md     ← timestamped learning entries (what, source, insight, artifact)
├── insights.md         ← distilled insights worth keeping permanently
└── connections.md      ← cross-domain bridges (the rarest and most valuable things you know)
```

## How it integrates with the rest of the repo

```
gap-analysis/jobs/      ──→  learning/roadmap.md     (gaps → what to learn)
                               ↓
                         second-brain/learning-log.md  (log each session)
                               ↓
                         github-projects/ideas.md      (build evidence)
                               ↓
                         content/ideas.md              (write about it)
                               ↓
                         content/pipeline.md           (produce the content)
                               ↓
                         evidence/platform-tracker.md  (log the artifact)
                               ↓
                         profile/my-profile.yaml       (update skill level + evidence)
```

## Learning log protocol

Every learning session gets one entry in `learning-log.md`:

```markdown
## YYYY-MM-DD | [Topic] | [Source]
**What I learned**: 1–3 sentences, the actual insight
**Connects to**: [other domains or skills this links to]
**Artifact**: [what I built or will build to prove it]
**Status**: LEARNED / BUILDING / PUBLISHED
```

## Insight types

| Type | Description | Where it goes |
|------|-------------|--------------|
| **Bridge** | A connection between two domains most people don't see | `connections.md` — highest value |
| **Principle** | A durable truth about how something works | `insights.md` |
| **Pattern** | A recurring solution to a class of problems | `insights.md` |
| **Observation** | Something you noticed that surprised you | `learning-log.md` |
| **Question** | Something you don't understand yet | `learning-log.md` → `learning/roadmap.md` |

## The generalist's advantage

Most engineers know one domain deeply. You know 6+ at working depth.
The value isn't in each domain separately — it's in the bridges between them.

Every bridge you can articulate and demonstrate is a story no other candidate can tell.
Document every cross-domain insight you have in `connections.md`.

Those become:
- LinkedIn post hooks ("Here's what RTL timing taught me about distributed systems latency")
- Medium article theses
- Interview differentiators ("I've seen this problem from the hardware side too")
- YouTube video angles
