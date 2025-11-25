import streamlit as st

from engines.ui import init_page


GLOSSARIO = {
    "A": [
        ("Adicional", "Remuneração complementar ao salário base."),
        ("Alíquota", "Percentual aplicado sobre base de cálculo."),
    ],
    "B": [
        ("Base de contribuição", "Valor sobre o qual incidem encargos."),
        ("Benefícios", "Remunerações não salariais."),
    ],
}

EQUIVALENCIAS = [
    "INSS (Brasil) ≈ CPP (Canadá) ≈ FICA (EUA)",
    "FGTS (Brasil) ≈ SAR (México) ≈ Cesantía (Chile)",
]


def main():
    translations = init_page("page_08_title")
    st.markdown(
        "<div class='title-row'>"
        "<h1>Glossário Global</h1>"
        "<span></span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:6px; border-top: 3px solid #0F4F59;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("### " + translations.get("glossary_header", "Glossário"))
    st.markdown(translations.get("glossary_intro", "Definições padronizadas."))

    for letter, entries in GLOSSARIO.items():
        st.markdown(f"#### {letter}")
        for term, desc in entries:
            st.markdown(f"**{term}** — {desc}")

    st.markdown("#### Equivalências")
    for item in EQUIVALENCIAS:
        st.markdown(f"- {item}")


if __name__ == "__main__":
    main()
