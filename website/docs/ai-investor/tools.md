---
id: tools
title: Ferramenta de Análise Técnica
sidebar_position: 2
---

# Ferramenta de Análise Técnica

O ficheiro `tools.py` implementa a ferramenta de análise técnica que os agentes utilizam para obter dados de mercado e calcular indicadores.

## Código: `tools.py`

```python
import yfinance as yf
from crewai.tools import tool

@tool("technical_analysis_tool")
def technical_analysis_tool(ticker: str) -> dict:
    """
    Realiza análise técnica de uma acção.
    Retorna preço actual, RSI, SMA20 e SMA50.
    """
    data = yf.download(ticker, period="3mo", interval="1d")

    # Médias Móveis Simples
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    # RSI (Relative Strength Index)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return {
        "price": float(data['Close'].iloc[-1]),
        "rsi": float(data['RSI'].iloc[-1]),
        "sma20": float(data['SMA_20'].iloc[-1]),
        "sma50": float(data['SMA_50'].iloc[-1]),
    }
```

## Indicadores calculados

| Indicador | Descrição | Interpretação |
|---|---|---|
| `price` | Preço de fecho mais recente | Referência de mercado |
| `rsi` | Relative Strength Index (14 dias) | `>70` sobrecomprado, `<30` sobrevendido |
| `sma20` | Média Móvel Simples de 20 dias | Tendência de curto prazo |
| `sma50` | Média Móvel Simples de 50 dias | Tendência de médio prazo |

## Por que retornar um dicionário?

:::tip Boa prática
Retornar um **dicionário** (ou JSON) em vez de uma string simples facilita a leitura dos dados pelos agentes, que podem referir valores específicos nas suas análises.
:::

## Próximo passo

Vê o [Script Principal →](./main)
