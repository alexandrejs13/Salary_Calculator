import streamlit as st

from engines.calculator import calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY
from engines.forms import render_country_form
from engines.i18n import t
from engines.tables_renderer import render_extra_info, render_three_column_table
from engines.ui import init_page, render_title_with_flag


def main():
    translations = init_page("page_01_title")
    current_code = st.session_state.get("page1_country_code", "br")
    country_cfg = COUNTRIES.get(current_code, DEFAULT_COUNTRY)

    render_title_with_flag(translations, country_cfg)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("#### Parâmetros de cálculo da remuneração", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:0;margin-bottom:12px'/>", unsafe_allow_html=True)

    values = render_country_form(country_cfg.code, translations, allow_country_select=True)
    st.session_state["page1_country_code"] = values.get("country_code", current_code)

    if st.button(t(translations, "calculate_button")):
        result = calculate_compensation(values.get("country_code", country_cfg.code), values)
        tabs = st.tabs(
            [
                translations.get("tab_monthly", "Remuneração Mensal"),
                translations.get("tab_annual", "Remuneração Anual"),
                translations.get("tab_composition", "Composição"),
            ]
        )

        with tabs[0]:
            render_three_column_table(
                translations.get("tab_monthly", "Remuneração Mensal"),
                result.monthly_rows,
                translations.get("final_monthly", "REMUNERAÇÃO MENSAL LÍQUIDA"),
                result.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )
            render_extra_info(result.extras, translations, result.currency, mode="monthly")
        with tabs[1]:
            render_three_column_table(
                translations.get("tab_annual", "Remuneração Anual"),
                result.annual_rows,
                translations.get("final_annual", "REMUNERAÇÃO ANUAL LÍQUIDA"),
                result.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )
            render_extra_info(result.extras, translations, result.currency, mode="annual")
        with tabs[2]:
            render_three_column_table(
                translations.get("tab_composition", "Composição"),
                result.composition_rows,
                translations.get("final_total_comp", "TOTAL REMUNERAÇÃO ANUAL"),
                result.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )


if __name__ == "__main__":
    main()
