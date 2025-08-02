from . import ru_text, en_text, kz_text

LANGUAGES = {
    "ru": {
        "TEXT": ru_text.TEXT,
        "BUTTONS_TEXT": ru_text.BUTTONS_TEXT,
        "GENDER_LABELS": ru_text.GENDER_LABELS,
        "GENDER_EMOJI": ru_text.GENDER_EMOJI,
        "GENDER_SEARCH_LABELS": ru_text.GENDER_SEARCH_LABELS,
    },
    "en": {
        "TEXT": en_text.TEXT,
        "BUTTONS_TEXT": en_text.BUTTONS_TEXT,
        "GENDER_LABELS": en_text.GENDER_LABELS,
        "GENDER_EMOJI": en_text.GENDER_EMOJI,
        "GENDER_SEARCH_LABELS": en_text.GENDER_SEARCH_LABELS,
    },
    "kz": {
        "TEXT": kz_text.TEXT,
        "BUTTONS_TEXT": kz_text.BUTTONS_TEXT,
        "GENDER_LABELS": kz_text.GENDER_LABELS,
        "GENDER_EMOJI": kz_text.GENDER_EMOJI,
        "GENDER_SEARCH_LABELS": kz_text.GENDER_SEARCH_LABELS,
    }
}

async def get_texts(lang_code: str) -> dict:
    """Возвращает набор словарей по коду языка."""
    return LANGUAGES.get(lang_code, LANGUAGES["ru"])
