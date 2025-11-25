import streamlit as st

from engines.calculator import CURRENCY_SYMBOL
from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.i18n import t
from engines.ui import init_page


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
    flag_map = {"br": "🇧🇷", "cl": "🇨🇱", "ar": "🇦🇷", "co": "🇨🇴", "mx": "🇲🇽", "us": "🇺🇸", "ca": "🇨🇦"}
    current_code = st.session_state.get("page3_country_code", "br")
    current_cfg = COUNTRIES.get(current_code, DEFAULT_COUNTRY)

    st.markdown(
        "<div class='title-row'>"
        f"<h1>Custo do Empregador</h1>"
        f"<span class='title-flag'>{flag_map.get(current_cfg.code, '')}</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:6px; border-top: 3px solid #0F4F59;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='title-card'>Parâmetros de cálculo da remuneração</div>", unsafe_allow_html=True)

    selected_country = st.selectbox(
        translations.get("country_label", "País"),
        country_names,
        index=0,
        key="page3_country_select",
    )
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    st.session_state["page3_country_code"] = country_cfg.code

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

    if st.button(translations.get("calculate_button", "Calcular")):
        annual_salary = base_salary * country_cfg.annual_frequency
        annual_additions = additions * country_cfg.annual_frequency
        bonus_value = annual_salary * (bonus_percent / 100)
        thirteenth = base_salary if country_cfg.annual_frequency > 12 else 0.0
        vacation = base_salary if country_cfg.code in ["br", "cl", "ar", "co", "mx"] else 0.0
        total_comp = annual_salary + annual_additions + bonus_value + thirteenth + vacation

        st.markdown("### " + translations.get("section_employer_cost", "Custo do empregador"))
        table_html = ["<table class='result-table'>"]
        currency = CURRENCY_SYMBOL.get(country_cfg.code, "R$")
        table_html.append(
            "<tr>"
            "<th class='text-left'>Item</th>"
            "<th class='text-center'>% empregador</th>"
            "<th class='text-right'>Valor anual</th>"
            "<th class='text-right'>Valor mensal (12)</th>"
            "</tr>"
        )
        base_rows = [
            ("Salário base (anual)", annual_salary),
            ("13º salário" if thirteenth else None, thirteenth),
            ("Férias provisionadas" if vacation else None, vacation),
            ("Bônus", bonus_value),
            ("Outros adicionais (anual)", annual_additions),
        ]
        for label, val in base_rows:
            if label:
                table_html.append(
                    f"<tr><td class='text-left'>{label}</td><td class='text-center'>—</td><td class='text-right'>{currency} {val:,.2f}</td><td class='text-right'>{currency} {(val/12):,.2f}</td></tr>"
                )

        for item, rate in EMPLOYER_ITEMS.get(country_cfg.code, []):
            annual_value = total_comp * rate
            monthly_value = annual_value / 12
            table_html.append(
                f"<tr>"
                f"<td class='text-left'>{item}</td>"
                f"<td class='text-center'>{rate*100:.2f}%</td>"
                f"<td class='text-right'>{currency} {annual_value:,.2f}</td>"
                f"<td class='text-right'>{currency} {monthly_value:,.2f}</td>"
                f"</tr>"
            )
        table_html.append(
            f"<tr class='final-row'>"
            f"<td class='text-left'>Total</td><td></td>"
            f"<td class='text-right'>{currency} {total_comp:,.2f}</td>"
        f"<td class='text-right'>{currency} {(total_comp/12):,.2f}</td>"
        f"</tr>"
        )
        table_html.append("</table>")
        st.markdown("\n".join(table_html), unsafe_allow_html=True)
        factor = country_cfg.annual_frequency
        linear_12 = total_comp * (12 / factor) if factor else total_comp
        st.markdown(
            f"**Fator anual do país:** {factor:.2f} meses. "
            f"Total anual utilizado: {currency} {total_comp:,.2f}. "
            f"Em 12 meses lineares, seria aproximadamente {currency} {linear_12:,.2f}."
        )
        if EMPLOYER_ITEMS.get(country_cfg.code):
            st.markdown("#### Incidência resumida")
            incidence_rows = []
            for item, rate in EMPLOYER_ITEMS.get(country_cfg.code, []):
                incidence_rows.append(
                    f"<tr><td class='text-left'>{item}</td><td class='text-center'>{rate*100:.2f}%</td></tr>"
                )
            inc_html = ["<table class='result-table'>", "<tr><th class='text-left'>Encargo</th><th class='text-center'>%</th></tr>"]
            inc_html.extend(incidence_rows)
            inc_html.append("</table>")
            st.markdown("\n".join(inc_html), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
