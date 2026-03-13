---
id: architecture
title: Arquitectura do Sistema
sidebar_position: 5
---

# Arquitectura do Sistema

## Fluxo de dados

```
+-------------------+
|  Research Agent   |
| (News Scraping)   |
+---------+---------+
          |
          |  notícias recentes sobre o ticker
          v
+-------------------+
| Technical Analyst |
| RSI / SMA / Data  |
+---------+---------+
          |
          |  indicadores técnicos
          v
+-------------------+
| Investor Agent    |
| Strategy Decision |
+---------+---------+
          |
          |  tese de investimento
          v
+-------------------+
| Writer Agent      |
| Report Generator  |
+---------+---------+
          |
          v
     PDF / Markdown
```

## Stack Tecnológico

| Componente | Tecnologia |
|---|---|
| Framework de agentes | CrewAI |
| LLM padrão | OpenAI GPT-4o |
| Dados financeiros | yfinance |
| Pesquisa web | SerperDev API |
| Containerização | Docker + Docker Compose |
| Exportação PDF | fpdf2 |

## Processo Sequencial vs. Hierárquico

### Sequential (padrão neste projecto)

```python
process=Process.sequential
```

- Cada agente executa na ordem definida
- Cada agente recebe o output do anterior como contexto
- Mais simples e previsível

### Hierarchical (avançado)

```python
process=Process.hierarchical
manager_llm=ChatOpenAI(model="gpt-4o")
```

- Um agente manager coordena os outros
- Os agentes podem executar em paralelo
- Ideal para sistemas com muitos agentes independentes

## Próximo passo

Vê as [Ideias Avançadas →](./advanced)
