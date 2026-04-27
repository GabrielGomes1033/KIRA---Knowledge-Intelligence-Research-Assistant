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
    def run(self):
        console.print("[bold cyan]KIRA v3 — Mini ChatGPT de Pesquisa Científica, Tecnologia e Mercado Financeiro[/bold cyan]")
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
        if text.startswith("/ajuda"):
            console.print(Markdown(HELP))
            return
        if text.startswith("/calcular"):
            expr = text.replace("/calcular", "", 1).strip()
            console.print(f"[bold]Resultado:[/bold] {calculate(expr)}")
            return
        if text.startswith("/traduzir"):
            parts = text.split(maxsplit=2)
            if len(parts) < 3:
                console.print("Uso: /traduzir en texto")
                return
            console.print(translate(parts[2], parts[1]))
            return
        if text.startswith("/financeiro"):
            symbol = text.replace("/financeiro", "", 1).strip()
            data = get_asset_summary(symbol)
            if "error" in data:
                console.print(f"[red]{data['error']}[/red]")
                return
            md = f"""
# Análise financeira rápida — {data['symbol']}

**Nome:** {data['name']}  
**Preço atual:** {data['price']} {data['currency']}  
**Variação em 1 mês:** {data['month_change_percent']}%  
**Setor:** {data['sector']}  
**Valor de mercado:** {data['market_cap']}  

## Resumo
{data['summary']}

> Observação: isso é informação educacional, não recomendação de investimento.
"""
            console.print(Markdown(md))
            return
        if text.startswith("/cotacao"):
            console.print(get_brl_rates())
            return
        if text.startswith("/cientifico"):
            q = text.replace("/cientifico", "", 1).strip()
            results = search_arxiv(q) + search_crossref(q) + search_web(q)
            console.print(Markdown(build_research_answer(q, sorted(results, key=lambda r: r.get('score', 0), reverse=True))))
            return
        if text.startswith("/tecnologia"):
            q = text.replace("/tecnologia", "", 1).strip()
            results = search_web(q + " tecnologia desenvolvimento software IA") + feed_news("tecnologia")
            console.print(Markdown(build_research_answer(q, results)))
            return
        if text.startswith("/pesquisar"):
            q = text.replace("/pesquisar", "", 1).strip()
            console.print(Markdown(build_research_answer(q, search_web(q))))
            return

        # Modo natural: qualquer frase vira pesquisa refinada.
        results = search_web(text)
        console.print(Markdown(build_research_answer(text, results)))
