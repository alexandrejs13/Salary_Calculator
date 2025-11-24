from base64 import b64encode
from pathlib import Path
from typing import Dict, Optional

import streamlit as st

from .countries import CountryConfig
from .i18n import load_translations

CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "css" / "layout_global.css"
EMOJI_BY_PAGE = {
    "app.py": "🧮",
    "pages/02_Comparador_de_Remuneracao.py": "⚖️",
    "pages/03_Custo_do_Empregador.py": "💼",
    "pages/04_Salario_Bruto_a_partir_do_Liquido.py": "🔄",
    "pages/05_Tabelas_de_Contribuicoes.py": "📊",
    "pages/06_Comparativo_Custo_Entre_Paises.py": "🌎",
    "pages/07_Explicador.py": "💡",
    "pages/08_Glossario_Global.py": "📚",
    "pages/09_Equivalencia_Internacional.py": "🔀",
}
FLAG_EMOJI_BY_CODE = {
    "br": "🇧🇷",
    "cl": "🇨🇱",
    "ar": "🇦🇷",
    "co": "🇨🇴",
    "mx": "🇲🇽",
    "us": "🇺🇸",
    "ca": "🇨🇦",
}


def init_page(page_title_key: str) -> Dict[str, str]:
    """Prepare Streamlit page with CSS and custom sidebar."""
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

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Menu")
    st.sidebar.page_link("app.py", label=f"{EMOJI_BY_PAGE['app.py']} {translations.get('page_01_title', 'Simulador')}")
    st.sidebar.page_link("pages/02_Comparador_de_Remuneracao.py", label=f"{EMOJI_BY_PAGE['pages/02_Comparador_de_Remuneracao.py']} {translations.get('page_02_title', 'Comparador')}")
    st.sidebar.page_link("pages/03_Custo_do_Empregador.py", label=f"{EMOJI_BY_PAGE['pages/03_Custo_do_Empregador.py']} {translations.get('page_03_title', 'Custo do empregador')}")
    st.sidebar.page_link("pages/04_Salario_Bruto_a_partir_do_Liquido.py", label=f"{EMOJI_BY_PAGE['pages/04_Salario_Bruto_a_partir_do_Liquido.py']} {translations.get('page_04_title', 'Bruto a partir do líquido')}")
    st.sidebar.page_link("pages/05_Tabelas_de_Contribuicoes.py", label=f"{EMOJI_BY_PAGE['pages/05_Tabelas_de_Contribuicoes.py']} {translations.get('page_05_title', 'Contribuições')}")
    st.sidebar.page_link("pages/06_Comparativo_Custo_Entre_Paises.py", label=f"{EMOJI_BY_PAGE['pages/06_Comparativo_Custo_Entre_Paises.py']} {translations.get('page_06_title', 'Custo entre países')}")
    st.sidebar.page_link("pages/07_Explicador.py", label=f"{EMOJI_BY_PAGE['pages/07_Explicador.py']} {translations.get('page_07_title', 'Explicador')}")
    st.sidebar.page_link("pages/08_Glossario_Global.py", label=f"{EMOJI_BY_PAGE['pages/08_Glossario_Global.py']} {translations.get('page_08_title', 'Glossário')}")
    st.sidebar.page_link("pages/09_Equivalencia_Internacional.py", label=f"{EMOJI_BY_PAGE['pages/09_Equivalencia_Internacional.py']} {translations.get('page_09_title', 'Equivalência')}")


def render_title_with_flag(translations: Dict[str, str], country_cfg: Optional[CountryConfig]) -> None:
    flag = ""
    if country_cfg:
        flag = FLAG_EMOJI_BY_CODE.get(country_cfg.code, "")
    st.markdown(
        "<div class='title-row'>"
        f"<h1>{translations.get('app_title', 'Simulador de Remuneração')} – {translations.get('banner_region', '')}</h1>"
        f"<span style='font-size:28px'>{flag}</span>"
        "</div>",
        unsafe_allow_html=True,
    )
