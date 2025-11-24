from typing import Dict, Optional

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
    code = country_code
    label_to_code = {cfg.label: cfg.code for cfg in COUNTRIES.values()}
    labels = list(label_to_code.keys())
    default_idx = labels.index(COUNTRIES.get(code, DEFAULT_COUNTRY).label) if code in [c.code for c in COUNTRIES.values()] else 0
    selected_label = None

    values: Dict = {"country_code": code}

    st.markdown(f"**{_section_title(t(translations, 'section_location_contract'))}**")
    col1, col2 = st.columns(2)
    if allow_country_select:
        selected_label = col1.selectbox(
            t(translations, "country_label"),
            labels,
            index=default_idx,
            key=f"{prefix}_country_select_inside",
        )
        code = label_to_code[selected_label]
        values["country_code"] = code
        values["country_label"] = selected_label
        cfg: CountryConfig = COUNTRIES.get(code, DEFAULT_COUNTRY)
    else:
        values["country_label"] = col1.text_input(
            t(translations, "country_label"),
            value=cfg.label,
            disabled=True,
            key=f"{prefix}_country_label",
        )
        cfg: CountryConfig = COUNTRIES.get(code, DEFAULT_COUNTRY)
    values["contract_type"] = col2.selectbox(
        t(translations, "contract_label"),
        cfg.contracts,
        key=f"{prefix}_contract",
    )

    # Base de cálculo
    st.markdown(f"**{_section_title(t(translations, 'section_base_calc'))}**")
    col1, col2, col3 = st.columns(3)
    values["base_salary"] = col1.number_input(
        t(translations, "base_salary_label"),
        min_value=0.0,
        step=100.0,
        key=f"{prefix}_base_salary",
    )
    col2.text_input(
        t(translations, "frequency_label"),
        value=f"{cfg.annual_frequency}",
        disabled=True,
        key=f"{prefix}_frequency",
    )
    values["other_additions"] = col3.number_input(
        t(translations, "other_additions_label"),
        min_value=0.0,
        step=50.0,
        key=f"{prefix}_additions",
        help=t(translations, "help_other_additions"),
    )

    # Descontos
    st.markdown(f"**{_section_title(t(translations, 'section_discounts'))}**")
    col1, col2, col3 = st.columns(3)
    values["other_discounts"] = col1.number_input(
        t(translations, "other_discounts_label"),
        min_value=0.0,
        step=50.0,
        key=f"{prefix}_other_discounts",
        help=t(translations, "help_other_discounts"),
    )
    values["alimony"] = col2.number_input(
        t(translations, "alimony_label"),
        min_value=0.0,
        step=50.0,
        key=f"{prefix}_alimony",
    )
    values["dependents"] = col3.number_input(
        t(translations, "dependents_label"),
        min_value=0,
        step=1,
        key=f"{prefix}_dependents",
    )

    # Previdência privada
    st.markdown(f"**{_section_title(t(translations, 'section_private_pension'))}**")
    col1, col2, col3 = st.columns(3)
    pension_options = cfg.extras.get("previdencia", ["PGBL", "VGBL", "FGBL"])
    values["pension_type"] = col1.selectbox(
        t(translations, "private_pension_type_label"),
        pension_options,
        key=f"{prefix}_pension_type",
    )
    values["pension_employer"] = col2.number_input(
        t(translations, "private_pension_employer_label"),
        min_value=0.0,
        step=50.0,
        key=f"{prefix}_pension_employer",
    )
    values["pension_employee"] = col3.number_input(
        t(translations, "private_pension_employee_label"),
        min_value=0.0,
        step=50.0,
        key=f"{prefix}_pension_employee",
    )

    # Campos específicos por país
    _render_country_specific_fields(code, cfg, translations, values, prefix)

    # Bônus
    st.markdown(f"**{_section_title(t(translations, 'section_bonus'))}**")
    col1, col2, col3 = st.columns(3)
    values["bonus_percent"] = col1.number_input(
        t(translations, "bonus_percent_label"),
        min_value=0.0,
        max_value=200.0,
        step=1.0,
        key=f"{prefix}_bonus_percent",
    )
    computed_bonus = values["bonus_percent"] * values["base_salary"] * cfg.annual_frequency / 100
    col2.text_input(
        t(translations, "bonus_value_label"),
        value=f"{computed_bonus:,.2f}",
        disabled=True,
        key=f"{prefix}_bonus_value",
    )
    values["bonus_incidence"] = col3.selectbox(
        t(translations, "bonus_incidence_label"),
        cfg.bonus_incidence,
        key=f"{prefix}_bonus_incidence",
    )

    return values


