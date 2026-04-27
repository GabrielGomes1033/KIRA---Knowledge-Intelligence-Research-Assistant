import re
from collections import Counter

STOPWORDS = set('''a o as os um uma uns umas de da do das dos para por com sem em no na nos nas e ou que qual quais como onde quando porque por que sobre entre mais menos muito muita muitos muitas seu sua seus suas minha meu meus minhas isso isto esse essa esses essas aquele aquela voce você me te se ao à aos às é são foi ser estar existe existem'''.split())

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def keywords(text: str, limit: int = 8) -> list[str]:
    words = re.findall(r"[A-Za-zÀ-ÿ0-9\-\.]{3,}", text.lower())
    words = [w for w in words if w not in STOPWORDS]
    return [w for w, _ in Counter(words).most_common(limit)]


def score_result(query: str, title: str, body: str) -> int:
    ks = keywords(query, 12)
    content = f"{title} {body}".lower()
    score = 0
    for k in ks:
        if k in content:
            score += 3 if k in title.lower() else 1
    return score
