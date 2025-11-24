from base64 import b64encode
from pathlib import Path
from typing import Dict, Optional

import streamlit as st

from .countries import CountryConfig
from .i18n import load_translations

CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "css" / "layout_global.css"


def init_page(page_title_key: str) -> Dict[str, str]:
    """Prepare Streamlit page with CSS and language selector (sem menu duplicado)."""
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


def _flag_data_uri(flag_path: Path) -> str:
    if not flag_path.exists():
        return ""
    data = flag_path.read_bytes()
    b64 = b64encode(data).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"


def render_title_with_flag(translations: Dict[str, str], country_cfg: Optional[CountryConfig]) -> None:
    flag_img = ""
    if country_cfg:
        data_uri = _flag_data_uri(Path(country_cfg.flag))
        if data_uri:
            flag_img = f"<img src='{data_uri}' class='title-flag' alt='flag'/>"
    st.markdown(
        "<div class='title-row'>"
        f"<h1>{translations.get('app_title', 'Simulador de Remuneração')} – {translations.get('banner_region', '')}</h1>"
        f"{flag_img}"
        "</div>",
        unsafe_allow_html=True,
    )
