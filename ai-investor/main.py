"""
AI Investor – Script Principal

Sistema multi-agente com CrewAI para análise financeira automatizada.
Gera um relatório de investimento completo para uma dada acção (ticker).

Uso:
    python main.py [TICKER]

    Ex: python main.py NVDA
        python main.py AAPL
"""

import sys
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from tools import technical_analysis_tool
from pdf_utils import exportar_para_pdf

# ── Ferramentas ───────────────────────────────────────────────────────────────

search_tool = SerperDevTool()

# ── Agentes ───────────────────────────────────────────────────────────────────

researcher = Agent(
    role="Financial News Researcher",
    goal="Find the latest and most relevant news about {ticker}",
    backstory=(
        "You are an expert financial journalist with access to global news sources. "
        "You specialise in finding market-moving news and summarising them clearly."
    ),
    tools=[search_tool],
    verbose=True,
)

analyst = Agent(
    role="Technical Analyst",
    goal="Analyze market indicators for {ticker} and identify trends",
    backstory=(
        "You are a seasoned technical analyst with 15 years of experience. "
        "You interpret RSI, moving averages and price patterns to forecast trends."
    ),
    tools=[technical_analysis_tool],
    verbose=True,
)

investor = Agent(
    role="Investment Strategist",
    goal="Decide if {ticker} is a buy, sell or hold based on all available data",
    backstory=(
        "You are a hedge fund portfolio manager known for disciplined, data-driven "
        "investment decisions. You weigh news sentiment against technical signals."
    ),
    verbose=True,
)

writer = Agent(
    role="Financial Report Writer",
    goal="Write a clear, professional investment report for {ticker}",
    backstory=(
        "You are a financial writer who produces institutional-quality reports. "
        "You translate complex analysis into clear, actionable insights."
    ),
    verbose=True,
)

# ── Tarefas ───────────────────────────────────────────────────────────────────

news_task = Task(
    description=(
        "Research the latest news about {ticker} from the last 24 hours. "
        "Focus on earnings, analyst upgrades/downgrades, macro events and "
        "any news that could impact the stock price."
    ),
    expected_output=(
        "A concise summary (3–5 bullet points) of the most relevant recent "
        "news about {ticker}, with source links where available."
    ),
    agent=researcher,
)

analysis_task = Task(
    description=(
        "Perform a technical analysis of {ticker}. "
        "Calculate and interpret: current price, RSI (14-day), SMA20 and SMA50. "
        "Identify if the stock is overbought, oversold, or in a trend."
    ),
    expected_output=(
        "A technical summary including: current price, RSI value with "
        "interpretation, SMA20/SMA50 values and whether a golden cross or "
        "death cross is present."
    ),
    agent=analyst,
)

decision_task = Task(
    description=(
        "Based on the news research and technical analysis, create a clear "
        "investment thesis for {ticker}. State a recommendation: BUY, SELL, or HOLD. "
        "Include a confidence score (0–100) and key reasons."
    ),
    expected_output=(
        "Investment thesis with: recommendation (BUY/SELL/HOLD), "
        "confidence score (0–100), supporting rationale (2–3 sentences), "
        "and key risks."
    ),
    agent=investor,
)

report_task = Task(
    description=(
        "Write a complete investment report for {ticker} with the following sections:\n\n"
        "1. Executive Summary\n"
        "2. Market News\n"
        "3. Technical Analysis\n"
        "4. Investment Thesis\n"
        "5. Key Risks\n"
        "6. Final Recommendation\n\n"
        "The report should be professional, clear and suitable for an institutional investor."
    ),
    expected_output=(
        "A complete Markdown investment report with all 6 sections filled in, "
        "ready to be shared with stakeholders."
    ),
    agent=writer,
    output_file="output/relatorio_investimento.md",
)

# ── Crew ──────────────────────────────────────────────────────────────────────

crew = Crew(
    agents=[researcher, analyst, investor, writer],
    tasks=[news_task, analysis_task, decision_task, report_task],
    process=Process.sequential,
    verbose=True,
)

# ── Entrada ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "NVDA"
    print(f"\n🚀 A analisar {ticker}...\n")

    crew.kickoff(inputs={"ticker": ticker})

    # Exportar relatório para PDF
    exportar_para_pdf(
        md_path="output/relatorio_investimento.md",
        pdf_path=f"output/relatorio_{ticker}.pdf",
    )
    print(f"\n✅ Relatório guardado em output/relatorio_{ticker}.pdf")
