from ddgs import DDGS
from kira.config import RESULTS_LIMIT
from kira.core.text import score_result


def search_web(query: str, max_results: int = RESULTS_LIMIT) -> list[dict]:
    results = []
    try:
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=max_results * 2):
                title = item.get("title", "")
                body = item.get("body", "")
                href = item.get("href", "")
                results.append({
                    "title": title,
                    "summary": body,
                    "url": href,
                    "score": score_result(query, title, body),
                    "source": "web"
                })
    except Exception as exc:
        results.append({"title": "Erro na busca web", "summary": str(exc), "url": "", "score": 0, "source": "erro"})
    return sorted(results, key=lambda x: x.get("score", 0), reverse=True)[:max_results]
