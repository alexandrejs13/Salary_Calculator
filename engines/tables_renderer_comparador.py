from typing import Dict

import streamlit as st

from .calculator import CalculationResult
from .tables_renderer import format_currency


def render_comparative_table(
    title: str,
    scenario_a: CalculationResult,
    scenario_b: CalculationResult,
    translations: Dict[str, str],
) -> None:
    currency = scenario_a.currency
    rows = [
        ("Remuneração mensal bruta", scenario_a.monthly_gross, scenario_b.monthly_gross),
        ("Remuneração mensal líquida", scenario_a.net_monthly, scenario_b.net_monthly),
        ("Remuneração anual total", scenario_a.total_comp, scenario_b.total_comp),
        ("Bônus anual", scenario_a.bonus_value, scenario_b.bonus_value),
    ]

    table_html = ["<table class='result-table'>"]
    table_html.append(
        "<tr>"
        f"<th>{translations.get('table_description', 'Descrição')}</th>"
        "<th>Cenário A</th>"
        "<th>Cenário B</th>"
        "<th>Dif. Absoluta</th>"
        "<th>Dif. %</th>"
        "</tr>"
    )

    for desc, val_a, val_b in rows:
        diff_abs = val_b - val_a
        diff_pct = (diff_abs / val_a * 100) if val_a else 0
        cls = "credit" if diff_abs >= 0 else "debit"
        diff_pct_display = f"{diff_pct:,.1f}%" if val_a else "—"
        table_html.append(
            "<tr>"
            f"<td>{desc}</td>"
            f"<td>{format_currency(val_a, currency)}</td>"
            f"<td>{format_currency(val_b, currency)}</td>"
            f"<td class='{cls}'>{format_currency(diff_abs, currency)}</td>"
            f"<td class='{cls}'>{diff_pct_display}</td>"
            "</tr>"
        )

    table_html.append(
        "<tr class='final-row'>"
        f"<td>{translations.get('final_total_comp', 'TOTAL REMUNERAÇÃO ANUAL')}</td>"
        f"<td>{format_currency(scenario_a.total_comp, currency)}</td>"
        f"<td>{format_currency(scenario_b.total_comp, currency)}</td>"
        f"<td>{format_currency(scenario_b.total_comp - scenario_a.total_comp, currency)}</td>"
        f"<td></td>"
        "</tr>"
    )
    table_html.append("</table>")

    st.markdown(f"**{title}**")
    st.markdown("\n".join(table_html), unsafe_allow_html=True)
