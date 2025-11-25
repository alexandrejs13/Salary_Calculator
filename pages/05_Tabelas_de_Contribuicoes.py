import streamlit as st

from engines.countries import COUNTRIES, DEFAULT_COUNTRY, find_country_by_label
from engines.ui import init_page


EMPLOYEE_TABLE = {
    "br": [
        ("INSS / Previdência", "Salário", "Teto progressivo", "7–14%", "Não", "Salário, 13º"),
        ("Imposto de Renda", "Base IR", "Tabela progressiva", "0–27.5%", "Não", "Salário, 13º"),
        ("Previdência complementar", "Salário ou teto", "Limite do plano", "Variável", "Pode", "Salário"),
        ("Pensão alimentícia", "Base IR", "—", "Variável", "Não", "Salário"),
    ],
    "default": [
        ("Imposto de Renda / Renda", "Base tributável", "Progressivo", "Variável", "Não", "Salário"),
        ("Segurança Social", "Salário", "Teto local", "Variável", "Não", "Salário"),
    ],
}

EMPLOYER_TABLE = {
    "br": [
        ("INSS Patronal", "Salário", "20%", "—", "Salário"),
        ("FGTS", "Salário + 13º + férias", "8%", "—", "Salário, 13º, férias, bônus*"),
        ("Sistema S", "Salário", "2.5%", "—", "Salário"),
        ("RAT/SAT", "Salário", "1–3%", "—", "Salário"),
    ],
    "default": [
        ("Segurança Social Patronal", "Salário", "Variável", "—", "Salário"),
        ("Impostos sobre folha", "Salário", "Variável", "—", "Salário"),
    ],
}

INCIDENCE_BY_COUNTRY = {
    "br": {
        "columns": ["Salário", "13º", "Férias", "FGTS", "Bônus"],
        "rows": [
            ("INSS empregado", [True, True, False, False, False]),
            ("IRRF", [True, True, False, False, False]),
            ("INSS patronal", [True, True, False, False, False]),
            ("FGTS", [True, True, True, True, True]),
            ("Sistema S", [True, True, False, False, False]),
            ("RAT/SAT", [True, True, False, False, False]),
        ],
    },
    "cl": {
        "columns": ["Salário", "Gratificação", "Bônus"],
        "rows": [
            ("AFP empregado", [True, True, False]),
            ("Saúde", [True, True, False]),
            ("Imposto Renda", [True, True, False]),
            ("Seguro cesantía", [True, True, False]),
        ],
    },
    "ar": {
        "columns": ["Salário", "13º", "Bônus"],
        "rows": [
            ("Jubilación", [True, True, False]),
            ("Obra Social", [True, True, False]),
            ("Imposto Ganancias", [True, True, False]),
        ],
    },
    "co": {
        "columns": ["Salário", "Prima", "Bônus"],
        "rows": [
            ("Pensión", [True, True, False]),
            ("Salud", [True, True, False]),
            ("Solidaridad", [True, True, False]),
            ("Imposto Renta", [True, True, False]),
        ],
    },
    "mx": {
        "columns": ["Salário", "Aguinaldo", "Bônus"],
        "rows": [
            ("IMSS empregado", [True, True, False]),
            ("ISR", [True, True, False]),
        ],
    },
    "us": {
        "columns": ["Salary", "Bonus"],
        "rows": [
            ("FICA empregado", [True, True]),
            ("Federal/State Tax", [True, True]),
            ("FICA empregador", [True, True]),
        ],
    },
    "ca": {
        "columns": ["Salary", "Bonus"],
        "rows": [
            ("CPP empregado", [True, True]),
            ("EI empregado", [True, True]),
            ("Imposto renda", [True, True]),
        ],
    },
}

