import streamlit as st

from engines.countries import COUNTRIES
from engines.ui import init_page


COST_DATA = {
    "Brasil": {
        "total": 0.315,
        "items": [("FGTS", 0.08), ("INSS Patronal", 0.20), ("Sistema S", 0.025), ("RAT", 0.02)],
    },
    "Estados Unidos": {
        "total": 0.153,
        "items": [("FICA (Employer)", 0.062), ("Medicare (Employer)", 0.0145), ("FUTA/SUTA", 0.01)],
    },
    "Canadá": {
        "total": 0.1607,
        "items": [("CPP (Employer)", 0.0595), ("EI (Employer)", 0.0221)],
    },
    "México": {"total": 0.22, "items": [("IMSS + SAR + INFONAVIT", 0.22)]},
    "Chile": {"total": 0.14, "items": [("AFP + Seguro Cesantía", 0.14)]},
    "Colômbia": {"total": 0.30, "items": [("Seguridad Social Patronal", 0.30)]},
    "Argentina": {"total": 0.25, "items": [("Cargas Patronales", 0.25)]},
}


def build_table(selection):
    html = ["<table class='result-table'>"]
    html.append("<tr><th>País</th><th>Total de encargos (%)</th><th>Detalhamento</th></tr>")
    for country in selection:
        data = COST_DATA.get(country)
        if not data:
            continue
        items = "<br/>".join([f"{name} ... {rate*100:.2f}%" for name, rate in data["items"]])
        html.append(
            f"<tr><td>{country}</td><td style='text-align:center'>{data['total']*100:.2f}%</td><td>{items}</td></tr>"
        )
    html.append("</table>")
    return "\n".join(html)


def main():
    translations = init_page("page_06_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    selection = st.multiselect(
        translations.get("multi_country_label", "Países para comparação"),
        country_names,
        default=country_names[:3],
    )

    st.markdown(build_table(selection), unsafe_allow_html=True)

    if selection:
        sorted_selection = sorted(selection, key=lambda c: COST_DATA.get(c, {}).get("total", 0))
        ranking = "\n".join(
            [f"{i+1}º {name} — {COST_DATA[name]['total']*100:.2f}%" for i, name in enumerate(sorted_selection)]
        )
        st.markdown("#### Ranking")
        st.markdown(ranking)


if __name__ == "__main__":
    main()
