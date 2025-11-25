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
    label_to_code = {cfg.label: cfg.code for cfg in COUNTRIES.values()}
    labels = list(label_to_code.keys())
    current_code = st.session_state.get(session_code_key, country_code)
    default_idx = labels.index(COUNTRIES.get(current_code, DEFAULT_COUNTRY).label) if current_code in [c.code for c in COUNTRIES.values()] else 0

    def _update_country():
        selected = st.session_state.get(f"{session_code_key}_select")
        if selected:
            st.session_state[session_code_key] = label_to_code.get(selected, current_code)

    def _fmt_br(num: float) -> str:
        return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def formatted_money_input(label: str, key: str, value: float = 0.0, step: float = 50.0, disabled: bool = False, help: str = None):
        float_key = key
        text_key = f"{key}_text"
        stored = st.session_state.get(float_key, value)
        default_text = _fmt_br(float(stored))
        text_val = st.text_input(
            label,
            value=st.session_state.get(text_key, default_text),
            key=text_key,
            disabled=disabled,
            help=help,
        )
        try:
            clean = text_val.replace(".", "").replace(",", ".")
            parsed = float(clean) if clean else 0.0
        except ValueError:
            parsed = stored if stored is not None else 0.0
        st.session_state[float_key] = parsed
        st.session_state[text_key] = _fmt_br(parsed)
        return parsed

    # Primeira linha: país + campos variáveis por país (país na primeira coluna)
    if current_code == "ca":
        country_col, province_col, contract_col, adj_col = st.columns([1, 1, 1, 1])
    elif current_code in ("co", "mx", "us"):
        country_col, second_col, contract_col = st.columns([1, 1, 1])
    else:
        country_col, contract_col = st.columns([1, 1])

    selected_label = country_col.selectbox(
        t(translations, "country_label"),
        labels,
        index=default_idx,
        key=f"{session_code_key}_select",
        on_change=_update_country,
    )
    current_code = label_to_code.get(selected_label, current_code)
    st.session_state[session_code_key] = current_code
    cfg: CountryConfig = COUNTRIES.get(current_code, DEFAULT_COUNTRY)
    form_key = f"{prefix}_{current_code}"
    k = lambda name: f"{form_key}_{name}"
    values: Dict = {"country_code": current_code, "country_label": selected_label}

    if current_code == "ca":
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
    elif current_code == "co":
        values["city"] = second_col.text_input(t(translations, "city_label"), key=k("city"))
        values["contract_type"] = contract_col.selectbox(
            t(translations, "contract_label"),
            cfg.contracts,
            key=k("contract"),
        )
    elif current_code == "mx":
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
    elif current_code == "us":
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

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    values["base_salary"] = formatted_money_input(
        t(translations, "base_salary_label"),
        key=k("base_salary"),
        value=0.0,
        step=100.0,
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
    values["other_additions"] = formatted_money_input(
        t(translations, "other_additions_label"),
        key=k("additions"),
        value=0.0,
        step=50.0,
        help=t(translations, "help_other_additions"),
    )
    values["in_kind_benefits"] = formatted_money_input(
        translations.get("in_kind_benefits_label", "Benefícios em espécie"),
        key=k("in_kind"),
        value=0.0,
        step=50.0,
        help=translations.get(
            "help_in_kind_benefits",
            "Adicione benefícios em espécie que não incidem no salário (vale refeição, alimentação, etc.).",
        ),
    )

    if current_code in ("cl", "us"):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    elif current_code == "ca":
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    else:
        col1, col2, col3 = st.columns([1, 1, 1])

    values["other_discounts"] = formatted_money_input(
        t(translations, "other_discounts_label"),
        key=k("other_discounts"),
        value=0.0,
        step=50.0,
        help=t(translations, "help_other_discounts"),
    )
    values["alimony"] = formatted_money_input(
        t(translations, "alimony_label"),
        key=k("alimony"),
        value=0.0,
        step=50.0,
    )
    values["dependents"] = col3.number_input(
        t(translations, "dependents_label"),
        min_value=0,
        step=1,
        key=k("dependents"),
    )
    if current_code == "cl":
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
    if current_code == "us":
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
    if current_code == "ca":
        values["additional_withholding"] = col4.number_input(
            t(translations, "additional_withholding"),
            min_value=0.0,
            step=50.0,
            key=k("withholding_ca"),
        )

    col1, col2, col3 = st.columns(3)
    pension_options = cfg.extras.get("previdencia", ["PGBL", "VGBL", "FGBL"])
    values["pension_type"] = col1.selectbox(
        t(translations, "private_pension_type_label"),
        pension_options,
        key=k("pension_type"),
    )
    values["pension_employer"] = formatted_money_input(
        t(translations, "private_pension_employer_label"),
        key=k("pension_employer"),
        value=0.0,
        step=50.0,
    )
    values["pension_employee"] = formatted_money_input(
        t(translations, "private_pension_employee_label"),
        key=k("pension_employee"),
        value=0.0,
        step=50.0,
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
