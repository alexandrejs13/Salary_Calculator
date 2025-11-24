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
