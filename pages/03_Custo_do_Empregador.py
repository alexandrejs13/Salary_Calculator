import streamlit as st

from engines.calculator import CURRENCY_SYMBOL
from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.i18n import t
from engines.ui import init_page, render_title_with_flag


EMPLOYER_ITEMS = {
    "br": [
        ("FGTS", 0.08),
        ("INSS patronal", 0.20),
        ("Sistema S", 0.025),
        ("RAT", 0.02),
    ],
    "us": [("FICA Employer", 0.0765), ("FUTA/SUTA", 0.01)],
    "ca": [("CPP Employer", 0.0595), ("EI Employer", 0.0221)],
    "mx": [("IMSS Patronal", 0.15), ("SAR/INFONAVIT", 0.05)],
    "cl": [("Seguro Cesantía", 0.024)],
    "co": [("Seguridad Social Patronal", 0.30)],
    "ar": [("Cargas Patronales", 0.25)],
}


def main():
    translations = init_page("page_03_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    selected_country = st.selectbox(
        translations.get("country_label", "País"),
        country_names,
        index=0,
        key="page3_country_select",
    )
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY

    render_title_with_flag(translations, country_cfg)

    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    base_salary = col1.number_input(
        t(translations, "base_salary_label"),
        min_value=0.0,
        step=100.0,
        key="page3_base",
    )
    additions = col2.number_input(
        t(translations, "other_additions_label"),
        min_value=0.0,
        step=50.0,
        key="page3_additions",
    )
    col3, col4 = st.columns(2)
    bonus_percent = col3.number_input(
        t(translations, "bonus_percent_label"),
        min_value=0.0,
        step=1.0,
        key="page3_bonus",
    )
    col4.text_input(
        t(translations, "frequency_label"),
        value=str(country_cfg.annual_frequency),
        disabled=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(translations.get("calculate_button", "Calcular")):
        annual_salary = base_salary * country_cfg.annual_frequency
        annual_additions = additions * country_cfg.annual_frequency
        bonus_value = annual_salary * (bonus_percent / 100)
        total_annual = annual_salary + annual_additions + bonus_value

        st.markdown("### " + translations.get("section_employer_cost", "Custo do empregador"))
        table_html = ["<table class='result-table'>"]
        currency = CURRENCY_SYMBOL.get(country_cfg.code, "R$")
        table_html.append(
            "<tr><th>Item</th><th>% empregador</th><th>Valor anual</th><th>Valor mensal (12)</th></tr>"
        )
        for item, rate in EMPLOYER_ITEMS.get(country_cfg.code, []):
            annual_value = total_annual * rate
            monthly_value = annual_value / 12
            table_html.append(
                f"<tr><td>{item}</td><td>{rate*100:.2f}%</td><td>{currency} {annual_value:,.2f}</td><td>{currency} {monthly_value:,.2f}</td></tr>"
            )
        table_html.append(
            f"<tr class='final-row'><td>Total</td><td></td><td>{currency} {total_annual:,.2f}</td><td>{currency} {(total_annual/12):,.2f}</td></tr>"
        )
        table_html.append("</table>")
        st.markdown("\n".join(table_html), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
