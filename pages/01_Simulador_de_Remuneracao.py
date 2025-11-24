import streamlit as st

from engines.calculator import calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.forms import render_country_form
from engines.i18n import t
from engines.tables_renderer import render_three_column_table
from engines.ui import init_page, render_title_with_flag


def main():
    translations = init_page("page_01_title")
    
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    selected_country = st.selectbox(
        translations.get("country_label", "País"),
        country_names,
        index=0,
        key="page1_country_select",
        help=t(translations, "country_select_placeholder"),
    )
    
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    render_title_with_flag(translations, country_cfg)

    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    st.markdown(
        f"<h4 class='section-title'>{translations.get('calc_params', 'Parâmetros de cálculo da remuneração')}</h4>",
        unsafe_allow_html=True,
    )
    
    values = render_country_form(country_cfg.code, translations)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(t(translations, "calculate_button"), type="primary"):
        result = calculate_compensation(country_cfg.code, values)
        
        st.success("✅ Cálculo realizado com sucesso!")
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs([
            translations.get("tab_monthly", "Remuneração Mensal"),
            translations.get("tab_yearly", "Remuneração Anual"),
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
                translations.get("tab_yearly", "Remuneração Anual"),
                result.yearly_rows,
                translations.get("final_yearly", "REMUNERAÇÃO ANUAL LÍQUIDA"),
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
                translations.get("final_composition", "TOTAL REMUNERAÇÃO ANUAL"),
                result.currency,
                {
                    "description": translations.get("table_description", "Descrição"),
                    "percent": translations.get("table_percent", "%"),
                    "value": translations.get("table_value", "Valor"),
                },
            )
        
        if result.additional_info:
            st.markdown(f"### {translations.get('additional_info', 'Informações Adicionais')}")
            info_html = "<ul class='info-adicionais'>"
            for item in result.additional_info:
                info_html += f"<li><strong>{item['label']}:</strong> {item['value']}</li>"
            info_html += "</ul>"
            st.markdown(info_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
