from rich.console import Console
from rich.markdown import Markdown

from kira.services.web_search import search_web
from kira.services.science import search_arxiv, search_crossref
from kira.services.finance import get_asset_summary, get_brl_rates
from kira.services.calculator import calculate
from kira.services.translator import translate
from kira.services.news import feed_news
from kira.core.summarizer import build_research_answer

console = Console()

HELP = """
# KIRA — comandos

- `/pesquisar pergunta` — pesquisa ampla na internet e resume.
- `/cientifico tema` — busca arXiv + Crossref + web.
- `/tecnologia tema` — busca tecnologia + notícias.
- `/financeiro ativo` — análise rápida de ativo. Ex: PETR4.SA, BTC-USD, AAPL.
- `/cotacao` — dólar, euro e bitcoin em BRL via AwesomeAPI.
- `/calcular expressão` — cálculo simbólico com SymPy.
- `/traduzir idioma texto` — traduz automaticamente. Ex: /traduzir en buracos negros.
- `/ajuda` — mostra ajuda.
- `/sair` — fecha.
"""


class KiraApp:
    def processar(self, pergunta: str) -> str:
        pergunta = pergunta.strip()

        if not pergunta:
            return "Digite uma pergunta para a KIRA pesquisar."

        if pergunta.startswith("/calcular"):
            expr = pergunta.replace("/calcular", "", 1).strip()
            return f"Resultado: {calculate(expr)}"

        if pergunta.startswith("/traduzir"):
            parts = pergunta.split(maxsplit=2)
            if len(parts) < 3:
                return "Uso: /traduzir en texto"
            return translate(parts[2], parts[1])

        if pergunta.startswith("/financeiro"):
            symbol = pergunta.replace("/financeiro", "", 1).strip()
            data = get_asset_summary(symbol)

            if "error" in data:
                return data["error"]

            return f"""
# Análise financeira rápida — {data['symbol']}

Nome: {data['name']}
Preço atual: {data['price']} {data['currency']}
Variação em 1 mês: {data['month_change_percent']}%
Setor: {data['sector']}
Valor de mercado: {data['market_cap']}

Resumo:
{data['summary']}

Observação: isso é informação educacional, não recomendação de investimento.
"""

        if pergunta.startswith("/cotacao"):
            return str(get_brl_rates())

        if pergunta.startswith("/cientifico"):
            q = pergunta.replace("/cientifico", "", 1).strip()
            results = search_arxiv(q) + search_crossref(q) + search_web(q)
            results = sorted(results, key=lambda r: r.get("score", 0), reverse=True)
            return build_research_answer(q, results)

        if pergunta.startswith("/tecnologia"):
            q = pergunta.replace("/tecnologia", "", 1).strip()
            results = search_web(q + " tecnologia desenvolvimento software IA") + feed_news("tecnologia")
            return build_research_answer(q, results)

        if pergunta.startswith("/pesquisar"):
            q = pergunta.replace("/pesquisar", "", 1).strip()
            return build_research_answer(q, search_web(q))

        results = search_web(pergunta)
        return build_research_answer(pergunta, results)

    def run(self):
        console.print(
            "[bold cyan]KIRA v3 — Mini ChatGPT de Pesquisa Científica, Tecnologia e Mercado Financeiro[/bold cyan]"
        )
        console.print("Digite /ajuda para ver comandos.\n")

        while True:
            try:
                text = input("KIRA> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nEncerrando KIRA.")
                break

            if not text:
                continue

            if text in ["/sair", "sair", "exit"]:
                break

            self.handle(text)

    def handle(self, text: str):
        resposta = self.processar(text)

        if text.startswith("/ajuda"):
            console.print(Markdown(HELP))
            return

        console.print(Markdown(str(resposta)))