VIGENCIA_LINKS = {
    "br": ("Vigente 2025 – INSS/IRRF", "https://www.gov.br/inss/pt-br"),
    "us": ("IRS 2025 supplemental tables", "https://www.irs.gov/"),
    "ca": ("CRA/CPP-EI 2025", "https://www.canada.ca/"),
    "mx": ("SAT/IMSS 2025", "https://www.gob.mx/imss"),
    "cl": ("SII/AFP 2025", "https://www.sii.cl/"),
    "co": ("DIAN/Seguridad Social 2025", "https://www.dian.gov.co/"),
    "ar": ("AFIP/SIPA 2025", "https://www.afip.gob.ar/"),
}


def table_html(headers, rows, aligns=None):
    aligns = aligns or []
    html = ["<table class='result-table'>"]
    header_cells = []
    for i, h in enumerate(headers):
        cls = f"text-{aligns[i]}" if i < len(aligns) else "text-left"
        header_cells.append(f"<th class='{cls}'>{h}</th>")
    html.append("<tr>" + "".join(header_cells) + "</tr>")
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            cls = f"text-{aligns[i]}" if i < len(aligns) else "text-left"
            cells.append(f"<td class='{cls}'>{cell}</td>")
        html.append("<tr>" + "".join(cells) + "</tr>")
    html.append("</table>")
    return "\n".join(html)


def main():
    translations = init_page("page_05_title")
    country_names = [cfg.label for cfg in COUNTRIES.values()]
    flag_map = {"br": "🇧🇷", "cl": "🇨🇱", "ar": "🇦🇷", "co": "🇨🇴", "mx": "🇲🇽", "us": "🇺🇸", "ca": "🇨🇦"}
    current_code = st.session_state.get("page5_country_code", "br")
    current_cfg = COUNTRIES.get(current_code, DEFAULT_COUNTRY)
    st.markdown(
        "<div class='title-row'>"
        f"<h1>Tabelas de Contribuições</h1>"
        f"<span class='title-flag'>{flag_map.get(current_cfg.code, '')}</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:6px; border-top: 3px solid #0F4F59;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    vigencia, link = VIGENCIA_LINKS.get(country_cfg.code, ("Vigência 2025 (referência genérica)", ""))
    st.markdown(f"**{vigencia}**" + (f" — Fonte oficial: [{link}]({link})" if link else ""))
    st.markdown("<div class='title-card'>Parâmetros de cálculo da remuneração</div>", unsafe_allow_html=True)

    selected_country = st.selectbox("País", country_names, index=0, key="page5_country_select")
    country_cfg = find_country_by_label(selected_country) or DEFAULT_COUNTRY
    st.session_state["page5_country_code"] = country_cfg.code

    st.markdown("#### " + translations.get("section_contributions_employee", "Contribuições do empregado"))
    st.markdown(
        table_html(
            ["Descrição", "Base de cálculo", "Faixa/Teto", "%", "Valor fixo?", "Incide sobre?"],
            EMPLOYEE_TABLE.get(country_cfg.code, EMPLOYEE_TABLE["default"]),
            aligns=["left", "left", "left", "center", "center", "left"],
        ),
        unsafe_allow_html=True,
    )

    st.markdown("#### " + translations.get("section_contributions_employer", "Contribuições do empregador"))
    st.markdown(
        table_html(
            ["Descrição", "Base de cálculo", "%", "Faixa/Teto", "Incide sobre?"],
            EMPLOYER_TABLE.get(country_cfg.code, EMPLOYER_TABLE["default"]),
            aligns=["left", "left", "center", "left", "left"],
        ),
        unsafe_allow_html=True,
    )

    st.markdown("#### Tabela de incidências")
    incidence_cfg = INCIDENCE_BY_COUNTRY.get(country_cfg.code, INCIDENCE_BY_COUNTRY["br"])
    inc_rows = []
    for label, flags in incidence_cfg["rows"]:
        inc_rows.append([label] + [("✔" if v else "✖") for v in flags])
    aligns = ["left"] + ["center"] * len(incidence_cfg["columns"])
    st.markdown(
        table_html(
            ["Encargo"] + incidence_cfg["columns"],
            inc_rows,
            aligns=aligns,
        ),
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
