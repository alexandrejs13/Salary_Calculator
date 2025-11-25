import streamlit as st

from engines.calculator import calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY
from engines.forms import render_country_form
from engines.i18n import t
from engines.ui import init_page


# Conversão simplificada (fator para moeda base fixa)
CURRENCY_RATE = {
    "br": 1.0,
    "cl": 1.0,
    "ar": 1.0,
    "co": 1.0,
    "mx": 1.0,
    "us": 5.0,
    "ca": 4.5,
}


def convert_amount(amount: float, code_from: str, code_to: str) -> float:
    rate_from = CURRENCY_RATE.get(code_from, 1.0)
    rate_to = CURRENCY_RATE.get(code_to, 1.0)
    if rate_to == 0:
        return amount
    return amount * (rate_from / rate_to)


def main():
    translations = init_page("page_02_title")
    current_origin = st.session_state.get("page2_origin_code", "br")
    current_dest = st.session_state.get("page2_dest_code", "us")

    flag_map = {"br": "🇧🇷", "cl": "🇨🇱", "ar": "🇦🇷", "co": "🇨🇴", "mx": "🇲🇽", "us": "🇺🇸", "ca": "🇨🇦"}
    flag_origin = flag_map.get(current_origin, "")
    flag_dest = flag_map.get(current_dest, "")
    st.markdown(
        "<div class='title-row'>"
        f"<h1>Comparador de Remuneração</h1>"
        f"<span style='display:flex; gap:8px; align-items:center;'>"
        f"<span class='title-flag'>{flag_origin}</span>"
        f"<span class='title-flag'>{flag_dest}</span>"
        "</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:6px; border-top: 3px solid #0F4F59;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    tab_origem, tab_destino = st.tabs(["País de origem", "País de destino"])

    with tab_origem:
        st.markdown("<div class='title-card'>Parâmetros de cálculo da remuneração</div>", unsafe_allow_html=True)
        values_origin = render_country_form(current_origin, translations, prefix="origin", allow_country_select=True)
        st.session_state["page2_origin_code"] = values_origin.get("country_code", current_origin)

    with tab_destino:
        st.markdown("<div class='title-card'>Parâmetros de cálculo da remuneração</div>", unsafe_allow_html=True)
        values_dest = render_country_form(current_dest, translations, prefix="dest", allow_country_select=True)
        st.session_state["page2_dest_code"] = values_dest.get("country_code", current_dest)

    st.markdown("<hr style='margin-top:6px;margin-bottom:20px'/>", unsafe_allow_html=True)

    if st.button("Comparar Remuneração"):
        origin_code = values_origin.get("country_code", current_origin)
        dest_code = values_dest.get("country_code", current_dest)
        res_origin = calculate_compensation(origin_code, values_origin)
        res_dest = calculate_compensation(dest_code, values_dest)

        # Converter valores do país de origem para a moeda do destino (se diferente)
        origin_to_dest_monthly = convert_amount(res_origin.net_monthly, origin_code, dest_code)
        origin_to_dest_annual = convert_amount(res_origin.net_annual, origin_code, dest_code)
        origin_to_dest_total = convert_amount(res_origin.total_comp, origin_code, dest_code)

        rows = [
            ("Remuneração mensal líquida", origin_to_dest_monthly, res_dest.net_monthly),
            ("Remuneração anual líquida", origin_to_dest_annual, res_dest.net_annual),
            ("Remuneração anual total", origin_to_dest_total, res_dest.total_comp),
        ]

        table_html = ["<table class='result-table'>"]
        table_html.append("<tr><th>Descrição</th><th>Origem</th><th>Destino</th><th>Variação</th><th>Variação %</th></tr>")
        for desc, o, d in rows:
            diff = d - o
            pct = (diff / o * 100) if o else 0
            cls = "credit" if diff > 0 else "debit" if diff < 0 else ""
            pct_txt = f"{pct:,.2f}%" if o else "0.00%"
            var_txt = f"{res_dest.currency} {abs(diff):,.2f}"
            if diff > 0:
                var_txt = f"+ {var_txt}"
            elif diff < 0:
                var_txt = f"- {var_txt}"
            table_html.append(
                "<tr>"
                f"<td>{desc}</td>"
                f"<td style='text-align:right'>{res_dest.currency} {o:,.2f}</td>"
                f"<td style='text-align:right'>{res_dest.currency} {d:,.2f}</td>"
                f"<td style='text-align:right' class='{cls}'>{var_txt}</td>"
                f"<td style='text-align:right' class='{cls}'>{pct_txt}</td>"
                "</tr>"
            )
        table_html.append("</table>")

        st.markdown("### Comparativo")
        st.markdown("\n".join(table_html), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
