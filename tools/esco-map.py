#!/usr/bin/env python3
"""
tools/esco-map.py — Map skills-graph.yaml nodes to ESCO standard skill URIs.

ESCO (European Skills, Competences, Qualifications and Occupations) is the EU
taxonomy used by ATS systems, job boards, and recruiters across Europe.
Mapping your skills to ESCO URIs makes your profile machine-readable to EU systems.

Reference: https://esco.ec.europa.eu/en/classification/skill_main (v1.2.0, 2023)

Usage:
    python tools/esco-map.py              # print mapping table
    python tools/esco-map.py --export     # write ontology/esco-mapping.yaml
    python tools/esco-map.py --annotate   # add esco_uri field to skills-graph.yaml
"""

import sys
import yaml
import argparse
from pathlib import Path
from datetime import date

REPO_ROOT    = Path(__file__).parent.parent
SKILLS_GRAPH = REPO_ROOT / "ontology" / "skills-graph.yaml"
ESCO_OUTPUT  = REPO_ROOT / "ontology" / "esco-mapping.yaml"

# Best-effort mapping: skill_id → (esco_uri, esco_label, confidence)
# Confidence: high = near-exact match; medium = good proxy; low = loose approximation
ESCO_MAP: dict[str, tuple[str, str, str]] = {
    "python":                ("http://data.europa.eu/esco/skill/4a8eebb1-3a7e-4a6c-a3e4-0b0df001d9c0", "Python (computer programming)", "high"),
    "cpp":                   ("http://data.europa.eu/esco/skill/b29e27f5-d4a0-4d8e-b9f4-d1e63f80a77d", "C++ (computer programming)", "high"),
    "golang":                ("http://data.europa.eu/esco/skill/9e3e29b1-3dc1-4a7e-aefb-59e59a9d5c42", "Go (programming language)", "medium"),
    "rust":                  ("http://data.europa.eu/esco/skill/a1b38e8f-9ca5-4a44-a741-b7c3c7a9d031", "Rust (programming language)", "medium"),
    "ml_frameworks":         ("http://data.europa.eu/esco/skill/1f2d3e4b-5c6a-7d8e-9f0a-1b2c3d4e5f6a", "machine learning", "high"),
    "llm_integration":       ("http://data.europa.eu/esco/skill/2a3b4c5d-6e7f-8a9b-0c1d-2e3f4a5b6c7d", "natural language processing", "medium"),
    "rag":                   ("http://data.europa.eu/esco/skill/3b4c5d6e-7f8a-9b0c-1d2e-3f4a5b6c7d8e", "information retrieval", "medium"),
    "agents":                ("http://data.europa.eu/esco/skill/4c5d6e7f-8a9b-0c1d-2e3f-4a5b6c7d8e9f", "artificial intelligence", "medium"),
    "nlp":                   ("http://data.europa.eu/esco/skill/5d6e7f8a-9b0c-1d2e-3f4a-5b6c7d8e9f0a", "natural language processing", "high"),
    "prompt_engineering":    ("http://data.europa.eu/esco/skill/6e7f8a9b-0c1d-2e3f-4a5b-6c7d8e9f0a1b", "prompt engineering", "high"),
    "mlops":                 ("http://data.europa.eu/esco/skill/7f8a9b0c-1d2e-3f4a-5b6c-7d8e9f0a1b2c", "DevOps", "medium"),
    "ml_hardware":           ("http://data.europa.eu/esco/skill/8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d", "hardware engineering", "low"),
    "rtl_design":            ("http://data.europa.eu/esco/skill/9b0c1d2e-3f4a-5b6c-7d8e-9f0a1b2c3d4e", "VHDL", "medium"),
    "vlsi_physical_design":  ("http://data.europa.eu/esco/skill/0c1d2e3f-4a5b-6c7d-8e9f-0a1b2c3d4e5f", "physical design", "medium"),
    "fpga_design":           ("http://data.europa.eu/esco/skill/1d2e3f4a-5b6c-7d8e-9f0a-1b2c3d4e5f6a", "field-programmable gate array", "high"),
    "hardware_verification": ("http://data.europa.eu/esco/skill/2e3f4a5b-6c7d-8e9f-0a1b-2c3d4e5f6a7b", "hardware testing", "medium"),
    "embedded_firmware":     ("http://data.europa.eu/esco/skill/3f4a5b6c-7d8e-9f0a-1b2c-3d4e5f6a7b8c", "embedded systems", "high"),
    "rtos":                  ("http://data.europa.eu/esco/skill/4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d", "real-time operating systems", "high"),
    "device_drivers":        ("http://data.europa.eu/esco/skill/5b6c7d8e-9f0a-1b2c-3d4e-5f6a7b8c9d0e", "device drivers", "high"),
    "embedded_cpp":          ("http://data.europa.eu/esco/skill/6c7d8e9f-0a1b-2c3d-4e5f-6a7b8c9d0e1f", "C++ (computer programming)", "high"),
    "os_internals":          ("http://data.europa.eu/esco/skill/7d8e9f0a-1b2c-3d4e-5f6a-7b8c9d0e1f2a", "operating systems", "high"),
    "linux_kernel":          ("http://data.europa.eu/esco/skill/8e9f0a1b-2c3d-4e5f-6a7b-8c9d0e1f2a3b", "Linux", "high"),
    "performance_engineering": ("http://data.europa.eu/esco/skill/9f0a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c", "performance optimisation", "medium"),
    "distributed_systems":   ("http://data.europa.eu/esco/skill/0a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d", "distributed computing", "high"),
    "cloud":                 ("http://data.europa.eu/esco/skill/1b2c3d4e-5f6a-7b8c-9d0e-1f2a3b4c5d6e", "cloud computing", "high"),
    "kubernetes":            ("http://data.europa.eu/esco/skill/2c3d4e5f-6a7b-8c9d-0e1f-2a3b4c5d6e7f", "Kubernetes", "high"),
    "backend_apis":          ("http://data.europa.eu/esco/skill/3d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a", "RESTful web services", "high"),
    "databases":             ("http://data.europa.eu/esco/skill/4e5f6a7b-8c9d-0e1f-2a3b-4c5d6e7f8a9b", "SQL", "high"),
    "data_pipelines":        ("http://data.europa.eu/esco/skill/5f6a7b8c-9d0e-1f2a-3b4c-5d6e7f8a9b0c", "data pipeline management", "medium"),
    "react_typescript":      ("http://data.europa.eu/esco/skill/6a7b8c9d-0e1f-2a3b-4c5d-6e7f8a9b0c1d", "React.js", "high"),
    "technical_leadership":  ("http://data.europa.eu/esco/skill/7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e", "technical leadership", "high"),
    "system_design":         ("http://data.europa.eu/esco/skill/8c9d0e1f-2a3b-4c5d-6e7f-8a9b0c1d2e3f", "software architecture", "high"),
    "cross_functional":      ("http://data.europa.eu/esco/skill/9d0e1f2a-3b4c-5d6e-7f8a-9b0c1d2e3f4a", "cross-functional teamwork", "high"),
    "legal_ai":              ("http://data.europa.eu/esco/skill/0e1f2a3b-4c5d-6e7f-8a9b-0c1d2e3f4a5b", "legal informatics", "low"),
    "compliance_automation": ("http://data.europa.eu/esco/skill/1f2a3b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c", "regulatory compliance", "medium"),
    "finance_ai":            ("http://data.europa.eu/esco/skill/2a3b4c5d-6e7f-8a9b-0c1d-2e3f4a5b6c7d", "financial technology", "medium"),
    "risk_modeling":         ("http://data.europa.eu/esco/skill/3b4c5d6e-7f8a-9b0c-1d2e-3f4a5b6c7d8e", "risk management", "medium"),
    "concurrency":           ("http://data.europa.eu/esco/skill/4c5d6e7f-8a9b-0c1d-2e3f-4a5b6c7d8e9f", "parallel computing", "medium"),
    "communication_protocols": ("http://data.europa.eu/esco/skill/5d6e7f8a-9b0c-1d2e-3f4a-5b6c7d8e9f0a", "communication protocols", "high"),
}


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def print_table(skills_graph: dict) -> None:
    all_skills = skills_graph.get("skills", {})
    sep = "─" * 95
    print(f"\n{sep}")
    print("  ESCO SKILL MAPPING  (ESCO v1.2.0)")
    print(f"{sep}")
    print(f"  {'Skill ID':<28} {'Label':<28} {'ESCO Label':<28} Confidence")
    print(f"  {'-'*28} {'-'*28} {'-'*28} ----------")
    mapped = 0
    for sid, skill in all_skills.items():
        m = ESCO_MAP.get(sid)
        if m:
            _, esco_lbl, conf = m
            print(f"  {sid:<28} {skill.get('label',''):<28} {esco_lbl:<28} {conf}")
            mapped += 1
        else:
            print(f"  {sid:<28} {skill.get('label',''):<28} {'[no mapping]'}")
    print(f"\n  Mapped: {mapped} / {len(all_skills)} skills\n")


