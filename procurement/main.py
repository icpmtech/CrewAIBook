"""
Procurement AI – Script Principal

Sistema multi-agente com CrewAI para análise de contratação pública europeia e portuguesa.
Usa a API TED (Tenders Electronic Daily) da UE e o portal BASE de Portugal.

Uso:
    python main.py [KEYWORD] [CPV_CODE] [COUNTRY]

    Ex: python main.py "software gestão" 72000000 PT
        python main.py "obras construção" 45000000 PT
        python main.py "serviços consultoria" 73000000 EU
"""

import sys
from crewai import Agent, Task, Crew, Process
from tools import ted_search_tool, cpv_lookup_tool, base_portugal_search_tool, base_contract_detail_tool

# ── Agentes ───────────────────────────────────────────────────────────────────

cpv_specialist = Agent(
    role="CPV Code Specialist",
    goal="Identify the correct CPV codes for the procurement category '{keyword}'",
    backstory=(
        "You are an expert in the EU Common Procurement Vocabulary (CPV) classification "
        "system used across European public procurement. You can quickly identify the "
        "right CPV codes for any category of goods, services or works."
    ),
    tools=[cpv_lookup_tool],
    verbose=True,
)

ted_researcher = Agent(
    role="EU Procurement Researcher",
    goal=(
        "Find and analyse European public procurement notices for CPV code '{cpv_code}' "
        "in country '{country}' using the TED Europa API"
    ),
    backstory=(
        "You are a specialist in EU public procurement who monitors the TED (Tenders "
        "Electronic Daily) journal daily. You understand procurement procedures, "
        "contract values and buying patterns across EU member states."
    ),
    tools=[ted_search_tool],
    verbose=True,
)

base_researcher = Agent(
    role="Portuguese Procurement Researcher",
    goal="Find and analyse public contracts published on Portugal's BASE portal for '{keyword}'",
    backstory=(
        "You are a specialist in Portuguese public procurement law (Código dos Contratos "
        "Públicos – CCP) and the BASE.gov.pt portal. You use the BASE REST API "
        "(base2/rest/contratos) to retrieve and analyse contracts, fetching details "
        "for the most relevant ones using their numeric IDs."
    ),
    tools=[base_portugal_search_tool, base_contract_detail_tool],
    verbose=True,
)

market_analyst = Agent(
    role="Public Procurement Market Analyst",
    goal=(
        "Analyse procurement data from TED and BASE to identify market trends, "
        "key buyers and contract value patterns for '{keyword}'"
    ),
    backstory=(
        "You are a market intelligence expert specialising in public procurement. "
        "You combine data from EU and national sources to produce actionable insights "
        "for companies wishing to participate in public tenders."
    ),
    verbose=True,
)

report_writer = Agent(
    role="Procurement Intelligence Report Writer",
    goal="Write a comprehensive procurement market report for '{keyword}' (CPV: {cpv_code})",
    backstory=(
        "You are a professional business writer specialising in public procurement. "
        "You produce clear, structured reports that help companies understand market "
        "opportunities and plan their bid strategy."
    ),
    verbose=True,
)

# ── Tarefas ───────────────────────────────────────────────────────────────────

cpv_task = Task(
    description=(
        "Search for CPV (Common Procurement Vocabulary) codes related to '{keyword}'. "
        "Find the most relevant CPV codes, their descriptions and parent categories. "
        "If a specific CPV code '{cpv_code}' is already provided, verify and describe it."
    ),
    expected_output=(
        "A list of 3–5 relevant CPV codes with their descriptions, "
        "including the most specific code for '{keyword}'. "
        "Format: CODE – Description."
    ),
    agent=cpv_specialist,
)

ted_task = Task(
    description=(
        "Search the TED Europa API for the 10 most recent procurement notices "
        "with CPV code '{cpv_code}' in country '{country}'. "
        "Extract: notice ID, title, buyer organisation, estimated value, "
        "publication date and the TED URL."
    ),
    expected_output=(
        "A structured list of up to 10 procurement notices from TED, each with: "
        "ID, title, buyer, estimated value, date and URL. "
        "Include a brief summary of total contract value and most active buyers."
    ),
    agent=ted_researcher,
)

base_task = Task(
    description=(
        "Use the BASE Portugal REST API (base2/rest/contratos) to retrieve recent public "
        "contracts. Fetch a batch of contracts using the Range-based pagination, then use "
        "base_contract_detail_tool to get full details for the most relevant contracts "
        "related to '{keyword}'. "
        "Extract: contract object, contracting entity, contractor, contract value and date."
    ),
    expected_output=(
        "A structured list of Portuguese contracts from BASE.gov.pt, each with: "
        "object, authority, contractor, value and date. "
        "Include a summary of total value and most active contracting entities."
    ),
    agent=base_researcher,
)

analysis_task = Task(
    description=(
        "Using the TED Europa and BASE Portugal data collected, analyse the public "
        "procurement market for '{keyword}' (CPV: {cpv_code}). "
        "Identify: key buyers, average contract values, seasonal patterns, "
        "market concentration and the most competitive segments."
    ),
    expected_output=(
        "A market analysis including: top 5 buyers by contract volume, "
        "average contract value range, key market trends, "
        "and recommended entry points for new market participants."
    ),
    agent=market_analyst,
)

report_task = Task(
    description=(
        "Write a complete procurement market intelligence report for '{keyword}' "
        "(CPV code: {cpv_code}, Country: {country}). Include the following sections:\n\n"
        "1. Resumo Executivo\n"
        "2. Enquadramento CPV\n"
        "3. Mercado Europeu (TED Europa)\n"
        "4. Mercado Português (BASE.gov.pt)\n"
        "5. Análise de Mercado\n"
        "6. Oportunidades e Recomendações\n\n"
        "The report should be in Portuguese and suitable for a company's business development team."
    ),
    expected_output=(
        "A complete Markdown report with all 6 sections, written in Portuguese, "
        "with tables, key figures and actionable recommendations."
    ),
    agent=report_writer,
    output_file="output/relatorio_contratacao.md",
)

# ── Crew ──────────────────────────────────────────────────────────────────────

crew = Crew(
    agents=[cpv_specialist, ted_researcher, base_researcher, market_analyst, report_writer],
    tasks=[cpv_task, ted_task, base_task, analysis_task, report_task],
    process=Process.sequential,
    verbose=True,
)

# ── Entrada ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "software gestão"
    cpv_code = sys.argv[2] if len(sys.argv) > 2 else "72000000"
    country = sys.argv[3].upper() if len(sys.argv) > 3 else "PT"

    print(f"\n🔍 A analisar mercado de contratação pública para: {keyword}")
    print(f"   CPV: {cpv_code} | País: {country}\n")

    crew.kickoff(inputs={"keyword": keyword, "cpv_code": cpv_code, "country": country})

    print(f"\n✅ Relatório guardado em output/relatorio_contratacao.md")
