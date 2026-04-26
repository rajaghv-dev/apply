# Distilled Insights

Durable principles worth keeping permanently.
These are the things that remain true across domains and over time.

---

## Principles of Abstraction

**Principle**: Every level of abstraction hides complexity and leaks it in failure modes.
- RTL → gates: timing violations leak through
- Driver → POSIX: hardware quirks leak through
- LLM API → application: hallucination and latency leak through
**Application**: Always understand one level below your operating layer.

---

## Principles of Observability

**Principle**: You cannot fix what you cannot see. Design for observability from day one.
- Hardware: DFT (scan chains, BIST) — built in at design time
- Software: telemetry, tracing, structured logs — built in at architecture time
- ML: eval pipelines, monitoring — built in before deployment
**Application**: Every system you build should have a "DFT mode" — a way to expose internal state.

---

## Principles of Fault Isolation

**Principle**: Faults spread unless you design containment boundaries.
- Hardware: power domains, clock domains, reset domains
- Software: circuit breakers, bulkheads, retries with backoff
- Distributed systems: partition tolerance, quorum reads
**Application**: Before building any system, draw the fault domains first.

---

## Principles of Testing

**Principle**: Test coverage is a proxy for confidence, not correctness.
- Hardware: fault coverage % ≠ bug-free silicon
- Software: line coverage % ≠ working software
- ML: accuracy % ≠ production reliability
**Application**: Define what failure modes matter, then test those specifically.

---

## Principles of Constraints

**Principle**: Performance problems are almost always about constraints — time, space, bandwidth.
- RTL: timing closure = meeting timing constraints under area/power budget
- Algorithms: time/space tradeoffs
- ML inference: latency vs. throughput vs. memory
**Application**: State the constraints before designing the solution.

---

## TO-FILL: Your Own Insights

Add insights here when you discover something that feels durably true.
Good candidates: things that surprised you, things that changed how you think,
things you wish you'd known earlier.

| Insight | Domain learned | Where it applies |
|---------|---------------|-----------------|
| [YOUR INSIGHT] | | |
