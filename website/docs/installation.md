---
id: installation
title: Instalação
sidebar_position: 2
---

# Instalação

## Requisitos

- **Python 3.10+**
- **pip**
- (Opcional) Docker & Docker Compose para execução containerizada

## Instalar o CrewAI

```bash
pip install crewai crewai-tools
```

## Bibliotecas Adicionais

Para o projeto **AI Investor** e funcionalidades avançadas:

```bash
pip install pandas yfinance fpdf2 python-dotenv
```

| Biblioteca | Finalidade |
|---|---|
| `pandas` | Manipulação de dados e séries temporais |
| `yfinance` | Dados financeiros do Yahoo Finance |
| `fpdf2` | Geração de ficheiros PDF |
| `python-dotenv` | Gestão de variáveis de ambiente via `.env` |

## Verificar Instalação

```bash
python -c "import crewai; print(crewai.__version__)"
```

## Chaves de API necessárias

O CrewAI utiliza por defeito a **OpenAI API**. Também suporta:

- [OpenAI](https://platform.openai.com/) – padrão
- [Google Gemini](https://ai.google.dev/)
- [Anthropic Claude](https://www.anthropic.com/)
- [DeepSeek](https://www.deepseek.com/)
- [Ollama](https://ollama.com/) – execução 100% local, sem API

## Próximo passo

Conhece a [Estrutura do Projeto →](./project-structure)
