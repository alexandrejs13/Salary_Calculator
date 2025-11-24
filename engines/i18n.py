import json
from functools import lru_cache
from pathlib import Path
from typing import Dict


BASE_DIR = Path(__file__).resolve().parent.parent
I18N_DIR = BASE_DIR / "data" / "i18n"
DEFAULT_LANG = "pt"
SUPPORTED_LANGS = ("pt", "en", "es")


@lru_cache(maxsize=None)
def load_translations(lang: str) -> Dict[str, str]:
    """Load translations for the given language, falling back to Portuguese."""
    lang_code = lang if lang in SUPPORTED_LANGS else DEFAULT_LANG
    path = I18N_DIR / f"{lang_code}.json"
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        fallback = I18N_DIR / f"{DEFAULT_LANG}.json"
        with fallback.open("r", encoding="utf-8") as f:
            return json.load(f)


def t(translations: Dict[str, str], key: str) -> str:
    """Return translated string for key or the key itself."""
    return translations.get(key, key)
