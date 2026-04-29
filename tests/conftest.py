"""Shared pytest fixtures — minimal YAML stubs that mirror real schema."""
import pytest


SKILLS_GRAPH = {
    "skills": {
        "python": {
            "label": "Python",
            "domain": "software_backend",
            "synonyms": ["Python3", "django", "fastapi"],
            "implies": {"backend_apis": 0.65, "ml_frameworks": 0.70},
        },
        "ml_frameworks": {
            "label": "ML Frameworks",
            "domain": "ai_ml",
            "synonyms": ["PyTorch", "TensorFlow", "machine learning", "deep learning"],
            "implies": {"python": 0.80},
        },
        "rtl_design": {
            "label": "RTL Design",
            "domain": "hardware",
            "synonyms": ["RTL", "Verilog", "VHDL", "SystemVerilog"],
            "implies": {"hardware_verification": 0.65, "timing_analysis": 0.75},
        },
        "hardware_verification": {
            "label": "Hardware Verification",
            "domain": "hardware",
            "synonyms": ["UVM", "functional verification", "testbench"],
            "implies": {},
        },
        "timing_analysis": {
            "label": "Timing Analysis",
            "domain": "hardware",
            "synonyms": ["STA", "static timing analysis", "timing closure"],
            "implies": {},
        },
        "backend_apis": {
            "label": "Backend APIs",
            "domain": "software_backend",
            "synonyms": ["REST", "RESTful", "GraphQL", "API design"],
            "implies": {},
        },
    }
}

ROLES_GRAPH = {
    "roles": {
        "ml_engineer": {
            "label": "ML Engineer",
            "domain_clusters": ["ai_ml"],
            "title_synonyms": ["ML Engineer", "AI Engineer"],
            "required":  {"ml_frameworks": "PROFICIENT", "python": "PROFICIENT"},
            "preferred": {"backend_apis": "FAMILIAR"},
            "target_companies": ["Google", "Meta"],
            "geographies": ["USA", "UK"],
        },
        "silicon_engineer": {
            "label": "Silicon Engineer",
            "domain_clusters": ["hardware"],
            "title_synonyms": ["ASIC Engineer", "RTL Engineer"],
            "required":  {"rtl_design": "EXPERT", "timing_analysis": "PROFICIENT"},
            "preferred": {"hardware_verification": "PROFICIENT"},
            "target_companies": ["Qualcomm", "ARM"],
            "geographies": ["UK", "India"],
        },
    }
}

PROFILE_FILLED = {
    "skills": {
        "python":    {"level": "EXPERT",     "last_used": 2025, "evidence": "github.com/x"},
        "rtl_design": {"level": "PROFICIENT", "last_used": 2020, "evidence": ""},
    }
}

PROFILE_EMPTY = {"skills": {}}


@pytest.fixture
def skills_graph():
    return SKILLS_GRAPH


@pytest.fixture
def roles_graph():
    return ROLES_GRAPH


@pytest.fixture
def profile_filled():
    return PROFILE_FILLED


@pytest.fixture
def profile_empty():
    return PROFILE_EMPTY
