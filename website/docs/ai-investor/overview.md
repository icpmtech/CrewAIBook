---
id: overview
title: Visão Geral do AI Investor
sidebar_position: 1
---

# Projecto AI Investor

O **AI Investor** é um sistema multi-agente construído com CrewAI que analisa automaticamente stocks e gera relatórios de investimento profissionais.

## O que faz

1. **Investiga notícias** recentes sobre uma acção (ex: NVDA)
2. **Analisa indicadores técnicos** (RSI, SMA20, SMA50)
3. **Toma uma decisão** de investimento fundamentada
4. **Gera um relatório** completo em Markdown e PDF

## Agentes

| Agente | Papel | Ferramentas |
|---|---|---|
| `researcher` | Pesquisa notícias financeiras recentes | SerperDev (busca web) |
| `analyst` | Calcula indicadores técnicos | `technical_analysis_tool` |
| `investor` | Define estratégia de investimento | — |
| `writer` | Redige o relatório final | — |

## Fluxo de execução

```
researcher → analyst → investor → writer → output/relatorio_investimento.md
```

O processo é **sequencial** — cada agente recebe o contexto do anterior.

## Output esperado

```
output/
└── relatorio_investimento.md   ← Relatório em Markdown
└── relatorio_investimento.pdf  ← Relatório em PDF (opcional)
```

## Próximo passo

Vê como implementar a [Ferramenta de Análise Técnica →](./tools)
