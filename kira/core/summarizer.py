from kira.core.text import clean_text, keywords
from kira.services.translator import translate


def build_research_answer(question: str, results: list[dict], target_lang: str = "pt") -> str:
    clean_results = [r for r in results if r.get("title") and r.get("source") != "erro"]
    top = clean_results[:6]
    ks = ", ".join(keywords(question, 8))

    if not top:
        return "Não encontrei resultados confiáveis para essa pergunta. Tente reformular com mais contexto."

    combined = " ".join([clean_text(r.get("summary", "")) for r in top])[:3500]
    translated = translate(combined, target_lang) if target_lang != "auto" else combined

    lines = []
    lines.append("## Resposta objetiva")
    lines.append(f"A pergunta central é: **{question}**. Pelas fontes encontradas, o tema envolve principalmente: **{ks}**.")
    lines.append("")
    lines.append("## Alto resumo detalhado")
    lines.append(translated)
    lines.append("")
    lines.append("## Pontos principais")
    for i, r in enumerate(top[:5], 1):
        summary = translate(r.get("summary", "")[:350], target_lang)
        lines.append(f"{i}. **{r.get('title')}** — {summary}")
    lines.append("")
    lines.append("## Fontes")
    for i, r in enumerate(top[:6], 1):
        lines.append(f"{i}. [{r.get('source')}] {r.get('title')} — {r.get('url')}")
    lines.append("")
    lines.append("## Próximos passos sugeridos")
    lines.append("- Comparar fontes acadêmicas com fontes técnicas recentes.")
    lines.append("- Validar dados financeiros em mais de uma fonte antes de tomar decisão.")
    lines.append("- Salvar os melhores links para criar uma base de conhecimento local da KIRA.")
    return "\n".join(lines)
