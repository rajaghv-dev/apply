# LP-003 | cocotb: Python-Based Hardware Verification

**Domain**: Hardware × Python  
**Priority**: P1 — bridges hardware and software; enables open-source contribution  
**Effort**: 3–5 days  
**STATUS**: TODO

---

## Why this matters

cocotb lets you write hardware testbenches in Python instead of SystemVerilog/UVM.
It's the bridge between your hardware expertise and your Python skills.
Contributing to cocotb is a credible, accessible open source entry point.

Gaps closed: `hardware_verification` (deepened), `python` (applied to hardware)

---

## Learning objectives

- [ ] Understand how cocotb hooks into an HDL simulator (ModelSim, Icarus, Verilator)
- [ ] Write coroutine-based testbenches using Python async patterns
- [ ] Drive RTL signals, monitor outputs, assert expected behavior
- [ ] Use cocotb's built-in components (Clock, Reset, bus interfaces)
- [ ] Integrate with pytest for structured reporting
- [ ] Set up a CI pipeline (GitHub Actions) for automated regression

---

## Resources

### Day 1 — Setup + first test
- [ ] Install: cocotb + Icarus Verilog (both free, runs on Linux/WSL)
- [ ] Tutorial: cocotb "Getting Started" — docs.cocotb.org/en/stable/quickstart.html
- [ ] Exercise: Write a testbench for a 4-bit adder in RTL

### Day 2 — RTL + testbench co-design
- [ ] Write RTL: a simple FIFO (or use an existing open-source FIFO)
- [ ] Write cocotb testbench:
  - Fill the FIFO, read back, verify ordering
  - Test empty/full edge cases
  - Measure throughput

### Day 3 — Advanced patterns
- [ ] Read: cocotb "Coroutines and tasks" section
- [ ] Implement: a bus functional model (BFM) for a simple APB or AXI-lite interface
- [ ] Exercise: test an SPI master module using cocotb

### Day 4 — CI integration + open source prep
- [ ] Set up GitHub Actions workflow that runs cocotb tests on every push
- [ ] Read: cocotb CONTRIBUTING.md and open issues list
- [ ] Identify: 1 good first issue to fix or 1 documentation gap to fill

### Day 5 — Contribution + artifact
- [ ] Submit a PR to cocotb (docs, example, or bug fix)
- [ ] Polish your cocotb project into a public repo with README
- [ ] Stub content: "cocotb tutorial: Python-based hardware verification from scratch"

---

## Evidence artifacts

1. **Your cocotb repo**: A clean, documented set of example testbenches (RTL + Python)
2. **cocotb PR**: At least 1 PR submitted (ideally merged)

---

## Done criteria

- [ ] Can write a complete cocotb testbench from scratch without looking at docs
- [ ] GitHub repo with at least 3 tested RTL modules
- [ ] 1 PR submitted to cocotb upstream
- [ ] `profile/my-profile.yaml`: `hardware_verification: PROFICIENT (deeper), python: EXPERT (applied to HW)`
- [ ] `open-source/log.md`: contribution entry added

---

## STATUS: TODO
