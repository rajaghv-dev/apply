# Open Source Target Projects

Organized by domain. Pick 1 from each priority tier to start.

---

## TIER 1 — Start here (accessible, active, high impact)

### cocotb — Python-based hardware verification
- **Repo**: github.com/cocotb/cocotb
- **Stars**: 2.1k+ | **Language**: Python + C | **Activity**: very active
- **Why**: Python + hardware — your exact intersection. Docs and test improvements welcome.
- **Entry points**: "good first issue" label; documentation improvements; new examples
- **Your angle**: hardware expertise + Python fluency = ideal contributor
- **Status**: [ ] explored [ ] first issue [ ] first PR [ ] merged

### LangChain — LLM application framework
- **Repo**: github.com/langchain-ai/langchain
- **Stars**: 90k+ | **Language**: Python | **Activity**: extremely active
- **Why**: AI/agents domain; massive audience; many docs + integration PRs merged quickly
- **Entry points**: documentation, integration bug fixes, example notebooks
- **Your angle**: legal + finance domain examples nobody else is writing
- **Status**: [ ] explored [ ] first issue [ ] first PR [ ] merged

### OpenLane — Open source chip design flow
- **Repo**: github.com/The-OpenROAD-Project/OpenLane
- **Stars**: 3k+ | **Language**: Python + TCL | **Activity**: active
- **Why**: EDA + Python — unique intersection, small contributor pool = high visibility
- **Entry points**: documentation, Python script improvements, new PDK support
- **Your angle**: RTL design expertise means you understand the domain deeply
- **Status**: [ ] explored [ ] first issue [ ] first PR [ ] merged

---

## TIER 2 — Medium effort, high credibility

### Transformers (Hugging Face) — ML model library
- **Repo**: github.com/huggingface/transformers
- **Stars**: 130k+ | **Language**: Python | **Activity**: very active
- **Why**: ML credibility signal; widely known; complex but well-documented
- **Entry points**: documentation, model card improvements, tokenizer fixes
- **Status**: [ ] explored [ ] first issue [ ] first PR [ ] merged

### OpenROAD — Physical design automation
- **Repo**: github.com/The-OpenROAD-Project/OpenROAD
- **Stars**: 700+ | **Language**: C++ + Python | **Activity**: active
- **Why**: Physical design + automation; your VLSI background is directly relevant
- **Entry points**: Python API improvements, documentation, test cases
- **Status**: [ ] explored [ ] first issue [ ] first PR [ ] merged

### LlamaIndex — RAG framework
- **Repo**: github.com/run-llama/llama_index
- **Stars**: 35k+ | **Language**: Python | **Activity**: very active
- **Why**: RAG expertise directly applicable; legal/finance domain integrations needed
- **Your angle**: build a legal document loader or compliance data connector
- **Status**: [ ] explored [ ] first issue [ ] first PR [ ] merged

### MLflow — ML experiment tracking
- **Repo**: github.com/mlflow/mlflow
- **Stars**: 18k+ | **Language**: Python + Java | **Activity**: active
- **Why**: MLOps gap in your profile; contributing forces you to learn the space
- **Entry points**: documentation, plugin integrations, example recipes
- **Status**: [ ] explored [ ] first issue [ ] first PR [ ] merged

---

## TIER 3 — Long-term, high authority

### LLVM / MLIR — Compiler + ML IR
- **Repo**: github.com/llvm/llvm-project
- **Stars**: 27k+ | **Language**: C++ | **Activity**: extremely active
- **Why**: If targeting AI hardware / AI compiler roles (NVIDIA, Google, AMD)
- **Entry points**: MLIR documentation, small dialect improvements
- **Warning**: Very high bar. Start with Tier 1 first.
- **Status**: [ ] explored

### RISC-V CVA6 / Ibex — Open RISC-V cores
- **Repo**: github.com/openhwgroup/cvA6 | github.com/lowRISC/ibex
- **Stars**: 1.2k / 1.1k | **Language**: SystemVerilog | **Activity**: active
- **Why**: RTL contribution in a real open-source core — extremely rare, very credible
- **Entry points**: verification improvements, documentation, tooling
- **Status**: [ ] explored

### QuantLib — Quantitative finance library
- **Repo**: github.com/lballabio/QuantLib
- **Stars**: 5k+ | **Language**: C++ | **Activity**: active
- **Why**: FinTech + C++ credibility; niche but well-known in quant circles
- **Status**: [ ] explored

---

## YOUR OWN PROJECTS (start and attract contributors)

These are repos you create and maintain. You are the maintainer from day one.

| Project | Domain | Status | Stars |
|---------|--------|--------|-------|
| `legal-contract-agent` | AI × legal | planned | — |
| `finance-risk-agent` | AI × finance | planned | — |
| `riscv-nn-accel` | hardware × AI | planned | — |
| `eda-mcp-server` | hardware × AI tools | planned | — |
| `compliance-checker` | AI × legal | planned | — |
| `cocotb-ai-tb` | hardware × AI | planned | — |

See `github-projects/ideas.md` for full project specs.

---

## Contribution tactics

### Finding issues
- Filter by `good first issue` + `help wanted` + `bug` labels
- Look for documentation issues — high merge rate, builds understanding
- Check "stale" issues — ones open > 6 months that nobody has picked up

### Making PRs that get merged
- One change per PR (not "while I'm here, I also fixed...")
- Match existing code style exactly
- Write a clear PR description: what, why, how to test
- Link to the issue it closes
- Respond to review comments within 24 hours

### Building toward maintainer
- Review other PRs before yours is merged (shows community orientation)
- Triage issues: comment with reproduction steps or "I can reproduce on X"
- Write a blog post about the project → share with maintainers → visibility
- Attend contributor calls if they exist

---

## Contribution log → see `open-source/log.md`
