---
id: main
title: Script Principal
sidebar_position: 3
---

# Script Principal – `main.py`

O `main.py` define os agentes, tarefas e a crew do sistema Procurement AI.

## Agentes

### `cpv_specialist` – Especialista em CPV

```python
cpv_specialist = Agent(
    role="CPV Code Specialist",
    goal="Identify the correct CPV codes for the procurement category '{keyword}'",
    backstory=(
        "You are an expert in the EU Common Procurement Vocabulary (CPV) classification "
        "system used across European public procurement."
    ),
    tools=[cpv_lookup_tool],
    verbose=True,
)
```

### `ted_researcher` – Investigador TED Europa

```python
ted_researcher = Agent(
    role="EU Procurement Researcher",
    goal="Find and analyse European procurement notices for CPV code '{cpv_code}'",
    backstory=(
        "You are a specialist in EU public procurement who monitors TED daily. "
        "You understand procurement procedures and contract values across EU member states."
    ),
    tools=[ted_search_tool],
    verbose=True,
)
```

### `base_researcher` – Investigador BASE Portugal

```python
base_researcher = Agent(
    role="Portuguese Procurement Researcher",
    goal="Find and analyse public contracts on Portugal's BASE portal for '{keyword}'",
    backstory=(
        "You are a specialist in Portuguese public procurement law (CCP) "
        "and the BASE.gov.pt portal. You use the BASE REST API "
        "(base2/rest/contratos) to retrieve and analyse contracts, fetching details "
        "for the most relevant ones using their numeric IDs."
    ),
    tools=[base_portugal_search_tool, base_contract_detail_tool],
    verbose=True,
)
```

### `market_analyst` – Analista de Mercado

```python
market_analyst = Agent(
    role="Public Procurement Market Analyst",
    goal="Analyse procurement data from TED and BASE to identify market trends",
    backstory=(
        "You are a market intelligence expert specialising in public procurement. "
        "You combine data from EU and national sources to produce actionable insights."
    ),
    verbose=True,
)
```

### `report_writer` – Redator do Relatório

```python
report_writer = Agent(
    role="Procurement Intelligence Report Writer",
    goal="Write a comprehensive procurement market report for '{keyword}'",
    backstory=(
        "You are a professional writer specialising in public procurement intelligence reports."
    ),
    verbose=True,
)
```

## Tarefas

| Tarefa | Agente | Output |
|---|---|---|
| `cpv_task` | `cpv_specialist` | Lista de códigos CPV relevantes |
| `ted_task` | `ted_researcher` | Anúncios TED + resumo de valores |
| `base_task` | `base_researcher` | Contratos BASE + detalhes via REST API |
| `analysis_task` | `market_analyst` | Análise de tendências e compradores |
| `report_task` | `report_writer` | Relatório Markdown completo |

## Crew e Execução

```python
crew = Crew(
    agents=[cpv_specialist, ted_researcher, base_researcher, market_analyst, report_writer],
    tasks=[cpv_task, ted_task, base_task, analysis_task, report_task],
    process=Process.sequential,
    verbose=True,
)

crew.kickoff(inputs={"keyword": keyword, "cpv_code": cpv_code, "country": country})
```

## Estrutura do Relatório Gerado

O relatório final `output/relatorio_contratacao.md` tem 6 secções:

1. **Resumo Executivo** – síntese dos principais indicadores
2. **Enquadramento CPV** – descrição do código CPV e categorias relacionadas
3. **Mercado Europeu (TED)** – concursos europeus recentes
4. **Mercado Português (BASE)** – contratos portugueses celebrados
5. **Análise de Mercado** – tendências, compradores e valores
6. **Oportunidades e Recomendações** – estratégia para participar em concursos

## Próximo passo

Vê a [Configuração do Ambiente →](./environment)
