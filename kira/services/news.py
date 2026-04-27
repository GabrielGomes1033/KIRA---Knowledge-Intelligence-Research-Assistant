import feedparser

FEEDS = {
    "tecnologia": [
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.arstechnica.com/arstechnica/index",
    ],
    "mercado": [
        "https://finance.yahoo.com/news/rssindex",
        "https://www.infomoney.com.br/feed/",
    ],
    "ciencia": [
        "https://www.sciencedaily.com/rss/top/science.xml",
    ]
}


def feed_news(topic: str, limit: int = 5) -> list[dict]:
    items = []
    for feed in FEEDS.get(topic, []):
        parsed = feedparser.parse(feed)
        for e in parsed.entries[:limit]:
            items.append({
                "title": e.get("title", ""),
                "summary": e.get("summary", "")[:500],
                "url": e.get("link", ""),
                "source": topic,
            })
    return items[:limit]
