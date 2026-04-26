# LP-001 | RAG Pipeline Fundamentals

**Domain**: AI / LLM  
**Priority**: P1 — appears in 80%+ of AI engineer JDs  
**Effort**: 3–5 days  
**STATUS**: TODO

---

## Why this matters

RAG (Retrieval-Augmented Generation) is the dominant pattern for building
LLM applications on private or domain-specific data. Every legal tech and
fintech AI role requires understanding it. Your hardware background (memory
hierarchy, bandwidth constraints) gives you an intuitive edge here.

Gap closed: `rag` in `profile/my-profile.yaml`

---

## Learning objectives

By the end you will be able to:
- [ ] Explain the RAG pipeline end-to-end (ingest → chunk → embed → index → retrieve → generate)
- [ ] Build a working RAG system from scratch using LangChain or LlamaIndex
- [ ] Evaluate RAG quality (retrieval precision, answer faithfulness, groundedness)
- [ ] Choose between chunking strategies (fixed size, semantic, recursive)
- [ ] Choose between vector databases (Chroma, FAISS, Pinecone, Weaviate)
- [ ] Handle failure modes: hallucination, missing context, irrelevant retrieval

---

## Resources (in order)

### Day 1 — Concepts
- [ ] Read: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (original RAG paper) — arxiv.org/abs/2005.11401
- [ ] Watch: "LangChain RAG deep dive" — DeepLearning.ai short course (~2 hrs)
- [ ] Read: LlamaIndex docs → "Getting Started" section

### Day 2 — Build the basics
- [ ] Tutorial: Build a simple document Q&A system with LangChain + Chroma
  - Ingest: load PDF or text
  - Chunk: RecursiveCharacterTextSplitter
  - Embed: OpenAI or HuggingFace embeddings
  - Retrieve: similarity search
  - Generate: Claude or GPT-4 with context

### Day 3 — Go deeper
- [ ] Read: "Evaluating RAG systems" — Ragas library docs (docs.ragas.io)
- [ ] Experiment: test 3 chunking strategies on the same document. Observe retrieval quality.
- [ ] Experiment: test 2 embedding models. Compare retrieval results.

### Day 4 — Domain application
- [ ] Build: RAG over a set of legal documents (use public contract templates)
  - Add metadata filtering (document type, date, party)
  - Test: "What are the termination conditions in contract X?"
  - Evaluate: does it hallucinate? does it cite the right section?

### Day 5 — Evidence artifact
- [ ] Polish the legal RAG project into a public GitHub repo
- [ ] Write README.md with: what it does, architecture diagram, how to run
- [ ] Stub a Medium article: "RAG for legal documents: what the tutorials don't cover"

---

## Evidence artifact

**Repo**: `legal-contract-agent` (or a dedicated `rag-legal-demo` repo)
**What it proves**: You can build production-quality RAG, not just run tutorials.
**Evaluation criteria**: Works on at least 3 different documents. Includes evaluation script.

---

## Done criteria

- [ ] GitHub repo live with working code
- [ ] README describes the architecture and tradeoffs you made
- [ ] You can explain, in an interview: why you chose that chunking strategy, that vector DB, that retrieval approach
- [ ] `profile/my-profile.yaml`: `rag: level: PROFICIENT, evidence: [repo URL]`
- [ ] `second-brain/learning-log.md`: entry added
- [ ] Content stub added to `content/ideas.md` if applicable

---

## Cross-domain connections to note

While doing this, watch for:
- Similarity to memory hierarchy in SoC (cache hit = retrieval hit)
- Chunking strategy ↔ cache line size tradeoffs
- Retrieval precision ↔ DFT fault coverage

Document anything you notice in `second-brain/connections.md`.

---

## STATUS: TODO → IN-PROGRESS → DONE

When done, update this file's STATUS line to DONE and add:
**Completed**: YYYY-MM-DD  
**Artifact**: [link]  
**Key insight**: [one sentence — the most surprising thing you learned]
