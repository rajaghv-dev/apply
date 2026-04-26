# Knowledge Map — Cross-Domain Concept Connections

The most valuable things a generalist knows are the connections most specialists never see.
Each entry here is a potential blog post, video, or interview story.

---

## Hardware → Software Bridges

### Timing closure ↔ Distributed systems latency
- In RTL: setup/hold violations → data corrupts at the clock edge
- In distributed systems: late arrival of data → stale reads, race conditions
- **The bridge**: both are fundamentally about ordering guarantees under timing uncertainty
- **Content angle**: "What chip designers know about latency that backend engineers don't"

### Clock domain crossing (CDC) ↔ Concurrency bugs
- In RTL: crossing between asynchronous clock domains without synchronizers → metastability
- In software: crossing between threads without memory barriers → data races
- **The bridge**: the hardware solution (synchronizer FFs) maps directly to mutex/semaphore
- **Content angle**: "CDC taught me to think about concurrency differently"

### DFT (scan chains) ↔ Observability / telemetry
- In RTL: you can't ship silicon you can't test — so you design testability in from day one
- In software: you can't debug production you can't observe — telemetry is DFT for software
- **The bridge**: "design for observability" is a hardware principle applied to software
- **Content angle**: "DFT for software engineers: what silicon taught me about observability"

### Power domains in SoC ↔ Service mesh resource isolation
- In SoC: different voltage islands, power gating, retention registers
- In microservices: resource quotas, circuit breakers, bulkheads
- **The bridge**: both are about fault isolation and resource management across subsystems

### RTL synthesis ↔ Compiler optimization
- Synthesis maps RTL to gates under timing/area constraints
- Compilers map high-level code to ISA under performance constraints
- **The bridge**: both are constraint-driven graph transformations
- **Content angle**: "Synthesis made me understand compilers"

---

## Embedded → Systems Bridges

### RTOS scheduling ↔ OS process scheduling
- FreeRTOS preemptive scheduling with priorities → Linux CFS scheduler
- **The bridge**: preemption, priority inversion, deadline scheduling — same problems, different scale
- **Content angle**: "RTOS taught me Linux scheduling from first principles"

### SoC bring-up ↔ Production incident response
- Bring-up: you have a new chip, nothing works, logs are sparse, you must find the truth
- Incident response: production is down, signals are partial, you must find root cause fast
- **The bridge**: the debugging discipline is identical — divide and conquer, signal isolation

### Device drivers ↔ Infrastructure abstraction layers
- Driver: hardware-specific implementation behind a generic POSIX file interface
- Infrastructure: cloud-specific implementation behind a generic provider interface
- **The bridge**: the abstraction pattern is identical; drivers made infrastructure patterns obvious

---

## Hardware × AI Bridges (your rarest moat)

### Systolic array architecture ↔ Matrix multiplication in ML
- Google's TPU is a systolic array. Understanding the hardware makes the ML primitives obvious.
- **Content angle**: "Building a systolic array in Verilog: understanding TPU from silicon up"
- **Project**: `riscv-nn-accel` — a minimal neural network accelerator in RTL

### Memory hierarchy in SoC ↔ KV cache in LLMs
- SoC: L1/L2/L3 cache, DRAM, bandwidth constraints drive everything
- LLMs: KV cache is a memory management problem — same pressure, different medium
- **Content angle**: "Why hardware engineers understand LLM inference bottlenecks intuitively"

### DFT coverage metrics ↔ ML evaluation metrics
- Fault coverage % → what % of faults can you detect?
- Recall, precision → what % of relevant items do you find?
- **The bridge**: both are about completeness of a test/evaluation regime

### RTL simulation ↔ ML model simulation/emulation
- Cycle-accurate RTL simulation: slow but faithful
- ML inference on CPU before deploying to accelerator: slow but faithful
- **The bridge**: simulation before silicon; emulation before deployment

---

## AI × Legal Bridges

### RAG pipeline ↔ Legal research workflow
- Legal research: find relevant precedents → synthesize → apply to current facts
- RAG: retrieve relevant chunks → synthesize → answer the query
- **The bridge**: RAG is legal research formalized
- **Content angle**: "Legal research as the original RAG system"

### Clause extraction ↔ Named entity recognition
- Contracts have structured entities (parties, dates, obligations, conditions)
- NER extracts typed spans from unstructured text
- **The bridge**: legal documents are the richest NER test case

### Compliance rules ↔ Rule-based + LLM hybrid systems
- Pure rule-based: brittle, can't handle ambiguous language
- Pure LLM: hallucination risk on compliance
- **The bridge**: hybrid is correct — rules for hard requirements, LLM for interpretation

---

## AI × Finance Bridges

### Monte Carlo simulation in finance ↔ Inference sampling in ML
- Risk: Monte Carlo to estimate VaR under uncertainty
- ML: sampling from distributions (MCMC, variational inference)
- **The bridge**: probabilistic reasoning under uncertainty — same mathematics

### Financial time series ↔ Sequence modeling
- Stock prices, order books → time series with regime changes
- LSTMs, Transformers on sequences → same architecture, different domain
- **The bridge**: transformers were useful in finance before language models

### Risk models ↔ Anomaly detection
- Credit risk: P(default) — anomaly in payment behavior
- Fraud detection: anomaly in transaction pattern
- **The bridge**: both are binary classifiers on imbalanced datasets

---

## The Meta-Bridge (your unique thesis)

**"From transistor to transformer"**

The same fundamental principles — abstraction layers, timing, resource constraints,
observability, fault tolerance, test coverage — appear at every level of the stack.

Someone who has worked at the transistor level and at the LLM level has seen
these principles in their most stripped-down forms. They recognize them everywhere else.

This is the thesis that makes you rare. Every content piece, interview story, and
LinkedIn post should tie back to this: **the principles don't change, the substrate does.**

---

## TO-FILL: Your Own Bridges

Add your own cross-domain insights here. These are the most valuable entries.

| Insight | Domain A | Domain B | Content angle |
|---------|---------|---------|---------------|
| [YOUR INSIGHT] | | | |
