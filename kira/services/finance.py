import yfinance as yf
import requests
from kira.config import TIMEOUT


def get_asset_summary(symbol: str) -> dict:
    symbol = symbol.strip().upper()
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo")
        info = ticker.info or {}
        if hist.empty:
            return {"error": f"Não encontrei dados para {symbol}. Tente PETR4.SA, VALE3.SA, BTC-USD, AAPL."}
        current = float(hist["Close"].iloc[-1])
        first = float(hist["Close"].iloc[0])
        change = ((current - first) / first) * 100 if first else 0
        return {
            "symbol": symbol,
            "name": info.get("longName") or info.get("shortName") or symbol,
            "price": round(current, 4),
            "currency": info.get("currency", ""),
            "month_change_percent": round(change, 2),
            "market_cap": info.get("marketCap"),
            "sector": info.get("sector"),
            "summary": info.get("longBusinessSummary", "Resumo fundamentalista indisponível."),
        }
    except Exception as exc:
        return {"error": str(exc)}


def get_brl_rates() -> dict:
    try:
        r = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as exc:
        return {"error": str(exc)}