def _render_country_specific_fields(
    country_code: str,
    cfg: CountryConfig,
    translations: Dict[str, str],
    values: Dict,
    prefix: str,
) -> None:
    """Small helper to inject country specific inputs."""
    if country_code == "cl":
        st.markdown(f"**{_section_title(t(translations, 'section_social_security'))}**")
        col1, col2, col3 = st.columns(3)
        values["health_option"] = col1.selectbox(
            t(translations, "health_label"),
            cfg.extras.get("salud", ["FONASA (7%)", "ISAPRE"]),
            key=f"{prefix}_health_cl",
        )
        values["afp_rate"] = col2.number_input(
            t(translations, "afp_label"),
            min_value=0.0,
            max_value=0.2,
            step=0.01,
            value=0.1,
            key=f"{prefix}_afp",
        )
        values["other_discounts"] = values.get("other_discounts", 0)
    elif country_code == "ar":
        st.markdown(f"**{_section_title(t(translations, 'section_social_security'))}**")
        col1, col2 = st.columns(2)
        values["jubilacion"] = col1.number_input(
            t(translations, "jubilacion_label"),
            min_value=0.0,
            max_value=0.2,
            step=0.01,
            value=0.11,
            key=f"{prefix}_jubilacion",
        )
        values["obra_social"] = col2.number_input(
            t(translations, "obra_social_label"),
            min_value=0.0,
            max_value=0.1,
            step=0.01,
            value=0.03,
            key=f"{prefix}_obra",
        )
    elif country_code == "co":
        st.markdown(f"**{_section_title(t(translations, 'section_social_security'))}**")
        col1, col2, col3 = st.columns(3)
        values["city"] = col1.text_input(t(translations, "city_label"), key=f"{prefix}_city")
        values["contract_type"] = col2.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=f"{prefix}_contract_co",
        )
        values["solidarity_fund"] = col3.number_input(
            t(translations, "solidarity_fund_label"),
            min_value=0.0,
            max_value=0.05,
            step=0.001,
            key=f"{prefix}_solidarity",
        )
    elif country_code == "mx":
        st.markdown(f"**{_section_title(t(translations, 'section_social_security'))}**")
        col1, col2, col3 = st.columns(3)
        values["state"] = col1.selectbox(
            t(translations, "state_label"),
            cfg.extras.get("estados", []),
            key=f"{prefix}_state_mx",
        )
        values["cuota_obrera"] = col2.number_input(
            t(translations, "cuota_obrera_label"),
            min_value=0.0,
            max_value=0.3,
            step=0.01,
            value=0.04,
            key=f"{prefix}_cuota",
        )
        values["riesgo_trabajo"] = col3.number_input(
            t(translations, "riesgo_trabajo_label"),
            min_value=0.0,
            max_value=0.1,
            step=0.005,
            value=0.01,
            key=f"{prefix}_riesgo",
        )
    elif country_code == "us":
        st.markdown(f"**{_section_title(t(translations, 'section_tax'))}**")
        col1, col2, col3 = st.columns(3)
        values["state"] = col1.selectbox(
            t(translations, "state_label"),
            cfg.extras.get("states", []),
            key=f"{prefix}_state_us",
        )
        values["filing_status"] = col2.selectbox(
            t(translations, "filing_status_label"),
            cfg.extras.get("filing_status", []),
            key=f"{prefix}_filing",
        )
        values["additional_withholding"] = col3.number_input(
            t(translations, "additional_withholding"),
            min_value=0.0,
            step=50.0,
            key=f"{prefix}_withholding",
        )
    elif country_code == "ca":
        st.markdown(f"**{_section_title(t(translations, 'section_tax'))}**")
        col1, col2, col3 = st.columns(3)
        values["province"] = col1.selectbox(
            t(translations, "province_label"),
            cfg.extras.get("provinces", []),
            key=f"{prefix}_province",
        )
        values["dependents"] = values.get("dependents", 0)
        values["additional_withholding"] = col2.number_input(
            t(translations, "additional_withholding"),
            min_value=0.0,
            step=50.0,
            key=f"{prefix}_withholding_ca",
        )
        values["other_adjustments"] = col3.number_input(
            t(translations, "provincial_adjustments_label"),
            min_value=0.0,
            step=50.0,
            key=f"{prefix}_prov_adj",
        )
