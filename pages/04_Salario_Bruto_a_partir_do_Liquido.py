import streamlit as st

from engines.calculator import CURRENCY_SYMBOL, calculate_compensation
from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.i18n import t
from engines.tables_renderer import render_three_column_table
from engines.ui import init_page, render_title_with_flag


def estimate_gross(country_code: str, target_net: float) -> float:
    low, high = 0.0, max(target_net * 3, 2000)
    for _ in range(30):
        mid = (low + high) / 2
        res = calculate_compensation(country_code, {"base_salary": mid})
        if res.net_monthly > target_net:
            high = mid
        else:
            low = mid
    return high


def main():
    translations = init_page("page_04_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    selected_country = st.selectbox(
        translations.get("country_label", "País"),
        country_names,
        index=0,
        key="page4_country_select",
    )
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    render_title_with_flag(translations, country_cfg)

    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    target_net = st.number_input(
        t(translations, "salary_net_target"),
        min_value=0.0,
        step=100.0,
        key="page4_target_net",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(t(translations, "reverse_button")) and target_net > 0:
        gross_needed = estimate_gross(country_cfg.code, target_net)
        result = calculate_compensation(country_cfg.code, {"base_salary": gross_needed})
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
