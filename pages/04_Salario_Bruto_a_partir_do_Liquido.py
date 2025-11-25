import streamlit as st

from engines.calculator import CURRENCY_SYMBOL, calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.i18n import t
from engines.tables_renderer import render_three_column_table
from engines.ui import init_page


def estimate_gross(country_code: str, target_net: float, dependents: int) -> float:
    low, high = 0.0, max(target_net * 3, 2000)
    for _ in range(30):
        mid = (low + high) / 2
        res = calculate_compensation(country_code, {"base_salary": mid, "dependents": dependents})
        if res.net_monthly > target_net:
            high = mid
        else:
            low = mid
    return high


def main():
    translations = init_page("page_04_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    flag_map = {"br": "🇧🇷", "cl": "🇨🇱", "ar": "🇦🇷", "co": "🇨🇴", "mx": "🇲🇽", "us": "🇺🇸", "ca": "🇨🇦"}
    current_code = st.session_state.get("page4_country_code", "br")
    current_cfg = COUNTRIES.get(current_code, DEFAULT_COUNTRY)
    st.markdown(
        "<div class='title-row'>"
        f"<h1>{translations.get('page_04_title', 'Salário Bruto a partir do Líquido')}</h1>"
        f"<span class='title-flag'>{flag_map.get(current_cfg.code, '')}</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:6px; border-top: 3px solid #0F4F59;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='title-card'>{translations.get('parameters_title', 'Parâmetros de cálculo da remuneração')}</div>",
        unsafe_allow_html=True,
    )

    selected_country = st.selectbox(
        translations.get("country_label", "País"),
        country_names,
        index=0,
        key="page4_country_select",
    )
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    st.session_state["page4_country_code"] = country_cfg.code

    target_net = st.number_input(
        t(translations, "salary_net_target"),
        min_value=0.0,
        step=100.0,
        key="page4_target_net",
    )
    dependents = st.number_input(
        t(translations, "dependents_label"),
        min_value=0,
        step=1,
        key="page4_dependents",
    )

    if st.button(t(translations, "reverse_button")) and target_net > 0:
        gross_needed = estimate_gross(country_cfg.code, target_net, dependents)
        result = calculate_compensation(country_cfg.code, {"base_salary": gross_needed, "dependents": dependents})
        currency = CURRENCY_SYMBOL.get(country_cfg.code, "R$")

        st.markdown("### " + translations.get("section_results", "Resultados"))
        st.markdown(
            f"- {translations.get('salary_gross_needed', 'Salário bruto necessário')}: {currency} {gross_needed:,.2f}"
        )
        st.markdown(f"- {translations.get('final_monthly', 'Líquido')} alvo: {currency} {target_net:,.2f}")

        render_three_column_table(
            translations.get("tab_monthly", "Remuneração Mensal"),
            result.monthly_rows,
            translations.get("final_monthly", "REMUNERAÇÃO MENSAL LÍQUIDA"),
            currency,
            {
                "description": translations.get("table_description", "Descrição"),
                "percent": translations.get("table_percent", "%"),
                "value": translations.get("table_value", "Valor"),
            },
        )


if __name__ == "__main__":
    main()
