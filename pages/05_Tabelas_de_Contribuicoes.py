import streamlit as st

from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.ui import init_page, render_title_with_flag


EMPLOYEE_TABLE = [
    ("INSS / Previdência", "Salário", "Teto progressivo", "7–14%", "Não", "Salário, 13º"),
    ("Imposto de Renda", "Base IR", "Tabela progressiva", "0–27.5%", "Não", "Salário, 13º"),
    ("Previdência complementar", "Salário ou teto", "Limite do plano", "Variável", "Pode", "Salário"),
    ("Pensão alimentícia", "Base IR", "—", "Variável", "Não", "Salário"),
]

EMPLOYER_TABLE = [
    ("INSS Patronal", "Salário", "20%", "—", "Salário"),
    ("FGTS", "Salário + 13º + férias", "8%", "—", "Salário, 13º, férias, bônus*"),
    ("Sistema S", "Salário", "2.5%", "—", "Salário"),
    ("RAT/SAT", "Salário", "1–3%", "—", "Salário"),
]

INCIDENCE_TABLE = [
    ("INSS empregado", "✔", "✔", "✖", "✖", "✖"),
    ("IRRF", "✔", "✔", "✖", "✖", "✖"),
    ("INSS patronal", "✔", "✔", "✖", "✖", "✖"),
    ("FGTS", "✔", "✔", "✔", "—", "✔*"),
    ("Sistema S", "✔", "✔", "✖", "✖", "✖"),
    ("RAT/SAT", "✔", "✔", "✖", "✖", "✖"),
]


def table_html(headers, rows):
    html = ["<table class='result-table'>"]
    html.append("<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>")
    for row in rows:
        html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    html.append("</table>")
    return "\n".join(html)


def main():
    translations = init_page("page_05_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    selected_country = st.selectbox("País", country_names, index=0, key="page5_country_select")
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    render_title_with_flag(translations, country_cfg)

    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    st.markdown("#### " + translations.get("section_contributions_employee", "Contribuições do empregado"))
    st.markdown(
        table_html(
            ["Descrição", "Base de cálculo", "Faixa/Teto", "%", "Valor fixo?", "Incide sobre?"],
            EMPLOYEE_TABLE,
        ),
        unsafe_allow_html=True,
    )

    st.markdown("#### " + translations.get("section_contributions_employer", "Contribuições do empregador"))
    st.markdown(
        table_html(
            ["Descrição", "Base de cálculo", "%", "Faixa/Teto", "Incide sobre?"],
            EMPLOYER_TABLE,
        ),
        unsafe_allow_html=True,
    )

    st.markdown("#### Tabela de incidências")
    st.markdown(
        table_html(
            ["Encargo", "Salário", "13º", "Férias", "FGTS", "Bônus"],
            INCIDENCE_TABLE,
        ),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
