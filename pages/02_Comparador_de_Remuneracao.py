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

    dest_flag = COUNTRIES.get(current_dest, DEFAULT_COUNTRY).code
    flag_emoji = {"br": "🇧🇷", "cl": "🇨🇱", "ar": "🇦🇷", "co": "🇨🇴", "mx": "🇲🇽", "us": "🇺🇸", "ca": "🇨🇦"}.get(dest_flag, "")
    st.markdown(
        "<div class='title-row'>"
        f"<h1>Comparador de Remuneração</h1>"
        f"<span class='title-flag'>{flag_emoji}</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:6px; border-top: 3px solid #0F4F59;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='title-card'>Parâmetros de cálculo da remuneração</div>", unsafe_allow_html=True)
    tab_origem, tab_destino = st.tabs(["País de origem", "País de destino"])

    with tab_origem:
        values_origin = render_country_form(current_origin, translations, prefix="origin", allow_country_select=True)
        st.session_state["page2_origin_code"] = values_origin.get("country_code", current_origin)

    with tab_destino:
        values_dest = render_country_form(current_dest, translations, prefix="dest", allow_country_select=True)
        st.session_state["page2_dest_code"] = values_dest.get("country_code", current_dest)

    st.markdown("<hr style='margin-top:6px;margin-bottom:20px'/>", unsafe_allow_html=True)

    if st.button("Comparar Remuneração"):
        origin_code = values_origin.get("country_code", current_origin)
        dest_code = values_dest.get("country_code", current_dest)
        res_origin = calculate_compensation(origin_code, values_origin)
        res_dest = calculate_compensation(dest_code, values_dest)

        # Converter valores do país de origem para a moeda do destino
        origin_to_dest_monthly = convert_amount(res_origin.net_monthly, origin_code, dest_code)
        origin_to_dest_annual = convert_amount(res_origin.net_annual, origin_code, dest_code)
        origin_to_dest_total = convert_amount(res_origin.total_comp, origin_code, dest_code)

        st.markdown("### Comparativo (valores convertidos para a moeda do destino)")
        st.table(
            {
                "Descrição": ["Remuneração mensal líquida", "Remuneração anual líquida", "Remuneração anual total"],
                "Origem (convertido)": [
                    f"{res_dest.currency} {origin_to_dest_monthly:,.2f}",
                    f"{res_dest.currency} {origin_to_dest_annual:,.2f}",
                    f"{res_dest.currency} {origin_to_dest_total:,.2f}",
                ],
                "Destino": [
                    f"{res_dest.currency} {res_dest.net_monthly:,.2f}",
                    f"{res_dest.currency} {res_dest.net_annual:,.2f}",
                    f"{res_dest.currency} {res_dest.total_comp:,.2f}",
                ],
            }
        )


if __name__ == "__main__":
    main()
