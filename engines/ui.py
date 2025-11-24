from pathlib import Path
from typing import Dict, Optional

import streamlit as st

from .countries import COUNTRIES, CountryConfig, DEFAULT_COUNTRY
from .i18n import load_translations, t

CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "css" / "layout_global.css"


def init_page(page_title_key: str) -> Dict[str, str]:
    """Prepare Streamlit page with CSS, language selector, and navigation."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "pt"
    lang = st.session_state["lang"]
    translations = load_translations(lang)
    st.set_page_config(
        page_title=translations.get(page_title_key, "Simulador de Remuneração"),
        layout="wide",
    )
    _inject_css()
    _render_sidebar(translations, lang)
    return translations


def _inject_css() -> None:
    if CSS_PATH.exists():
        with CSS_PATH.open() as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _render_sidebar(translations: Dict[str, str], current_lang: str) -> None:
    languages = {"Português": "pt", "English": "en", "Español": "es"}
    display_langs = list(languages.keys())
    current_display = [k for k, v in languages.items() if v == current_lang]
    index = display_langs.index(current_display[0]) if current_display else 0
    choice = st.sidebar.selectbox(translations.get("language_label", "Idioma"), display_langs, index=index)
    st.session_state["lang"] = languages.get(choice, "pt")

    st.sidebar.markdown("## " + translations.get("app_title", "Simulador de Remuneração"))
    st.sidebar.page_link("app.py", label=translations.get("page_01_title", "Simulador"))
    st.sidebar.page_link("pages/02_Comparador_de_Remuneracao.py", label=translations.get("page_02_title", "Comparador"))
    st.sidebar.page_link("pages/03_Custo_do_Empregador.py", label=translations.get("page_03_title", "Custo do empregador"))
    st.sidebar.page_link("pages/04_Salario_Bruto_a_partir_do_Liquido.py", label=translations.get("page_04_title", "Bruto a partir do líquido"))
    st.sidebar.page_link("pages/05_Tabelas_de_Contribuicoes.py", label=translations.get("page_05_title", "Contribuições"))
    st.sidebar.page_link("pages/06_Comparativo_Custo_Entre_Paises.py", label=translations.get("page_06_title", "Custo entre países"))
    st.sidebar.page_link("pages/07_Explicador.py", label=translations.get("page_07_title", "Explicador"))
    st.sidebar.page_link("pages/08_Glossario_Global.py", label=translations.get("page_08_title", "Glossário"))
    st.sidebar.page_link("pages/09_Equivalencia_Internacional.py", label=translations.get("page_09_title", "Equivalência"))


def render_title_with_flag(translations: Dict[str, str], country_cfg: Optional[CountryConfig]) -> None:
    flag_img = ""
    if country_cfg and Path(country_cfg.flag).exists():
        flag_img = f"<img src='{country_cfg.flag}' class='title-flag' alt='flag'/>"
    st.markdown(
        "<div class='title-row'>"
        f"<h1>{translations.get('app_title', 'Simulador de Remuneração')} – {translations.get('banner_region', '')}</h1>"
        f"{flag_img}"
        "</div>",
        unsafe_allow_html=True,
    )
