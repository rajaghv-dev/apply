"""Tests for tools/offer-compare.py — parsing, enrichment, CoL adjustment."""
import sys
import importlib.util
import pytest
from pathlib import Path

# Load hyphenated module
def _load():
    spec = importlib.util.spec_from_file_location(
        "offer_compare",
        Path(__file__).parent.parent / "tools" / "offer-compare.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules["offer_compare"] = mod
    return mod

_mod = _load()
parse_offer_str = _mod.parse_offer_str
enrich          = _mod.enrich
FX              = _mod.FX
COL             = _mod.COL


def _offer(company="TestCo", currency="USD", base=100_000,
           equity=10_000, bonus_pct=10, city="New York"):
    return dict(company=company, currency=currency, base=base,
                equity=equity, bonus_pct=bonus_pct, city=city)


# ── parse_offer_str ───────────────────────────────────────────────────────────

def test_parse_valid():
    o = parse_offer_str("Google Zurich,CHF,180000,50000,20,Zurich")
    assert o["company"]   == "Google Zurich"
    assert o["currency"]  == "CHF"
    assert o["base"]      == 180_000
    assert o["equity"]    == 50_000
    assert o["bonus_pct"] == 20
    assert o["city"]      == "Zurich"


def test_parse_strips_whitespace():
    o = parse_offer_str(" ARM , GBP , 120000 , 20000 , 15 , Cambridge ")
    assert o["company"]  == "ARM"
    assert o["currency"] == "GBP"
    assert o["city"]     == "Cambridge"


def test_parse_invalid_format():
    with pytest.raises(ValueError):
        parse_offer_str("only,four,fields,here")


def test_parse_uppercase_currency():
    o = parse_offer_str("Co,eur,100000,0,10,Berlin")
    assert o["currency"] == "EUR"


# ── enrich ───────────────────────────────────────────────────────────────────

def test_enrich_bonus_calculation():
    o = enrich(_offer(base=100_000, equity=0, bonus_pct=20))
    assert o["bonus"] == 20_000
    assert o["total"] == 120_000


def test_enrich_total():
    o = enrich(_offer(base=100_000, equity=10_000, bonus_pct=10))
    assert o["total"] == 120_000


def test_enrich_usd_no_adjustment():
    o = enrich(_offer(currency="USD", base=100_000, equity=0, bonus_pct=0, city="New York"))
    assert o["adj_usd"] == pytest.approx(100_000)


def test_enrich_chf_adjusts():
    o = enrich(_offer(currency="CHF", base=100_000, equity=0, bonus_pct=0, city="Zurich"))
    expected = 100_000 * FX["CHF"] * (100 / COL["Zurich"])
    assert o["adj_usd"] == pytest.approx(expected)


def test_enrich_unknown_city_uses_default():
    o = enrich(_offer(city="UnknownCity"))
    assert o["adj_usd"] > 0


def test_enrich_inr():
    o = enrich(_offer(currency="INR", base=4_000_000, equity=0, bonus_pct=0, city="Bangalore"))
    expected = 4_000_000 * FX["INR"] * (100 / COL["Bangalore"])
    assert o["adj_usd"] == pytest.approx(expected)


def test_sort_by_total():
    offers = [
        enrich(_offer(base=100_000, equity=0, bonus_pct=0)),
        enrich(_offer(base=200_000, equity=0, bonus_pct=0)),
        enrich(_offer(base=150_000, equity=0, bonus_pct=0)),
    ]
    ranked = sorted(offers, key=lambda x: x["total"], reverse=True)
    assert ranked[0]["total"] == 200_000
    assert ranked[-1]["total"] == 100_000
