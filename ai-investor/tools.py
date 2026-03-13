"""
AI Investor – Ferramenta de Análise Técnica
"""

import yfinance as yf
from crewai.tools import tool


@tool("technical_analysis_tool")
def technical_analysis_tool(ticker: str) -> dict:
    """
    Realiza análise técnica de uma acção.

    Calcula o preço actual, RSI (14 dias), SMA20 e SMA50
    com base nos últimos 3 meses de dados históricos.

    Args:
        ticker: Símbolo da acção (ex: 'NVDA', 'AAPL').

    Returns:
        Dicionário com price, rsi, sma20 e sma50.
    """
    data = yf.download(ticker, period="3mo", interval="1d", progress=False)

    if data.empty:
        return {"error": f"Sem dados disponíveis para o ticker '{ticker}'."}

    # Médias Móveis Simples
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["SMA_50"] = data["Close"].rolling(window=50).mean()

    # RSI (Relative Strength Index – 14 dias)
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    return {
        "ticker": ticker,
        "price": float(data["Close"].iloc[-1]),
        "rsi": float(data["RSI"].iloc[-1]),
        "sma20": float(data["SMA_20"].iloc[-1]),
        "sma50": float(data["SMA_50"].iloc[-1]),
    }
