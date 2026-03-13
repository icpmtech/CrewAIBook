---
id: environment
title: Variáveis de Ambiente
sidebar_position: 5
---

# Variáveis de Ambiente

As chaves de API e configurações sensíveis são geridas através de um ficheiro `.env`.

## Ficheiro `.env`

```bash
# OpenAI (modelo padrão do CrewAI)
OPENAI_API_KEY=sk-...

# Serper (pesquisa web para o researcher agent)
SERPER_API_KEY=...
```

## Alternativas ao OpenAI

O CrewAI suporta vários fornecedores de LLM. Configura as variáveis conforme o modelo escolhido:

### Google Gemini

```bash
GOOGLE_API_KEY=...
```

```python
from crewai import LLM

llm = LLM(model="gemini/gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
```

### Anthropic Claude

```bash
ANTHROPIC_API_KEY=...
```

```python
llm = LLM(model="claude-3-5-sonnet-20241022")
```

### DeepSeek

```bash
DEEPSEEK_API_KEY=...
```

```python
llm = LLM(model="deepseek/deepseek-chat", base_url="https://api.deepseek.com/v1")
```

### Ollama (100% local, sem API)

```bash
# Não precisa de API key
```

```python
llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
```

## Segurança

:::danger
Nunca commites o ficheiro `.env` com chaves reais para um repositório público.
:::

Adiciona ao `.gitignore`:

```gitignore
.env
output/
__pycache__/
*.pyc
```

## Próximo passo

Aprende a exportar relatórios para [PDF →](./pdf-export)
