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
    freq_display = col2.text_input(
        t(translations, "frequency_label"),
        value=str(country_cfg.annual_frequency),
        disabled=True,
    )
    additions = col3.number_input(
        t(translations, "other_additions_label"),
        min_value=0.0,
        step=50.0,
        key="page3_additions",
    )

    annual_salary_display = (base_salary or 0) * country_cfg.annual_frequency
    col1b, col2b, col3b = st.columns(3)
    col1b.text_input(
        translations.get("salary_annual", "Salário anual (base)"),
        value=f"{annual_salary_display:,.2f}",
        disabled=True,
        key="page3_salary_annual",
    )
    in_kind_benefits = col2b.number_input(
        translations.get("in_kind_benefits_label", "Benefícios em espécie"),
        min_value=0.0,
        step=50.0,
        key="page3_in_kind",
        help=translations.get(
            "help_in_kind_benefits",
            "Adicione benefícios em espécie que não incidem no salário (vale refeição, alimentação, etc.).",
        ),
    )
    pension_employer = col3b.number_input(
        translations.get("private_pension_employer_label", "Previdência Privada"),
        min_value=0.0,
        step=50.0,
        key="page3_pension_employer",
        help=translations.get("private_pension_info", "Plano de previdência privada custeado pelo empregador."),
    )

    col4, col5, col6 = st.columns(3)
    bonus_percent = col4.number_input(
        t(translations, "bonus_percent_label"),
        min_value=0.0,
        step=1.0,
        key="page3_bonus",
    )
    # Calculado após inputs
    bonus_incidence = col6.selectbox(
        translations.get("bonus_incidence_label", "Incidências do Bônus"),
        country_cfg.bonus_incidence,
        key="page3_bonus_incidence",
    )
    monthly_base_for_bonus = base_salary + additions
    bonus_value_preview = (bonus_percent / 100) * monthly_base_for_bonus * country_cfg.annual_frequency
    col5.text_input(
        translations.get("bonus_value_label", "Valor Calculado"),
        value=f"{bonus_value_preview:,.2f}",
        disabled=True,
        key="page3_bonus_value",
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
        remuneration_rows = [
            ("Salário base", base_salary * 12, None, "Remuneração") if base_salary else (None, 0, None, None),
            ("Outros adicionais", additions * 12, None, "Remuneração") if additions else (None, 0, None, None),
            ("Bônus", bonus_value, None, "Remuneração") if bonus_value else (None, 0, None, None),
        ]
        pct_13 = 100.0 / 12.0  # ~8.33%
        pct_vac = 100.0 / 12.0  # ~8.33%
        pct_third = (1.0 / 3.0) * pct_vac  # ~2.78%
        manual_charges = [
            ("13º salário" if thirteenth else None, thirteenth, pct_13, "Encargos") if thirteenth else (None, 0, None, None),
            ("Férias", vacation, pct_vac, "Encargos") if vacation else (None, 0, None, None),
            ("1/3 férias", vacation_third, pct_third, "Encargos") if vacation_third else (None, 0, None, None),
        ]
        benefits_rows = [
            ("Benefícios em espécie", in_kind_benefits * freq, None, "Benefícios") if in_kind_benefits else (None, 0, None, None),
            ("Previdência Privada", pension_employer * freq, None, "Benefícios") if pension_employer else (None, 0, None, None),
        ]
        charge_base = annual_salary + thirteenth + vacation + vacation_third
        if include_bonus_in_charges:
            charge_base += bonus_value
        employer_rows = []
        for item, rate in EMPLOYER_ITEMS.get(country_cfg.code, []):
            annual_value = charge_base * rate
            employer_rows.append((item, rate * 100, annual_value))

        all_rows = []
        for label, val, rate, type_label in remuneration_rows:
            if label and val:
                all_rows.append((label, rate, val, "rem", type_label or "Remuneração"))
        for label, val, rate, type_label in benefits_rows:
            if label and val:
                all_rows.append((label, rate, val, "benefit", type_label or "Benefícios"))
        for label, val, rate, type_label in manual_charges:
            if label and val:
                all_rows.append((label, rate, val, "charge", type_label or "Encargos"))
        for label, rate_pct, val in employer_rows:
            all_rows.append((label, rate_pct, val, "charge", "Encargos"))

        rem_total = sum(val for _, _, val, cat, type_lbl in all_rows if cat == "rem" or type_lbl == "Remuneração")
        ben_total = sum(val for _, _, val, cat, type_lbl in all_rows if cat == "benefit" or type_lbl == "Benefícios")
        charge_total = sum(val for _, _, val, cat, type_lbl in all_rows if cat == "charge" or type_lbl == "Encargos")
        charge_pct_sum = sum((rate or 0) for _, rate, _, cat, type_lbl in all_rows if cat == "charge" or type_lbl == "Encargos")
        total_cost = rem_total + ben_total + charge_total
        st.markdown("### " + translations.get("section_employer_cost", "Custo do empregador"))
        table_html = ["<table class='result-table'>"]
        table_html.append(
            "<tr>"
            "<th class='text-left' style='width:25%; white-space:nowrap'>Tipo</th>"
            "<th class='text-left' style='width:25%'>Descrição</th>"
            "<th class='text-center' style='width:16.6%; text-align:center'>% Encargos</th>"
            "<th class='text-right' style='width:16.6%; text-align:right'>Valor mensal</th>"
            "<th class='text-right' style='width:16.6%; text-align:right'>Valor anual</th>"
            "</tr>"
        )
        rem_rows = [r for r in all_rows if r[3] == "rem" or r[4] == "Remuneração"]
        ben_rows = [r for r in all_rows if r[3] == "benefit" or r[4] == "Benefícios"]
        charge_rows = [r for r in all_rows if r[3] == "charge" or r[4] == "Encargos"]

        def render_rows(rows, show_percent: bool = False):
            for label, rate, annual_value, _cat, type_label in rows:
                monthly_value = annual_value / 12
                rate_txt = f"{rate:.2f}%" if (show_percent and rate) else ("—" if show_percent else "")
                table_html.append(
                    f"<tr>"
                    f"<td class='text-left' style='width:25%; white-space:nowrap'>{type_label}</td>"
                    f"<td class='text-left' style='width:25%'>{label}</td>"
                    f"<td class='text-center' style='width:16.6%'>{rate_txt}</td>"
                    f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {monthly_value:,.2f}</td>"
                    f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {annual_value:,.2f}</td>"
                    f"</tr>"
                )

        render_rows(rem_rows, show_percent=False)
        render_rows(ben_rows, show_percent=False)
        render_rows(charge_rows, show_percent=True)

        # Subtotais em cinza claro
        def pct(total):
            return (total / total_cost * 100) if total_cost else 0
        table_html.append(
            f"<tr style='background:#f4f4f4'>"
            f"<td class='text-left' style='width:25%; white-space:nowrap'>Subtotal Remuneração ({pct(rem_total):.1f}%)</td>"
            f"<td style='width:25%'></td><td class='text-center' style='width:16.6%'></td>"
            f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {(rem_total/12):,.2f}</td>"
            f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {rem_total:,.2f}</td>"
            f"</tr>"
        )
        table_html.append(
            f"<tr style='background:#f4f4f4'>"
            f"<td class='text-left' style='width:25%; white-space:nowrap'>Subtotal Benefícios ({pct(ben_total):.1f}%)</td>"
            f"<td style='width:25%'></td><td class='text-center' style='width:16.6%'></td>"
            f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {(ben_total/12):,.2f}</td>"
            f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {ben_total:,.2f}</td>"
            f"</tr>"
        )
        table_html.append(
            f"<tr style='background:#f4f4f4'>"
            f"<td class='text-left' style='width:25%; white-space:nowrap'>Subtotal Encargos ({pct(charge_total):.1f}%)</td>"
            f"<td style='width:25%'></td>"
            f"<td class='text-center' style='width:16.6%'></td>"
            f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {(charge_total/12):,.2f}</td>"
            f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {charge_total:,.2f}</td>"
            f"</tr>"
        )
        table_html.append(
            f"<tr class='final-row'>"
            f"<td class='text-left' style='width:25%'>Total</td><td style='width:25%'></td><td class='text-center' style='width:16.6%; color:white; font-weight:bold'>{charge_pct_sum:.2f}%</td>"
            f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {(total_cost/12):,.2f}</td>"
            f"<td class='text-right' style='width:16.6%; text-align:right'>{currency} {total_cost:,.2f}</td>"
            f"</tr>"
        )
        table_html.append("</table>")
        st.markdown("\n".join(table_html), unsafe_allow_html=True)

        # Tabela de incidências
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown("### Incidências dos encargos sobre componentes")
        inc_headers = ["Encargo", "Salário", "13º", "Férias", "Bônus", "Benefícios esp.", "Prev. empregador"]
        inc_cols = ["salary", "thirteenth", "vacation", "bonus", "in_kind", "pension"]
        inc_matrix = []
        for item, rate in EMPLOYER_ITEMS.get(country_cfg.code, []):
            inc_matrix.append((item, True, bool(thirteenth), bool(vacation), include_bonus_in_charges, False, False))
        symbol = lambda v: "✔" if v else "✖"
        inc_html = ["<table class='result-table'>"]
        inc_html.append(
            "<tr>"
            + "".join(
                [
                    (f"<th class='text-center' style='text-align:center'>{h}</th>" if i else f"<th class='text-left'>{h}</th>")
                    for i, h in enumerate(inc_headers)
                ]
            )
            + "</tr>"
        )
        for row in inc_matrix:
            name, sal, thir, vac, bon, ink, pen = row
            inc_html.append(
                "<tr>"
                f"<td class='text-left'>{name}</td>"
                f"<td class='text-center'>{symbol(sal)}</td>"
                f"<td class='text-center'>{symbol(thir)}</td>"
                f"<td class='text-center'>{symbol(vac)}</td>"
                f"<td class='text-center'>{symbol(bon)}</td>"
                f"<td class='text-center'>{symbol(ink)}</td>"
                f"<td class='text-center'>{symbol(pen)}</td>"
                "</tr>"
            )
        inc_html.append("</table>")
        st.markdown("\n".join(inc_html), unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        with st.expander(translations.get("charges_explainer_title", "O que é cada encargo ?"), expanded=False):
            body = translations.get(
                "charges_explainer_body",
                """
1. **13º salário**
   Remuneração adicional equivalente a 1 salário por ano, paga em até duas parcelas.
   Custo para a empresa: provisão mensal de 1/12 do salário (= 8,33%).
   Incidências: INSS patronal, FGTS e RAT.

2. **Férias**
   Direito anual de 30 dias remunerados, acrescidos do 1/3 constitucional.
   Custo para a empresa: provisão mensal de 1/12 (= 8,33%).
   Incidências: INSS patronal, FGTS e RAT.

3. **1/3 de férias**
   Adicional obrigatório de 33,33% sobre o valor das férias.
   Custo: equivale a 2,78% ao mês na provisão.
   Incidências: sofre INSS e FGTS.
   Observação: convenções coletivas podem elevar para 40% ou 50%, aumentando o custo.

4. **FGTS**
   Depósito mensal de 8% do salário bruto.
   Base: salário + adicionais + 13º + férias. Não incide sobre benefícios ou indenizações.

5. **INSS Patronal**
   Contribuição da empresa à Previdência (alíquota padrão 20%).
   Pode variar por desoneração ou Simples.

6. **Sistema S / Terceiros**
   Contribuições para SESI, SENAI, SESC, SEBRAE, INCRA, Salário-Educação etc.
   Alíquota varia por setor; aqui usamos 2,5% como referência.

7. **RAT (Risco Ambiental do Trabalho)**
   Seguro acidente: 1%, 2% ou 3% conforme o risco, ajustado pelo FAP.
                """,
            )
            # Preserva quebras de linha da tradução substituindo sequências literais \n por quebras reais
            st.markdown(body.replace("\\n", "\n"), unsafe_allow_html=False)


if __name__ == "__main__":
    main()
