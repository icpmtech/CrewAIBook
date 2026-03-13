---
id: project-structure
title: Estrutura do Projeto
sidebar_position: 3
---

# Estrutura do Projeto

O projeto **AI Investor** segue uma estrutura simples e organizada:

```
ai-investor/
│
├── main.py               ← Script principal (agentes, tarefas, crew)
├── tools.py              ← Ferramentas personalizadas (análise técnica)
├── requirements.txt      ← Dependências Python
├── Dockerfile            ← Imagem Docker
├── docker-compose.yml    ← Orquestração de containers
├── .env                  ← Variáveis de ambiente (API keys)
│
└── output/               ← Pasta de saída (relatórios PDF/Markdown)
```

## Descrição de cada ficheiro

| Ficheiro | Descrição |
|---|---|
| `main.py` | Define os agentes, tarefas e inicia o crew |
| `tools.py` | Ferramenta de análise técnica (RSI, SMA) com yfinance |
| `requirements.txt` | Lista de dependências do projeto |
| `Dockerfile` | Define a imagem Docker para o projecto |
| `docker-compose.yml` | Facilita a execução com volumes e variáveis de ambiente |
| `.env` | Guarda as API keys (não commitar para o repositório!) |
| `output/` | Directório onde os relatórios são guardados |

:::warning
Nunca commites o ficheiro `.env` para o repositório público. Usa `.gitignore` para o excluir.
:::

## Próximo passo

Explora a [Ferramenta de Análise Técnica →](./ai-investor/tools)
