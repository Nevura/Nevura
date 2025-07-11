import json
import os
from typing import Dict

I18N_DIR = os.path.join(os.path.dirname(__file__), "../../i18n")

_cache = {}

def load_language(lang_code: str) -> Dict[str, str]:
    if lang_code in _cache:
        return _cache[lang_code]
    path = os.path.join(I18N_DIR, f"{lang_code}.json")
    if not os.path.isfile(path):
        path = os.path.join(I18N_DIR, "en.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        _cache[lang_code] = data
        return data

def translate(lang_code: str, key: str) -> str:
    translations = load_language(lang_code)
    return translations.get(key, key)
