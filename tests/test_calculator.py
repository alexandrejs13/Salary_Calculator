from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engines.calculator import (  # noqa: E402
    calculate_compensation,
    inss_br,
    irrf_br,
)


@pytest.mark.parametrize("country", ["br", "us", "ca"])
def test_calculation_returns_positive_totals(country):
    res = calculate_compensation(
        country,
        {
            "base_salary": 5000,
            "other_additions": 500,
            "bonus_percent": 10,
            "dependents": 1,
        },
    )
    assert res.monthly_gross > 0
    assert res.net_monthly > 0
    assert res.total_comp > 0


def test_bonus_value_respects_percentage():
    res = calculate_compensation("br", {"base_salary": 4000, "bonus_percent": 25})
    expected_bonus = 4000 * 13.33 * 0.25
    assert pytest.approx(res.bonus_value, rel=0.05) == expected_bonus


def test_brazil_progressive_inss_and_irrf_applied():
    base = 8000.0
    dependents = 2
    previd_priv = 500.0
    inputs = {
        "base_salary": base,
        "other_additions": 0,
        "bonus_percent": 0,
        "dependents": dependents,
        "alimony": 0,
        "other_discounts": 0,
        "pension_employee": previd_priv,
    }
    res = calculate_compensation("br", inputs)
    expected_inss = inss_br(base)
    expected_irrf = irrf_br(base, dependents, 0, previd_priv)
    expected_net = base - expected_inss - expected_irrf - previd_priv
    assert pytest.approx(res.net_monthly, rel=1e-3) == expected_net
    fgts = next(val for name, val in res.extras["benefits_monthly"] if name == "FGTS")
    assert pytest.approx(fgts, rel=1e-3) == base * 0.08


def test_chile_afp_and_salud_applied():
    base = 2000.0
    afp_rate = 0.1
    inputs = {
        "base_salary": base,
        "other_additions": 0,
        "bonus_percent": 0,
        "afp_rate": afp_rate,
    }
    res = calculate_compensation("cl", inputs)
    social_security_expected = base * (afp_rate + 0.07)
    income_expected = (base - social_security_expected) * 0.1
    net_expected = base - social_security_expected - income_expected
    assert pytest.approx(res.net_monthly, rel=1e-3) == net_expected
    afp_benefit = next(val for name, val in res.extras["benefits_monthly"] if "AFP" in name)
    assert pytest.approx(afp_benefit, rel=1e-3) == base * afp_rate


def test_usa_fica_and_dependents_reduction():
    base = 6000.0
    dependents = 2
    inputs = {
        "base_salary": base,
        "other_additions": 0,
        "bonus_percent": 0,
        "dependents": dependents,
    }
    res = calculate_compensation("us", inputs)
    ss_base = min(base, 14050)
    ss = ss_base * 0.062
    medicare = base * 0.0145
    expected_social = ss + medicare
    expected_income = (base - expected_social - dependents * 300) * 0.12
    net_expected = base - expected_social - expected_income
    assert pytest.approx(res.net_monthly, rel=1e-3) == net_expected


def test_inss_br_respects_ceiling():
    base_high = 20000.0
    capped = inss_br(base_high)
    capped_expected = inss_br(7786.02)
    assert pytest.approx(capped, rel=1e-3) == capped_expected


@pytest.mark.parametrize(
    "code,base,expected_label",
    [
        ("co", 4000.0, "Fundo de Pensão"),
        ("mx", 5000.0, "AFORE (estimado)"),
        ("ca", 4500.0, "RRSP / Group RRSP (empregado)"),
    ],
)
def test_country_specific_benefits_present(code, base, expected_label):
    res = calculate_compensation(code, {"base_salary": base, "bonus_percent": 0})
    labels = [name for name, _ in res.extras["benefits_monthly"]]
    assert expected_label in labels
