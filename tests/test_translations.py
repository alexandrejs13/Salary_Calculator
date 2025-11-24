from pathlib import Path
import json


def test_translation_keys_match():
    base_dir = Path(__file__).resolve().parents[1] / "data" / "i18n"
    files = list(base_dir.glob("*.json"))
    assert files, "Nenhum arquivo de tradução encontrado"

    key_sets = []
    for path in files:
        with path.open(encoding="utf-8") as f:
            key_sets.append(set(json.load(f).keys()))

    reference = key_sets[0]
    for idx, keys in enumerate(key_sets[1:], start=1):
        missing = reference - keys
        extras = keys - reference
        assert not missing, f"Faltando chaves em {files[idx].name}: {missing}"
        assert not extras, f"Chaves extras em {files[idx].name}: {extras}"
