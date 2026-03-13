---
id: overview
title: Visão Geral – Contratação Pública
sidebar_position: 1
---

# Projecto Procurement AI

O **Procurement AI** é um sistema multi-agente construído com CrewAI que analisa automaticamente o mercado de contratação pública europeia e portuguesa, usando as APIs oficiais da UE e de Portugal.

## APIs utilizadas

| API | Fonte | Dados |
|---|---|---|
| **TED Europa REST API** | [ted.europa.eu](https://api.ted.europa.eu) | Anúncios de concursos públicos da UE |
| **SIMAP CPV API** | [simap.ted.europa.eu](https://simap.ted.europa.eu/pt/simap/cpv) | Vocabulário Comum de Contratos Públicos |
| **BASE Portugal API** | [base.gov.pt](https://www.base.gov.pt) | Contratos públicos celebrados em Portugal |

## O que faz

1. **Identifica códigos CPV** relevantes para uma categoria de produto/serviço
2. **Pesquisa anúncios** de concursos europeus via TED Europa
3. **Pesquisa contratos** celebrados em Portugal via BASE.gov.pt
4. **Analisa o mercado** – compradores, valores, tendências
5. **Gera um relatório** completo em Markdown

## O que é o CPV?

O **CPV (Common Procurement Vocabulary)** é o sistema de classificação da União Europeia para contratos públicos. É composto por códigos numéricos de 8 dígitos que identificam categorias de produtos, serviços e obras.

```
72000000 – Serviços de tecnologias de informação
45000000 – Trabalhos de construção
33000000 – Equipamento médico e farmacêutico
73000000 – Serviços de investigação e desenvolvimento
```

Todos os contratos públicos da UE acima dos limites regulamentares são obrigatoriamente publicados no **TED (Tenders Electronic Daily)** com o respetivo código CPV.

🔗 Explora os códigos CPV em: [simap.ted.europa.eu/pt/simap/cpv](https://ted.europa.eu/pt/simap/cpv)

## Agentes

| Agente | Papel | Ferramentas |
|---|---|---|
| `cpv_specialist` | Identifica os códigos CPV correctos | `cpv_lookup_tool` |
| `ted_researcher` | Pesquisa anúncios TED Europa | `ted_search_tool` |
| `base_researcher` | Pesquisa e detalha contratos BASE Portugal | `base_portugal_search_tool`, `base_contract_detail_tool` |
| `market_analyst` | Analisa tendências de mercado | — |
| `report_writer` | Redige o relatório final | — |

## Fluxo de execução

```
cpv_specialist → ted_researcher → base_researcher → market_analyst → report_writer
                                                                          ↓
                                                         output/relatorio_contratacao.md
```

## Output esperado

```
output/
└── relatorio_contratacao.md   ← Relatório de inteligência de mercado em Markdown
```

## Próximo passo

Vê como implementar as [Ferramentas de API →](./tools)
