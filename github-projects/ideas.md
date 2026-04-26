# GitHub Project Specs

---

## GP-01 | legal-contract-agent

**Tagline**: LLM agent for contract clause extraction, risk flagging, and GDPR compliance checking

**What it does**:
- Ingest: PDF or text contracts
- Extract: clause types, parties, dates, obligations (structured JSON output)
- Flag: missing required clauses, high-risk terms, jurisdiction mismatches
- Tools: read_file, extract_clause, check_compliance, search_precedent
- API: Claude tool use + RAG over a clause reference corpus

**Tech stack**: Python, Claude API, LangChain or raw tool use, Chroma, pdfplumber

**Why it's differentiating**:
- Most LLM demos use toy data. This uses real contract structure.
- Demonstrates domain knowledge (you know what to extract and why)
- Directly demonstrates legal tech engineer capability

**Done criteria**:
- [ ] Works on 5 different real contracts
- [ ] Extracts ≥10 clause types accurately
- [ ] Includes evaluation script with precision/recall
- [ ] README explains the architecture and tradeoffs
- [ ] Demo video or GIF

**Lesson plans**: LP-001, LP-002, LP-007
**Content angle**: T02, T03 from `content/ideas.md`

---

## GP-02 | compliance-checker

**Tagline**: AI-powered GDPR and regulatory compliance rule checker for legal documents

**What it does**:
- Input: Data Processing Agreement or privacy policy
- Check: against GDPR Article 28 requirements checklist
- Output: pass/fail per requirement + evidence quote + confidence + remediation suggestion
- Hybrid: rule-based for mandatory requirements + LLM for interpretation

**Tech stack**: Python, Claude API, pdfplumber, structured output (Pydantic)

**Why it's differentiating**:
- Hybrid architecture (rule + LLM) is production-realistic
- Compliance domain shows regulatory awareness
- DRC (Design Rule Check) from chip design is the mental model — explain that in README

**Done criteria**:
- [ ] Checks against GDPR Article 28 (20+ requirements)
- [ ] Output is a structured JSON report + human-readable summary
- [ ] Tested on 3 real DPAs (downloadable from public sources)
- [ ] README explains why hybrid (not pure LLM) is the right architecture

**Lesson plans**: LP-007
**Content angle**: T03

---

## GP-03 | finance-risk-agent

**Tagline**: RAG-powered financial risk analyzer with live market data tools

**What it does**:
- Tools: get_price(ticker), get_financials(ticker), calculate_var(portfolio), search_news(query)
- Workflow: given a portfolio → analyze risk exposure → generate report with citations
- RAG: over financial regulations (Basel III, SEC filings format)
- Output: structured risk report with evidence sources

**Tech stack**: Python, Claude API, yfinance, LangChain, Chroma

**Why it's differentiating**:
- Shows finance domain knowledge (VaR, portfolio risk, regulatory context)
- Tool use with real APIs (not just static docs)
- Demonstrates you understand what "AI in finance" actually means

**Done criteria**:
- [ ] Works with live price data (yfinance)
- [ ] Calculates basic portfolio metrics (VaR, Sharpe, correlation)
- [ ] Generates a structured risk report
- [ ] README explains the financial concepts (shows domain knowledge)

**Lesson plans**: LP-001, LP-002, LP-008
**Content angle**: T04, T10

---

## GP-04 | riscv-nn-accel

**Tagline**: Minimal neural network accelerator in SystemVerilog + Python inference

**What it does**:
- RTL implementation of a 4x4 systolic array (matrix multiply unit)
- Configurable MAC (multiply-accumulate) depth
- cocotb testbench verifying correctness against NumPy reference
- Python script to run a tiny neural network (MNIST MLP) on the hardware
- Cycle-accurate simulation using Verilator

**Tech stack**: SystemVerilog, cocotb, Verilator, Python, NumPy

**Why it's differentiating**:
- Extremely rare: most people can do ML OR RTL, not both in one repo
- Directly demonstrates the "transistor to transformer" thesis
- Job magnet for AI hardware roles at Google, Apple, NVIDIA

**Done criteria**:
- [ ] RTL passes all cocotb tests vs. NumPy reference
- [ ] Can run a tiny MLP (2 layers) through the simulated hardware
- [ ] README explains the systolic array architecture and why it matters for ML
- [ ] Includes a "what this would look like as a real chip" section

**Lesson plans**: LP-003, LP-009, LP-012
**Content angle**: T01, B06

---

## GP-05 | eda-mcp-server

**Tagline**: MCP server exposing EDA tool capabilities to Claude and other LLM clients

**What it does**:
- MCP tools: run_synthesis(rtl_file), run_sim(testbench), check_timing(sdf_file), lint_rtl(file)
- Wraps: open-source EDA tools (Yosys, Icarus Verilog, Verilator)
- Use case: "Hey Claude, synthesize this RTL and tell me the critical path"
- Extension: LLM-assisted RTL debugging

**Tech stack**: Python, MCP SDK, Yosys, Icarus Verilog, Verilator

**Why it's differentiating**:
- Bridges AI tooling (MCP) with hardware tooling (EDA) — nobody else is doing this
- Shows you understand MCP protocol AND EDA tools
- High novelty = high visibility (blog post writes itself)

**Done criteria**:
- [ ] At least 3 working MCP tools (synthesis, simulation, linting)
- [ ] Works with Claude Desktop or Claude Code
- [ ] README includes architecture and demo GIF
- [ ] Blog post published

**Lesson plans**: LP-004, LP-002
**Content angle**: T07

---

## GP-06 | cocotb-examples

**Tagline**: A curated collection of cocotb testbenches for common RTL patterns

**What it does**:
- Testbenches for: FIFO, SPI master, AXI-lite subordinate, UART, clock divider, CRC generator
- Each module: RTL (SystemVerilog) + cocotb testbench (Python) + CI (GitHub Actions)
- Educational: clear comments, README explaining the verification strategy
- Contribution target: submit the best examples to cocotb upstream

**Tech stack**: SystemVerilog, cocotb, Icarus Verilog, pytest, GitHub Actions

**Why it's differentiating**:
- First target for open source contribution (LP-003)
- Educational content = search traffic + community goodwill
- Demonstrates both RTL and Python depth

**Lesson plans**: LP-003
**Content angle**: T06

---

## GP-07 | cctv-analytics-demo

**Tagline**: Real-time CCTV analytics: detection + tracking + zone alerts

**What it does**:
- Input: video file or webcam stream
- Detect: people, vehicles, objects (YOLOv8)
- Track: multi-object tracking with stable IDs (ByteTrack)
- Alert: configurable zone entry/exit events
- Output: annotated video + JSON event log

**Tech stack**: Python, Ultralytics YOLOv8, ByteTrack, OpenCV

**Why it's differentiating**:
- Shows embedded/systems thinking applied to CV (latency profiling, edge constraints)
- Video output is inherently compelling (easy to share)
- Unlocks industrial + surveillance + smart city domain targeting

**Lesson plans**: LP-013
**Content angle**: "Building a CCTV analytics pipeline"

---

## GP-08 | llm-rtl-gen (future)

**Tagline**: LLM-assisted RTL generation and verification

**What it does**:
- Input: natural language description of a hardware module
- Generate: RTL code (SystemVerilog) via LLM
- Verify: auto-generate cocotb testbench + run simulation
- Report: whether generated RTL passes functional verification

**Status**: P3 — complex, but extremely high differentiation once built

**Lesson plans**: LP-004, LP-002, LP-003
