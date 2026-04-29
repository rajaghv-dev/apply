"""Tests for tools/pathfinder.py — graph building, path finding, learning plan."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))               # conftest
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from pathfinder import build_skill_graph, shortest_path_to, build_learning_plan, get_role_gaps
from conftest import SKILLS_GRAPH, ROLES_GRAPH


def test_build_graph_nodes():
    G = build_skill_graph(SKILLS_GRAPH)
    assert "python" in G.nodes
    assert "ml_frameworks" in G.nodes
    assert "rtl_design" in G.nodes


def test_build_graph_edges():
    G = build_skill_graph(SKILLS_GRAPH)
    # python implies backend_apis
    assert G.has_edge("python", "backend_apis")
    assert G.has_edge("python", "ml_frameworks")


def test_build_graph_edge_cost():
    G = build_skill_graph(SKILLS_GRAPH)
    data = G["python"]["backend_apis"]
    assert data["weight"] == 0.65
    assert abs(data["cost"] - 0.35) < 0.01


def test_shortest_path_direct():
    G = build_skill_graph(SKILLS_GRAPH)
    path, cost = shortest_path_to(G, {"python"}, "backend_apis")
    assert path == ["python", "backend_apis"]
    assert cost < 1.0


def test_shortest_path_self():
    G = build_skill_graph(SKILLS_GRAPH)
    path, cost = shortest_path_to(G, {"python"}, "python")
    assert path == ["python"]
    assert cost == 0.0


def test_shortest_path_unreachable():
    G = build_skill_graph(SKILLS_GRAPH)
    # timing_analysis has no outgoing implies edges → no path FROM timing_analysis
    # but we test from a source that can't reach it
    path, cost = shortest_path_to(G, {"backend_apis"}, "rtl_design")
    # backend_apis doesn't imply rtl_design
    assert cost == float("inf")


def test_shortest_path_multi_hop():
    G = build_skill_graph(SKILLS_GRAPH)
    # python → ml_frameworks (0.70 weight)
    # so from {"python"} to ml_frameworks should be reachable
    path, cost = shortest_path_to(G, {"python"}, "ml_frameworks")
    assert path is not None
    assert len(path) == 2


def test_build_learning_plan_ordering():
    G    = build_skill_graph(SKILLS_GRAPH)
    plan = build_learning_plan(
        ["backend_apis", "timing_analysis"],
        {"python"},
        G,
        SKILLS_GRAPH,
    )
    # backend_apis is reachable from python; timing_analysis may not be
    reachable    = [s for s in plan if s["cost"] != float("inf")]
    from_scratch = [s for s in plan if s["cost"] == float("inf")]
    # Reachable should come first in sorted order
    if reachable and from_scratch:
        assert plan.index(reachable[0]) < plan.index(from_scratch[0])


def test_build_learning_plan_empty_profile():
    G    = build_skill_graph(SKILLS_GRAPH)
    plan = build_learning_plan(["python", "ml_frameworks"], set(), G, SKILLS_GRAPH)
    # All should be from-scratch
    assert all(s["cost"] == float("inf") for s in plan)


def test_get_role_gaps_silicon():
    label, gaps = get_role_gaps("silicon_engineer", set(), ROLES_GRAPH)
    assert label == "Silicon Engineer"
    assert "rtl_design" in gaps
    assert "timing_analysis" in gaps


def test_get_role_gaps_no_gaps_when_all_known():
    label, gaps = get_role_gaps(
        "ml_engineer",
        {"ml_frameworks", "python", "backend_apis"},
        ROLES_GRAPH,
    )
    assert gaps == []


def test_get_role_gaps_unknown_role():
    label, gaps = get_role_gaps("nonexistent_role", set(), ROLES_GRAPH)
    assert label == ""
    assert gaps == []


def test_get_role_gaps_partial_label_match():
    label, gaps = get_role_gaps("silicon", set(), ROLES_GRAPH)
    assert "Silicon" in label
