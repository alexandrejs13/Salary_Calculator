import streamlit as st

from engines.calculator import calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.forms import render_country_form
from engines.i18n import t
from engines.tables_renderer import render_three_column_table
from engines.tables_renderer_comparador import render_comparative_table
from engines.ui import init_page, render_title_with_flag


def main():
    translations = init_page("page_02_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    selected_country = st.selectbox(
        translations.get("country_label", "País"),
        country_names,
        index=0,
        key="page2_country_select",
        help=t(translations, "country_select_placeholder"),
    )
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY

    render_title_with_flag(translations, country_cfg)

    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"#### {translations.get('scenario_a', 'Cenário A')}")
        values_a = render_country_form(country_cfg.code, translations, prefix="A")
    with col_b:
        st.markdown(f"#### {translations.get('scenario_b', 'Cenário B')}")
        values_b = render_country_form(country_cfg.code, translations, prefix="B")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(t(translations, "calculate_ab_button")):
        res_a = calculate_compensation(country_cfg.code, values_a)
        res_b = calculate_compensation(country_cfg.code, values_b)

        st.markdown("### Resultados individuais")
        block1, block2 = st.columns(2)
        with block1:
            st.markdown(f"**{translations.get('scenario_a', 'Cenário A')}**")
            render_three_column_table(
                translations.get("tab_monthly", "Remuneração Mensal"),
                res_a.monthly_rows,
                translations.get("final_monthly", "REMUNERAÇÃO MENSAL LÍQUIDA"),
                res_a.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )
            render_three_column_table(
                translations.get("tab_annual", "Remuneração Anual"),
                res_a.annual_rows,
                translations.get("final_annual", "REMUNERAÇÃO ANUAL LÍQUIDA"),
                res_a.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )
            render_three_column_table(
                translations.get("tab_composition", "Composição"),
                res_a.composition_rows,
                translations.get("final_total_comp", "TOTAL REMUNERAÇÃO ANUAL"),
                res_a.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )
        with block2:
            st.markdown(f"**{translations.get('scenario_b', 'Cenário B')}**")
            render_three_column_table(
                translations.get("tab_monthly", "Remuneração Mensal"),
                res_b.monthly_rows,
                translations.get("final_monthly", "REMUNERAÇÃO MENSAL LÍQUIDA"),
                res_b.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )
            render_three_column_table(
                translations.get("tab_annual", "Remuneração Anual"),
                res_b.annual_rows,
                translations.get("final_annual", "REMUNERAÇÃO ANUAL LÍQUIDA"),
                res_b.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )
            render_three_column_table(
                translations.get("tab_composition", "Composição"),
                res_b.composition_rows,
                translations.get("final_total_comp", "TOTAL REMUNERAÇÃO ANUAL"),
                res_b.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )

        render_comparative_table(
            translations.get("compare_table_title", "Comparativo de remuneração"),
            res_a,
            res_b,
            translations,
        )


if __name__ == "__main__":
    main()
