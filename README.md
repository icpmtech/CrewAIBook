# CrewAI Book

**Guia Prático – Multi-Agentes com CrewAI + Docker**

Documentação e código fonte para o livro/guia sobre criação de sistemas
multi-agente com [CrewAI](https://docs.crewai.com), incluindo um projecto
completo de análise financeira automatizada.

## 📚 Documentação (Docusaurus)

A documentação está em [`website/`](./website/) e pode ser visualizada localmente:

```bash
cd website
npm install
npm start
```

## 🤖 Projecto AI Investor

O projecto de exemplo está em [`ai-investor/`](./ai-investor/).

### Início rápido

```bash
cd ai-investor
cp .env.example .env
# Preenche as API keys no .env
docker compose up
```

O relatório é guardado em `ai-investor/output/`.

## 📂 Estrutura do Repositório

```
CrewAIBook/
├── ai-investor/      ← Projecto completo de análise financeira
│   ├── main.py
│   ├── tools.py
│   ├── pdf_utils.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
│
└── website/          ← Site de documentação (Docusaurus)
    ├── docs/
    └── src/
```

## 🔗 Links

- [Documentação CrewAI](https://docs.crewai.com)
- [SerperDev API](https://serper.dev)
- [yfinance](https://pypi.org/project/yfinance/)
