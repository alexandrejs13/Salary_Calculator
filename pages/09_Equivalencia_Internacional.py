import streamlit as st

from engines.countries import COUNTRIES
from engines.i18n import t
from engines.ui import init_page


PPP_INDEX = {
    "Brasil": 3.5,
    "Estados Unidos": 1.0,
    "Canadá": 1.1,
    "México": 2.2,
    "Chile": 1.8,
    "Argentina": 2.5,
    "Colômbia": 2.0,
}

COST_OF_LIVING = {
    "Brasil": 55,
    "Estados Unidos": 75,
    "Canadá": 70,
    "México": 45,
    "Chile": 50,
    "Argentina": 40,
    "Colômbia": 42,
}


def main():
    translations = init_page("page_09_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    origin = st.selectbox(t(translations, "origin_country"), country_names, index=0, key="page9_origin")
    destination = st.selectbox(t(translations, "destination_country"), country_names, index=1, key="page9_dest")
    salary = st.number_input(t(translations, "base_salary_label"), min_value=0.0, step=100.0)
    include_bonus = st.checkbox(t(translations, "include_bonus"), value=True)
    consider_cost = st.checkbox(t(translations, "consider_employer_cost"), value=False)

    bonus_percent = st.slider(t(translations, "bonus_percent_label"), 0.0, 100.0, 0.0) if include_bonus else 0.0

    if st.button(translations.get("calculate_button", "Calcular")) and origin and destination:
        base = salary * (1 + bonus_percent / 100)
        ppp_origin = PPP_INDEX.get(origin, 1.0)
        ppp_dest = PPP_INDEX.get(destination, 1.0)
        cost_origin = COST_OF_LIVING.get(origin, 60)
        cost_dest = COST_OF_LIVING.get(destination, 60)

        salary_adjusted = base * (ppp_origin / ppp_dest)
        salary_equivalent = salary_adjusted * (cost_dest / cost_origin)
        if consider_cost:
            salary_equivalent *= 1.05

        st.markdown(
            f"**{origin} → {destination}:** {salary_equivalent:,.2f} (ajustado por PPP e custo de vida)"
        )
        st.progress(min(max(salary_equivalent / (salary * 2 if salary else 1), 0), 1))


if __name__ == "__main__":
    main()
