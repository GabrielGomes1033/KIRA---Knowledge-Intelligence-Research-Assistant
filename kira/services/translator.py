from deep_translator import GoogleTranslator


def translate(text: str, target: str = "pt") -> str:
    if not text.strip():
        return ""
    try:
        return GoogleTranslator(source="auto", target=target).translate(text)
    except Exception as exc:
        return f"[Tradução indisponível: {exc}]\n{text}"