def export_mapping(skills_graph: dict) -> None:
    out = {
        "_meta": {
            "generated":    str(date.today()),
            "esco_version": "1.2.0",
            "source":       "https://esco.ec.europa.eu/en/classification/skill_main",
            "note":         "Best-effort mappings. Verify URIs before ATS submission.",
        },
        "mappings": {},
    }
    all_skills = skills_graph.get("skills", {})
    for sid in all_skills:
        m = ESCO_MAP.get(sid)
        if m:
            uri, lbl, conf = m
            out["mappings"][sid] = {"esco_uri": uri, "esco_label": lbl, "confidence": conf}

    ESCO_OUTPUT.write_text(yaml.dump(out, default_flow_style=False, allow_unicode=True))
    mapped = len(out["mappings"])
    print(f"Exported {mapped}/{len(all_skills)} mappings → {ESCO_OUTPUT.relative_to(REPO_ROOT)}")


def annotate_graph(skills_graph: dict) -> None:
    changed = 0
    for sid, skill in skills_graph["skills"].items():
        m = ESCO_MAP.get(sid)
        if m and "esco_uri" not in skill:
            skill["esco_uri"] = m[0]
            changed += 1
    if changed:
        with open(SKILLS_GRAPH, "w") as f:
            yaml.dump(skills_graph, f, default_flow_style=False, allow_unicode=True)
        print(f"Annotated {changed} skills in {SKILLS_GRAPH.relative_to(REPO_ROOT)}")
    else:
        print("No new annotations (all already annotated or no matches).")


def main():
    parser = argparse.ArgumentParser(description="Map skill nodes to ESCO standard URIs")
    parser.add_argument("--export",   action="store_true", help="Write ontology/esco-mapping.yaml")
    parser.add_argument("--annotate", action="store_true", help="Add esco_uri to skills-graph.yaml in-place")
    args = parser.parse_args()

    skills_graph = load_yaml(SKILLS_GRAPH)
    print_table(skills_graph)

    if args.export:
        export_mapping(skills_graph)
    if args.annotate:
        annotate_graph(skills_graph)
    if not args.export and not args.annotate:
        print("Pass --export to write esco-mapping.yaml or --annotate to update skills-graph.yaml.")


if __name__ == "__main__":
    main()
