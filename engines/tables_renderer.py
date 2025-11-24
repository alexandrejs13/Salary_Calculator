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
        f"<th>{columns_labels.get('description', 'Descrição')}</th>"
        f"<th>{columns_labels.get('percent', '%')}</th>"
        f"<th>{columns_labels.get('value', 'Valor')}</th>"
        "</tr>"
    )
    for row in filtered_rows:
        cls = "credit" if row.get("kind") == "credit" and row.get("value", 0) >= 0 else "debit"
        value = format_currency(row["value"], currency)
        table_html.append(
            "<tr>"
            f"<td>{row['description']}</td>"
            f"<td>{row['percent']}%</td>"
            f"<td class='{cls}'>{value}</td>"
            "</tr>"
        )
    table_html.append(
        f"<tr class='final-row'><td>{_capitalize_first(final_label)}</td><td></td><td>{format_currency(final_value, currency)}</td></tr>"
    )
    table_html.append("</table>")
    st.markdown("\n".join(table_html), unsafe_allow_html=True)


def render_extra_info(extras: Dict, translations: Dict[str, str], currency: str, mode: str = "monthly") -> None:
    fgts_monthly = extras.get("fgts_monthly", 0)
    fgts_annual = extras.get("fgts_annual", 0)
    pension_emp_monthly = extras.get("pension_employer_monthly", 0)
    pension_emp_annual = extras.get("pension_employer_annual", 0)

    if mode == "monthly":
        fgts = fgts_monthly
        pension = pension_emp_monthly
    else:
        fgts = fgts_annual
        pension = pension_emp_annual

    if fgts or pension:
        st.markdown("<br/>", unsafe_allow_html=True)
    if fgts:
        st.markdown(f"- FGTS: {format_currency(fgts, currency)}")
    if pension:
        st.markdown(f"- Previdência Privada Empregador: {format_currency(pension, currency)}")
