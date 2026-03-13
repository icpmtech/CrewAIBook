---
id: advanced
title: Ideias Avançadas
sidebar_position: 6
---

# Ideias Avançadas

## 1️⃣ Multi-agente para Portfólio Completo

Em vez de analisar uma só acção, cria um crew que gere um portfólio inteiro:

```python
portfolio_manager = Agent(
    role="Portfolio Manager",
    goal="Optimize the overall portfolio allocation",
    verbose=True,
)

risk_analyst = Agent(
    role="Risk Analyst",
    goal="Assess and quantify portfolio risk",
    verbose=True,
)

dividend_analyst = Agent(
    role="Dividend Analyst",
    goal="Identify best dividend-paying stocks",
    verbose=True,
)

macro_economist = Agent(
    role="Macro Economist",
    goal="Analyse macro-economic trends affecting the portfolio",
    verbose=True,
)
```

## 2️⃣ Integração com API Própria

Se tens uma API de análise de mercado (ex: `marketanalyticshubapp.azurewebsites.net`), podes criar uma ferramenta personalizada:

```python
import requests
from crewai.tools import tool

@tool("market_api_tool")
def market_api_tool(ticker: str) -> dict:
    """Obtém dados da API de análise de mercado."""
    response = requests.get(
        f"https://marketanalyticshubapp.azurewebsites.net/api/stock/{ticker}",
        headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"},
    )
    return response.json()
```

## 3️⃣ Sinais de Auto-Trading

Estrutura o output do agente para gerar sinais de trading accionáveis:

```python
trading_task = Task(
    description="Generate a trading signal for {ticker}",
    expected_output="One of: BUY, SELL, or HOLD with confidence score 0-100.",
    agent=investor,
)
```

Output exemplo:

```json
{
  "signal": "BUY",
  "confidence": 78,
  "rationale": "RSI em zona neutra (52), SMA20 acima de SMA50 (golden cross), notícias positivas sobre crescimento da IA."
}
```

## 4️⃣ Dashboard Automático

Gera gráficos junto com o relatório:

```python
import matplotlib.pyplot as plt
import yfinance as yf

def gerar_graficos(ticker: str, output_dir: str = "output"):
    data = yf.download(ticker, period="3mo")

    # Gráfico RSI
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    axes[0].plot(data['Close'], label="Preço")
    axes[0].set_title(f"{ticker} – Preço de Fecho")
    axes[0].legend()

    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + gain / loss))

    axes[1].plot(rsi, label="RSI", color="orange")
    axes[1].axhline(70, color="red", linestyle="--", label="Sobrecomprado")
    axes[1].axhline(30, color="green", linestyle="--", label="Sobrevendido")
    axes[1].set_title(f"{ticker} – RSI (14)")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(f"{output_dir}/{ticker}_dashboard.png", dpi=150)
    plt.close()
```

## 5️⃣ Versão com Ollama (100% Local)

Para executar sem qualquer API paga, usa o Ollama:

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descarregar modelo
ollama pull llama3.2
```

```python
from crewai import LLM

llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

analyst = Agent(
    role="Technical Analyst",
    goal="Analyze market indicators for {ticker}",
    llm=llm,
    tools=[technical_analysis_tool],
    verbose=True,
)
```

## 6️⃣ Arquitectura de Hedge Fund (10 agentes)

Um sistema completo de investimento institucional:

| Agente | Função |
|---|---|
| Data Collector | Recolhe dados de mercado em tempo real |
| News Analyst | Analisa sentimento de notícias |
| Technical Analyst | Indicadores técnicos (RSI, MACD, Bollinger) |
| Fundamental Analyst | P/E, EPS, balanço patrimonial |
| Macro Economist | PIB, inflação, taxas de juro |
| Risk Manager | VaR, drawdown máximo, diversificação |
| Portfolio Manager | Alocação óptima de activos |
| Compliance Officer | Verificação de regras e limites |
| Report Writer | Relatório diário para stakeholders |
| Executive Summarizer | Sumário executivo para decisores |
