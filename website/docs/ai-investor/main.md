---
id: main
title: Script Principal
sidebar_position: 3
---

# Script Principal

O ficheiro `main.py` define todos os agentes, tarefas e o crew que os orquestra.

## Código: `main.py`

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from tools import technical_analysis_tool

# Ferramentas
search_tool = SerperDevTool()

# ── Agentes ─────────────────────────────────────────────────────────────────

researcher = Agent(
    role="Financial News Researcher",
    goal="Find latest news about {ticker}",
    tools=[search_tool],
    verbose=True,
)

analyst = Agent(
    role="Technical Analyst",
    goal="Analyze market indicators for {ticker}",
    tools=[technical_analysis_tool],
    verbose=True,
)

investor = Agent(
    role="Investment Strategist",
    goal="Decide if {ticker} is a buy or sell",
    verbose=True,
)

writer = Agent(
    role="Financial Report Writer",
    goal="Write a professional investment report",
    verbose=True,
)

# ── Tarefas ──────────────────────────────────────────────────────────────────

news_task = Task(
    description="Find latest news for {ticker} in last 24h",
    expected_output="A summary of the most relevant news about {ticker}.",
    agent=researcher,
)

analysis_task = Task(
    description="Perform technical analysis for {ticker}",
    expected_output="RSI, SMA20, SMA50 and current price for {ticker}.",
    agent=analyst,
)

decision_task = Task(
    description="Create investment thesis based on news and technical data",
    expected_output="A clear BUY, SELL or HOLD recommendation with rationale.",
    agent=investor,
)

report_task = Task(
    description="""
Write an investment report with the following structure:

1. Executive Summary
2. Market News
3. Technical Analysis
4. Investment Thesis
5. Risks
6. Final Recommendation
""",
    expected_output="A complete Markdown investment report.",
    agent=writer,
    output_file="output/relatorio_investimento.md",
)

# ── Crew ─────────────────────────────────────────────────────────────────────

crew = Crew(
    agents=[researcher, analyst, investor, writer],
    tasks=[news_task, analysis_task, decision_task, report_task],
    process=Process.sequential,
)

if __name__ == "__main__":
    crew.kickoff(inputs={"ticker": "NVDA"})
```

## Notas importantes

### `expected_output`
A partir do CrewAI v0.30+, cada `Task` deve ter um campo `expected_output` que descreve o que o agente deve produzir. Isto melhora a qualidade dos resultados.

### `output_file`
O parâmetro `output_file` na última tarefa guarda automaticamente o output em Markdown.

### `Process.sequential`
O processo sequencial garante que cada agente recebe o contexto de todos os anteriores antes de executar.

## Próximo passo

Configura o [Docker →](./docker)
