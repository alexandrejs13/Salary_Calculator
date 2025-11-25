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
        f"<h1>{translations.get('page_03_title', 'Custo do Empregador')}</h1>"
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
        key="page3_country_select",
    )
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    st.session_state["page3_country_code"] = country_cfg.code

    col1, col2, col3 = st.columns(3)
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
    in_kind_benefits = col3.number_input(
        translations.get("in_kind_benefits_label", "Benefícios em espécie"),
        min_value=0.0,
        step=50.0,
        key="page3_in_kind",
        help=translations.get(
            "help_in_kind_benefits",
            "Adicione benefícios em espécie que não incidem no salário (vale refeição, alimentação, etc.).",
        ),
    )

    col4, col5, col6 = st.columns(3)
    bonus_percent = col3.number_input(
        t(translations, "bonus_percent_label"),
        min_value=0.0,
        step=1.0,
        key="page3_bonus",
    )
    bonus_incidence = col4.selectbox(
        translations.get("bonus_incidence_label", "Incidências do Bônus"),
        country_cfg.bonus_incidence,
        key="page3_bonus_incidence",
    )
    pension_employer = col5.number_input(
        t(translations, "private_pension_employer_label"),
        min_value=0.0,
        step=50.0,
        key="page3_pension_employer",
    )
    col6.text_input(
        t(translations, "frequency_label"),
        value=str(country_cfg.annual_frequency),
        disabled=True,
    )

    if st.button(translations.get("calculate_button", "Calcular")):
        freq = country_cfg.annual_frequency
        monthly_base = base_salary + additions
        currency = CURRENCY_SYMBOL.get(country_cfg.code, "R$")
        bonus_value = (bonus_percent / 100) * monthly_base * freq
        inc_lower = (bonus_incidence or "").lower()
        include_bonus_in_charges = not ("não" in inc_lower or "exent" in inc_lower)
        thirteenth = monthly_base if freq > 12 else 0.0
        vacation = monthly_base if country_cfg.code in ["br", "cl", "ar", "co", "mx"] else 0.0
        vacation_third = monthly_base / 3 if country_cfg.code == "br" else 0.0
        annual_salary = monthly_base * 12
        base_components = [
            ("Salário base + adicionais (12x)", annual_salary, None),
            ("13º salário" if thirteenth else None, thirteenth, None),
            ("Férias", vacation, None) if vacation else (None, 0, None),
            ("1/3 férias", vacation_third, None) if vacation_third else (None, 0, None),
            ("Bônus", bonus_value, None) if bonus_value else (None, 0, None),
            ("Benefícios em espécie", in_kind_benefits * freq, None) if in_kind_benefits else (None, 0, None),
            ("Previdência privada (empregador)", pension_employer * freq, None) if pension_employer else (None, 0, None),
        ]
        charge_base = annual_salary + thirteenth + vacation + vacation_third
        if include_bonus_in_charges:
            charge_base += bonus_value
        employer_rows = []
        for item, rate in EMPLOYER_ITEMS.get(country_cfg.code, []):
            annual_value = charge_base * rate
            employer_rows.append((item, rate * 100, annual_value))

        all_rows = []
        for label, val, rate in base_components:
            if label and val:
                all_rows.append((label, rate, val))
        all_rows.extend(employer_rows)
        total_cost = sum(val for _, _, val in all_rows)
        st.markdown("### " + translations.get("section_employer_cost", "Custo do empregador"))
        table_html = ["<table class='result-table'>"]
        table_html.append(
            "<tr>"
            "<th class='text-left'>Item</th>"
            "<th class='text-center'>% empregador</th>"
            "<th class='text-right'>Valor mensal (12)</th>"
            "<th class='text-right'>Valor anual</th>"
            "</tr>"
        )
        for label, rate, annual_value in all_rows:
            monthly_value = annual_value / 12
            rate_txt = f"{rate:.2f}%" if rate else "—"
            table_html.append(
                f"<tr>"
                f"<td class='text-left'>{label}</td>"
                f"<td class='text-center'>{rate_txt}</td>"
                f"<td class='text-right'>{currency} {monthly_value:,.2f}</td>"
                f"<td class='text-right'>{currency} {annual_value:,.2f}</td>"
                f"</tr>"
            )
        table_html.append(
            f"<tr class='final-row'>"
            f"<td class='text-left'>Total</td><td></td>"
            f"<td class='text-right'>{currency} {(total_cost/12):,.2f}</td>"
        f"<td class='text-right'>{currency} {total_cost:,.2f}</td>"
        f"</tr>"
        )
        table_html.append("</table>")
        st.markdown("\n".join(table_html), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
