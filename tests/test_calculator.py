from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engines.calculator import calculate_compensation  # noqa: E402


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
