import arxiv
import requests
from kira.config import RESULTS_LIMIT, TIMEOUT
from kira.core.text import score_result


def search_arxiv(query: str, max_results: int = RESULTS_LIMIT) -> list[dict]:
    output = []
    try:
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
        for paper in client.results(search):
            output.append({
                "title": paper.title,
                "summary": paper.summary.replace("\n", " "),
                "url": paper.entry_id,
                "published": str(paper.published.date()),
                "source": "arXiv",
                "score": score_result(query, paper.title, paper.summary)
            })
    except Exception as exc:
        output.append({"title": "Erro no arXiv", "summary": str(exc), "url": "", "source": "erro", "score": 0})
    return output


def search_crossref(query: str, max_results: int = RESULTS_LIMIT) -> list[dict]:
    url = "https://api.crossref.org/works"
    params = {"query": query, "rows": max_results, "sort": "relevance"}
    output = []
    try:
        r = requests.get(url, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        for item in r.json().get("message", {}).get("items", []):
            title = " ".join(item.get("title", ["Sem título"]))
            abstract = item.get("abstract", "").replace("<jats:p>", "").replace("</jats:p>", "")
            doi = item.get("DOI", "")
            link = f"https://doi.org/{doi}" if doi else item.get("URL", "")
            output.append({
                "title": title,
                "summary": abstract[:900] if abstract else "Artigo encontrado, mas sem resumo disponível na API.",
                "url": link,
                "source": "Crossref",
                "score": score_result(query, title, abstract)
            })
    except Exception as exc:
        output.append({"title": "Erro no Crossref", "summary": str(exc), "url": "", "source": "erro", "score": 0})
    return output
