# LP-002 | LLM Agents + Tool Use

**Domain**: AI / LLM  
**Priority**: P1 — fastest-growing requirement in AI engineer JDs  
**Effort**: 3–5 days  
**STATUS**: TODO

---

## Why this matters

Agents are the shift from "LLM as generator" to "LLM as reasoning engine that takes actions."
Every AI platform role now requires understanding agentic systems. Your systems engineering
background (state machines, resource management, fault isolation) is directly applicable.

Gap closed: `agents` in `profile/my-profile.yaml`

---

## Learning objectives

- [ ] Explain the ReAct pattern (Reason → Act → Observe loop)
- [ ] Build an agent that uses tools (web search, code execution, file I/O, APIs)
- [ ] Handle agent failure modes: infinite loops, hallucinated tool calls, context overflow
- [ ] Implement multi-agent patterns: supervisor, parallel, sequential
- [ ] Use Claude's tool use API natively (not just through a framework)
- [ ] Evaluate agent reliability: success rate, steps to completion, failure analysis

---

## Resources

### Day 1 — Concepts + API
- [ ] Read: Anthropic docs → Tool use guide (docs.anthropic.com/en/docs/tool-use)
- [ ] Read: "ReAct: Synergizing Reasoning and Acting" — arxiv.org/abs/2210.03629
- [ ] Build: Hello-world tool use agent with Claude API (1 tool: calculator or web search)

### Day 2 — Framework fluency
- [ ] Tutorial: LangChain agents + tools (~3 hrs)
- [ ] Tutorial: LlamaIndex agents (~2 hrs)
- [ ] Compare: build the same agent in raw API vs LangChain. Note the tradeoffs.

### Day 3 — Real agent
- [ ] Build: A research agent that:
  - Takes a question as input
  - Searches the web (via Tavily or SerpAPI)
  - Reads and summarizes relevant pages
  - Writes a structured answer with citations

### Day 4 — Domain application (legal or finance)
- [ ] Build: A legal contract review agent:
  - Tools: read_file, search_clause, extract_dates, check_jurisdiction
  - Task: "Review this contract for missing clauses and flag high-risk terms"
  - OR: A finance agent: read_ticker, get_price, calculate_returns, generate_report

### Day 5 — Evidence + polish
- [ ] Polish into a GitHub repo with a compelling README
- [ ] Add a demo GIF or screenshot (increases GitHub star rate significantly)
- [ ] Stub content: "Building a legal review agent: the architecture decisions"

---

## Evidence artifact

**Repo**: `legal-contract-agent` (expands LP-001 from RAG to agentic)
**What it proves**: You build agents, not just chatbots. Domain-aware tool design.

---

## Done criteria

- [ ] Working agent with ≥3 tools
- [ ] Handles at least one failure mode gracefully (tool error, hallucinated call)
- [ ] GitHub repo live with demo
- [ ] `profile/my-profile.yaml`: `agents: level: PROFICIENT, evidence: [URL]`
- [ ] `second-brain/learning-log.md`: entry added

---

## Cross-domain connections

- State machine = agent loop (RTL state machines → agent reasoning loop)
- Resource management: agent token budget ↔ SoC power budget
- Fault isolation: agent tool error handling ↔ embedded error recovery

---

## STATUS: TODO
