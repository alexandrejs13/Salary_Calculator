import streamlit as st

from engines.calculator import CURRENCY_SYMBOL, calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.i18n import t
from engines.ui import init_page, render_title_with_flag


def main():
    translations = init_page("page_07_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    selected_country = st.selectbox("País", country_names, index=0, key="page7_country_select")
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    render_title_with_flag(translations, country_cfg)

    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(translations.get("calculate_button", "Calcular"), key="page7_button"):
        res = calculate_compensation(country_cfg.code, {"base_salary": salary, "bonus_percent": bonus, "other_additions": extras})
        currency = CURRENCY_SYMBOL.get(country_cfg.code, "R$")

        st.markdown("### " + translations.get("explanation_title", "Explicação automática"))
        st.markdown(
            f"O salário informado sofre incidência de contribuições previdenciárias e imposto de renda do país selecionado. "
            f"O líquido estimado é {currency} {res.net_monthly:,.2f} por mês."
        )
        st.markdown(
            f"- Carga do empregado: {((salary - res.net_monthly) / salary * 100 if salary else 0):.1f}%"
        )
        st.markdown(f"- Carga do empregador (estimada): {res.extras.get('employer_cost',0)/ (salary*12) *100 if salary else 0:.1f}%")


if __name__ == "__main__":
    main()
