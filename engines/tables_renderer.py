from typing import Dict, List

import streamlit as st


def format_currency(value: float, currency: str) -> str:
    return f"{currency} {value:,.2f}"


def _capitalize_first(text: str) -> str:
    if not text:
        return text
    lowered = text.lower()
    return lowered[0].upper() + lowered[1:]


def render_three_column_table(
    title: str,
    rows: List[Dict],
    final_label: str,
    currency: str,
    columns_labels: Dict[str, str],
) -> None:
    st.markdown(f"<div class='table-title'>{title}</div>", unsafe_allow_html=True)
    filtered_rows = [r for r in rows if abs(r.get("value", 0)) > 1e-9]
    final_value = sum(r["value"] for r in filtered_rows)
    table_html = ["<table class='result-table'>"]
    table_html.append(
        "<tr>"
        f"<th class='text-left' style='width:45%'>{columns_labels.get('description', 'Descrição')}</th>"
        f"<th class='text-center' style='width:15%'>{columns_labels.get('percent', '%')}</th>"
        f"<th class='text-right' style='width:40%'>{columns_labels.get('value', 'Valor')}</th>"
        "</tr>"
    )
    for row in filtered_rows:
        cls = "credit" if row.get("kind") == "credit" and row.get("value", 0) >= 0 else "debit"
        value = format_currency(row["value"], currency)
        table_html.append(
            "<tr>"
            f"<td class='text-left' style='width:45%'>{row['description']}</td>"
            f"<td class='text-center' style='width:15%'>{row['percent']}%</td>"
            f"<td class='text-right {cls}' style='width:40%'>{value}</td>"
            "</tr>"
        )
    table_html.append(
        f"<tr class='final-row'>"
        f"<td class='text-left' style='width:45%'>{_capitalize_first(final_label)}</td>"
        f"<td class='text-center' style='width:15%'></td>"
        f"<td class='text-right' style='width:40%'>{format_currency(final_value, currency)}</td>"
        f"</tr>"
    )
    table_html.append("</table>")
    st.markdown("\n".join(table_html), unsafe_allow_html=True)


def render_extra_info(extras: Dict, translations: Dict[str, str], currency: str, mode: str = "monthly") -> None:
    benefits = extras.get("benefits_monthly" if mode == "monthly" else "benefits_annual", [])
    pension = extras.get("pension_employer_monthly" if mode == "monthly" else "pension_employer_annual", 0)

    rows = list(benefits)
    if pension:
        rows.append(("Previdência Privada Empregador", pension))
    if not rows:
        return

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='table-title'>{translations.get('benefits_title', 'Benefícios e depósitos')}</div>",
        unsafe_allow_html=True,
    )
    html = ["<table class='result-table'>"]
    html.append(
        "<tr>"
        f"<th class='text-left' style='width:45%'>{translations.get('table_description', 'Descrição')}</th>"
        f"<th class='text-center' style='width:15%'>{translations.get('table_percent', '%')}</th>"
        f"<th class='text-right' style='width:40%'>{translations.get('table_value', 'Valor')}</th>"
        "</tr>"
    )
    total = 0.0
    for label, value in rows:
        total += value
        pct = (value / total * 100) if total else 0
        html.append(
            "<tr>"
            f"<td class='text-left' style='width:45%'>{label}</td>"
            f"<td class='text-center' style='width:15%'>{pct:.2f}%</td>"
            f"<td class='text-right' style='width:40%'>{format_currency(value, currency)}</td>"
            "</tr>"
        )
    html.append(
        f"<tr class='final-row'>"
        f"<td class='text-left' style='width:45%'>{translations.get('total_label', 'Total')}</td>"
        f"<td class='text-center' style='width:15%'>100%</td>"
        f"<td class='text-right' style='width:40%'>{format_currency(total, currency)}</td>"
        f"</tr>"
    )
    html.append("</table>")
    st.markdown("\n".join(html), unsafe_allow_html=True)
