import streamlit as st

from engines.calculator import CURRENCY_SYMBOL, calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.i18n import t
from engines.ui import init_page


def main():
    translations = init_page("page_07_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    flag_map = {"br": "🇧🇷", "cl": "🇨🇱", "ar": "🇦🇷", "co": "🇨🇴", "mx": "🇲🇽", "us": "🇺🇸", "ca": "🇨🇦"}
    current_code = st.session_state.get("page7_country_code", "br")
    current_cfg = COUNTRIES.get(current_code, DEFAULT_COUNTRY)
    st.markdown(
        "<div class='title-row'>"
        f"<h1>Explicador Automático</h1>"
        f"<span class='title-flag'>{flag_map.get(current_cfg.code, '')}</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:6px; border-top: 3px solid #0F4F59;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='title-card'>Parâmetros de cálculo da remuneração</div>", unsafe_allow_html=True)

    selected_country = st.selectbox("País", country_names, index=0, key="page7_country_select")
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    st.session_state["page7_country_code"] = country_cfg.code

    salary = st.number_input(
        t(translations, "base_salary_label"),
        min_value=0.0,
        step=100.0,
        key="page7_salary",
    )
    bonus = st.number_input(
        t(translations, "bonus_percent_label"),
        min_value=0.0,
        step=1.0,
        key="page7_bonus",
    )
    extras = st.number_input(
        t(translations, "other_additions_label"),
        min_value=0.0,
        step=50.0,
        key="page7_extras",
    )

    if st.button(translations.get("calculate_button", "Calcular"), key="page7_button"):
        res = calculate_compensation(country_cfg.code, {"base_salary": salary, "bonus_percent": bonus, "other_additions": extras})
        currency = CURRENCY_SYMBOL.get(country_cfg.code, "R$")

        st.markdown("### " + translations.get("explanation_title", "Explicação automática"))
        carga_empregado = ((salary + extras - res.net_monthly) / (salary + extras) * 100) if (salary + extras) else 0
        carga_empregador = (res.extras.get("employer_cost", 0) / ((salary + extras) * 12) * 100) if (salary + extras) else 0
        st.markdown(
            f"O salário informado sofre incidência de contribuições e impostos locais. "
            f"O líquido estimado é **{currency} {res.net_monthly:,.2f}/mês**."
        )
        st.markdown(f"- Carga do empregado: {carga_empregado:.1f}%")
        st.markdown(f"- Carga do empregador (estimada): {carga_empregador:.1f}%")

        table = [
            ("Salário bruto mensal", f"{currency} {res.monthly_gross:,.2f}"),
            ("Impostos/Previdência (empregado)", f"{currency} {(res.monthly_gross - res.net_monthly):,.2f}"),
            ("Líquido mensal", f"{currency} {res.net_monthly:,.2f}"),
            ("Custo empregador (mensal)", f"{currency} {res.extras.get('employer_cost_monthly',0):,.2f}"),
        ]
        html = ["<table class='result-table'>"]
        html.append("<tr><th class='text-left'>Item</th><th class='text-right'>Valor</th></tr>")
        for label, val in table:
            html.append(f"<tr><td class='text-left'>{label}</td><td class='text-right'>{val}</td></tr>")
        html.append("</table>")
        st.markdown("\n".join(html), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
