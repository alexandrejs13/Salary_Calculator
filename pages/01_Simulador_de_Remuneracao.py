import streamlit as st

from engines.calculator import calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY
from engines.forms import render_country_form
from engines.i18n import t
from engines.tables_renderer import render_three_column_table
from engines.ui import init_page, render_title_with_flag


def main():
    translations = init_page("page_01_title")
    current_code = st.session_state.get("page1_country_code", "br")
    country_cfg = COUNTRIES.get(current_code, DEFAULT_COUNTRY)
    render_title_with_flag(translations, country_cfg)

    values = render_country_form(country_cfg.code, translations, allow_country_select=True)
    st.session_state["page1_country_code"] = values.get("country_code", current_code)

    if st.button(t(translations, "calculate_button"), type="primary"):
        selected_cfg = COUNTRIES.get(values.get("country_code", current_code), country_cfg)
        result = calculate_compensation(selected_cfg.code, values)

        tab1, tab2, tab3 = st.tabs([
            translations.get("tab_monthly", "Remuneração Mensal"),
            translations.get("tab_annual", "Remuneração Anual"),
            translations.get("tab_composition", "Composição da Remuneração"),
        ])

        with tab1:
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

        with tab2:
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

        with tab3:
            render_three_column_table(
                translations.get("tab_composition", "Composição da Remuneração"),
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
