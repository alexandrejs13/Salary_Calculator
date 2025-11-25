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
    st.markdown(f"**{title}**")
    filtered_rows = [r for r in rows if abs(r.get("value", 0)) > 1e-9]
    final_value = sum(r["value"] for r in filtered_rows)
    table_html = ["<table class='result-table'>"]
    table_html.append(
        "<tr>"
        f"<th class='text-left'>{columns_labels.get('description', 'Descrição')}</th>"
        f"<th class='text-center'>{columns_labels.get('percent', '%')}</th>"
        f"<th class='text-right'>{columns_labels.get('value', 'Valor')}</th>"
        "</tr>"
    )
    for row in filtered_rows:
        cls = "credit" if row.get("kind") == "credit" and row.get("value", 0) >= 0 else "debit"
        value = format_currency(row["value"], currency)
        table_html.append(
            "<tr>"
            f"<td class='text-left'>{row['description']}</td>"
            f"<td class='text-center'>{row['percent']}%</td>"
            f"<td class='text-right {cls}'>{value}</td>"
            "</tr>"
        )
    table_html.append(
        f"<tr class='final-row'><td class='text-left'>{_capitalize_first(final_label)}</td><td></td><td class='text-right'>{format_currency(final_value, currency)}</td></tr>"
    )
    table_html.append("</table>")
    st.markdown("\n".join(table_html), unsafe_allow_html=True)


def render_extra_info(extras: Dict, translations: Dict[str, str], currency: str, mode: str = "monthly") -> None:
    benefits = extras.get("benefits_monthly" if mode == "monthly" else "benefits_annual", [])
    pension = extras.get("pension_employer_monthly" if mode == "monthly" else "pension_employer_annual", 0)

    if benefits or pension:
        st.markdown("<br/>", unsafe_allow_html=True)
    for label, value in benefits:
        st.markdown(f"- {label}: {format_currency(value, currency)}")
    if pension:
        st.markdown(f"- Previdência Privada Empregador: {format_currency(pension, currency)}")
