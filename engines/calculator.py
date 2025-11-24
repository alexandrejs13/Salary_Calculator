from dataclasses import dataclass
from typing import Dict, List, Tuple

from .countries import COUNTRIES


# Basic currency mapping for display purposes
CURRENCY_SYMBOL = {
    "br": "R$",
    "cl": "CLP$",
    "ar": "ARS$",
    "co": "COP$",
    "mx": "MXN$",
    "us": "US$",
    "ca": "CA$",
}


@dataclass
class CalculationResult:
    monthly_rows: List[Dict]
    annual_rows: List[Dict]
    composition_rows: List[Dict]
    net_monthly: float
    net_annual: float
    total_comp: float
    bonus_value: float
    extras: Dict
    currency: str
    monthly_gross: float
    annual_gross: float


def progressive_tax(base: float, brackets: List[Tuple[float, float, float]]) -> float:
    """Apply progressive tax brackets [(limit, rate, deduction)]"""
    tax = 0.0
    for limit, rate, deduction in brackets:
        if base <= limit:
            tax = base * rate - deduction
            break
    else:
        # last bracket (infinite)
        limit, rate, deduction = brackets[-1]
        tax = base * rate - deduction
    return max(tax, 0.0)


def inss_br(base: float) -> float:
    # Simplified 2024/2025 brackets
    brackets = [
        (1412.00, 0.075, 0.0),
        (2666.68, 0.09, 21.18),
        (4000.03, 0.12, 91.0),
        (7786.02, 0.14, 163.82),
    ]
    return progressive_tax(base, brackets)


def irrf_br(base: float, dependents: int, pensao: float) -> float:
    deduction_dep = 189.59 * dependents
    taxable = max(base - deduction_dep - pensao - inss_br(base), 0)
    brackets = [
        (2112.0, 0.0, 0.0),
        (2826.65, 0.075, 158.4),
        (3751.05, 0.15, 370.4),
        (4664.68, 0.225, 651.73),
        (9999999, 0.275, 884.96),
    ]
    return progressive_tax(taxable, brackets)


def compute_country_taxes(code: str, gross_monthly: float, bonus_value: float, inputs: Dict) -> Dict:
    """Return dict with social_security, income_tax, employer_cost and info extras."""
    dependents = float(inputs.get("dependents") or 0)
    other_discounts = float(inputs.get("other_discounts") or 0)
    alimony = float(inputs.get("alimony") or 0)
    pension_employee = float(inputs.get("pension_employee") or 0)
    pension_employer = float(inputs.get("pension_employer") or 0)
    addl_withholding = float(inputs.get("additional_withholding") or 0)

    social_security = 0.0
    income_tax = 0.0
    employer_cost = 0.0
    notes: List[str] = []
    currency = CURRENCY_SYMBOL.get(code, "R$")

    if code == "br":
        social_security = inss_br(gross_monthly)
        income_tax = irrf_br(gross_monthly + bonus_value / 12, int(dependents), alimony)
        employer_cost = gross_monthly * 0.2 + gross_monthly * 0.08
        notes.append("INSS progressivo e IRRF simplificados conforme faixas atuais.")
    elif code == "cl":
        afp_rate = float(inputs.get("afp_rate") or 0.1)
        salud_rate = 0.07
        social_security = gross_monthly * (afp_rate + salud_rate)
        income_tax = max((gross_monthly - social_security) * 0.1, 0)
        employer_cost = gross_monthly * 0.024  # seguro cesantía médio
        notes.append("AFP + Salud conforme seleção; imposto linear ilustrativo.")
    elif code == "ar":
        jubilacion = float(inputs.get("jubilacion") or 0.11)
        obra_social = float(inputs.get("obra_social") or 0.03)
        social_security = gross_monthly * (jubilacion + obra_social)
        income_tax = max((gross_monthly - social_security) * 0.15, 0)
        employer_cost = gross_monthly * 0.25
        notes.append("Jubilación + Obra Social; Ganancias aproximado.")
    elif code == "co":
        pension = gross_monthly * 0.04
        salud = gross_monthly * 0.04
        solidarity = float(inputs.get("solidarity_fund") or 0)
        social_security = pension + salud + solidarity
        income_tax = max((gross_monthly - social_security) * 0.1, 0)
        employer_cost = gross_monthly * 0.30
        notes.append("Saúde e pensão de 4%; imposto linear ilustrativo.")
    elif code == "mx":
        cuota_obrera = float(inputs.get("cuota_obrera") or 0.04)
        riesgo = float(inputs.get("riesgo_trabajo") or 0.01)
        social_security = gross_monthly * (cuota_obrera + riesgo)
        income_tax = max((gross_monthly - social_security) * 0.15, 0)
        employer_cost = gross_monthly * 0.20
        notes.append("IMSS simplificado e ISR linear para ilustração.")
    elif code == "us":
        ss = gross_monthly * 0.062
        medicare = gross_monthly * 0.0145
        social_security = ss + medicare
        income_tax = max((gross_monthly - social_security - dependents * 300) * 0.12, 0)
        employer_cost = ss + medicare
        notes.append("FICA (6.2% + 1.45%) e imposto federal linear.")
    elif code == "ca":
        cpp = gross_monthly * 0.0595
        ei = gross_monthly * 0.0163
        social_security = cpp + ei
        income_tax = max((gross_monthly - social_security - dependents * 200) * 0.15, 0)
        employer_cost = gross_monthly * 0.075
        notes.append("CPP + EI padrão; imposto linear.")
    else:
        social_security = gross_monthly * 0.08
        income_tax = gross_monthly * 0.12
        employer_cost = gross_monthly * 0.10

    social_security += pension_employee
    employer_cost += pension_employer
    income_tax += addl_withholding
    other_deds = other_discounts + alimony

    return {
        "social_security": social_security,
        "income_tax": income_tax,
        "employer_cost": employer_cost,
        "other_deductions": other_deds,
        "notes": notes,
        "currency": currency,
    }


