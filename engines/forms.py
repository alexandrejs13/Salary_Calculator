from typing import Dict

import streamlit as st

from .countries import COUNTRIES, CountryConfig, DEFAULT_COUNTRY
from .i18n import t


def _section_title(text: str) -> str:
    if not text:
        return ""
    lowered = text.lower()
    return lowered[0].upper() + lowered[1:]


def render_country_form(
    country_code: str,
    translations: Dict[str, str],
    prefix: str = "",
    allow_country_select: bool = False,
) -> Dict:
    """Render dynamic form for a country and return captured inputs."""
    session_code_key = f"{prefix}_country_code" if prefix else "page1_country_code"
    code = st.session_state.get(session_code_key, country_code)
    label_to_code = {cfg.label: cfg.code for cfg in COUNTRIES.values()}
    labels = list(label_to_code.keys())
    default_idx = labels.index(COUNTRIES.get(code, DEFAULT_COUNTRY).label) if code in [c.code for c in COUNTRIES.values()] else 0

    # Seção de localização
    st.markdown(
        f"<div style='margin-top:6px;margin-bottom:2px;font-weight:700'>{_section_title(t(translations, 'section_location_contract'))}</div>",
        unsafe_allow_html=True,
    )

    # Layout por país (primeira linha)
    if code == "ca":
        cols = st.columns([1, 1, 1, 1])
    elif code in ("co", "mx", "us"):
        cols = st.columns([1, 1, 1])
    else:
        cols = st.columns([1, 1])

    selected_label = cols[0].selectbox(
        t(translations, "country_label"),
        labels,
        index=default_idx,
        key=f"{session_code_key}_select",
    )
    code = label_to_code.get(selected_label, code)
    st.session_state[session_code_key] = code
    cfg: CountryConfig = COUNTRIES.get(code, DEFAULT_COUNTRY)
    form_key = f"{prefix}_{code}"
    k = lambda name: f"{form_key}_{name}"
    values: Dict = {"country_code": code, "country_label": selected_label}

    if code == "ca":
        country_col, province_col, contract_col, adj_col = cols
        values["province"] = province_col.selectbox(
            t(translations, "province_label"),
            cfg.extras.get("provinces", []),
            key=k("province"),
        )
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )
        values["other_adjustments"] = adj_col.number_input(
            t(translations, "provincial_adjustments_label"),
            min_value=0.0,
            step=50.0,
            key=k("prov_adj"),
        )
    elif code == "co":
        country_col, second_col, contract_col = cols
        values["city"] = second_col.text_input(t(translations, "city_label"), key=k("city"))
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )
    elif code == "mx":
        country_col, second_col, contract_col = cols
        values["state"] = second_col.selectbox(
            t(translations, "state_label"),
            cfg.extras.get("estados", []),
            key=k("state"),
        )
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )
    elif code == "us":
        country_col, second_col, contract_col = cols
        values["state"] = second_col.selectbox(
            t(translations, "state_label"),
            cfg.extras.get("states", []),
            key=k("state"),
        )
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )
    else:
        country_col, contract_col = cols
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )

    elif code == "co":
        values["city"] = second_col.text_input(t(translations, "city_label"), key=k("city"))
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )
    elif code == "mx":
        values["state"] = second_col.selectbox(
            t(translations, "state_label"),
            cfg.extras.get("estados", []),
            key=k("state"),
        )
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )
    elif code == "us":
        values["state"] = second_col.selectbox(
            t(translations, "state_label"),
            cfg.extras.get("states", []),
            key=k("state"),
        )
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )
    else:
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )

    # Base de cálculo
    st.markdown(
        f"<div style='margin-top:10px;margin-bottom:2px;font-weight:700'>{_section_title(t(translations, 'section_base_calc'))}</div>",
        unsafe_allow_html=True,
    )
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    values["base_salary"] = col1.number_input(
        t(translations, "base_salary_label"),
        min_value=0.0,
        step=100.0,
        key=k("base_salary"),
    )
    col2.text_input(
        t(translations, "frequency_label"),
        value=f"{cfg.annual_frequency}",
        disabled=True,
        key=k("frequency"),
    )
    computed_annual = values["base_salary"] * cfg.annual_frequency
    col3.text_input(
        "Salário Anual",
        value=f"{computed_annual:,.2f}",
        disabled=True,
        key=k("annual_salary"),
    )
    values["other_additions"] = col4.number_input(
        t(translations, "other_additions_label"),
        min_value=0.0,
        step=50.0,
        key=k("additions"),
        help=t(translations, "help_other_additions"),
    )

    # Descontos
    st.markdown(
        f"<div style='margin-top:10px;margin-bottom:2px;font-weight:700'>{_section_title(t(translations, 'section_discounts'))}</div>",
        unsafe_allow_html=True,
    )
    if code in ("cl", "us"):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    elif code == "ca":
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    else:
        col1, col2, col3 = st.columns([1, 1, 1])

    values["other_discounts"] = col1.number_input(
        t(translations, "other_discounts_label"),
        min_value=0.0,
        step=50.0,
        key=k("other_discounts"),
        help=t(translations, "help_other_discounts"),
    )
    values["alimony"] = col2.number_input(
        t(translations, "alimony_label"),
        min_value=0.0,
        step=50.0,
        key=k("alimony"),
    )
    values["dependents"] = col3.number_input(
        t(translations, "dependents_label"),
        min_value=0,
        step=1,
        key=k("dependents"),
    )
    if code == "cl":
        values["health_option"] = col4.selectbox(
            t(translations, "health_label"),
            cfg.extras.get("salud", ["FONASA (7%)", "ISAPRE"]),
            key=k("health_cl"),
        )
        values["afp_rate"] = col5.number_input(
            t(translations, "afp_label"),
            min_value=0.0,
            max_value=0.2,
            step=0.01,
            value=0.1,
            key=k("afp"),
        )
    if code == "us":
        values["filing_status"] = col4.selectbox(
            t(translations, "filing_status_label"),
            cfg.extras.get("filing_status", []),
            key=k("filing_status"),
        )
        values["additional_withholding"] = col5.number_input(
            t(translations, "additional_withholding"),
            min_value=0.0,
            step=50.0,
            key=k("withholding"),
        )
    if code == "ca":
        values["additional_withholding"] = col4.number_input(
            t(translations, "additional_withholding"),
            min_value=0.0,
            step=50.0,
            key=k("withholding_ca"),
        )

    # Previdência privada
    st.markdown(
        f"<div style='margin-top:10px;margin-bottom:2px;font-weight:700'>{_section_title(t(translations, 'section_private_pension'))}</div>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    pension_options = cfg.extras.get("previdencia", ["PGBL", "VGBL", "FGBL"])
    values["pension_type"] = col1.selectbox(
        t(translations, "private_pension_type_label"),
        pension_options,
        key=k("pension_type"),
    )
    values["pension_employer"] = col2.number_input(
        t(translations, "private_pension_employer_label"),
        min_value=0.0,
        step=50.0,
        key=k("pension_employer"),
    )
    values["pension_employee"] = col3.number_input(
        t(translations, "private_pension_employee_label"),
        min_value=0.0,
        step=50.0,
        key=k("pension_employee"),
    )

    # Bônus
    st.markdown(
        f"<div style='margin-top:10px;margin-bottom:2px;font-weight:700'>{_section_title(t(translations, 'section_bonus'))}</div>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    values["bonus_percent"] = col1.number_input(
        t(translations, "bonus_percent_label"),
        min_value=0.0,
        max_value=200.0,
        step=1.0,
        key=k("bonus_percent"),
    )
    computed_bonus = values["bonus_percent"] * values["base_salary"] * cfg.annual_frequency / 100
    col2.text_input(
        t(translations, "bonus_value_label"),
        value=f"{computed_bonus:,.2f}",
        disabled=True,
        key=k("bonus_value"),
    )
    values["bonus_incidence"] = col3.selectbox(
        t(translations, "bonus_incidence_label"),
        cfg.bonus_incidence,
        key=k("bonus_incidence"),
    )

    return values