def calculate_compensation(country_code: str, inputs: Dict) -> CalculationResult:
    cfg = COUNTRIES.get(country_code, COUNTRIES["br"])
    base_salary = float(inputs.get("base_salary") or 0)
    other_additions = float(inputs.get("other_additions") or 0)
    bonus_percent = float(inputs.get("bonus_percent") or 0)

    monthly_gross = base_salary + other_additions
    annual_gross = monthly_gross * cfg.annual_frequency
    bonus_value = (bonus_percent / 100.0) * annual_gross
    bonus_monthly_equiv = bonus_value / cfg.annual_frequency

    tax_data = compute_country_taxes(country_code, monthly_gross, bonus_value, inputs)
    social_security = tax_data["social_security"]
    income_tax = tax_data["income_tax"]
    other_deductions = tax_data["other_deductions"]

    net_monthly = monthly_gross - social_security - income_tax - other_deductions
    net_annual = net_monthly * cfg.annual_frequency
    total_comp = annual_gross + bonus_value

    # Monthly table rows
    monthly_rows = [
        {"description": "Salário Base", "value": base_salary, "percent": _pct(base_salary, monthly_gross), "kind": "credit"},
        {"description": "Outros Adicionais", "value": other_additions, "percent": _pct(other_additions, monthly_gross), "kind": "credit"},
        {"description": "Imposto de Renda", "value": -income_tax, "percent": _pct(income_tax, monthly_gross), "kind": "debit"},
        {"description": "Previdência Social", "value": -social_security, "percent": _pct(social_security, monthly_gross), "kind": "debit"},
        {"description": "Outros Descontos", "value": -other_deductions, "percent": _pct(other_deductions, monthly_gross), "kind": "debit"},
    ]

    annual_rows = [
        {"description": "Salário Anual Bruto", "value": annual_gross, "percent": 100.0, "kind": "credit"},
        {"description": "Impostos Anuais", "value": -(income_tax * cfg.annual_frequency), "percent": _pct(income_tax * cfg.annual_frequency, annual_gross), "kind": "debit"},
        {"description": "Contribuições Previdenciárias", "value": -(social_security * cfg.annual_frequency), "percent": _pct(social_security * cfg.annual_frequency, annual_gross), "kind": "debit"},
    ]

    composition_rows = [
        {"description": "Salário Anual", "value": annual_gross, "percent": _pct(annual_gross, total_comp), "kind": "credit"},
        {"description": "Bônus Anual", "value": bonus_value, "percent": _pct(bonus_value, total_comp), "kind": "credit"},
    ]

    extras = {
        "fgts": monthly_gross * 0.08 * cfg.annual_frequency if country_code == "br" else 0,
        "pension_private": (float(inputs.get("pension_employee") or 0) + float(inputs.get("pension_employer") or 0)) * cfg.annual_frequency,
        "employer_cost": tax_data["employer_cost"] * cfg.annual_frequency,
        "notes": tax_data["notes"],
    }

    return CalculationResult(
        monthly_rows=monthly_rows,
        annual_rows=annual_rows,
        composition_rows=composition_rows,
        net_monthly=net_monthly,
        net_annual=net_annual,
        total_comp=total_comp,
        bonus_value=bonus_value,
        extras=extras,
        currency=tax_data["currency"],
        monthly_gross=monthly_gross,
        annual_gross=annual_gross,
    )


def _pct(value: float, total: float) -> float:
    if total == 0:
        return 0.0
    return round((abs(value) / total) * 100, 1)
