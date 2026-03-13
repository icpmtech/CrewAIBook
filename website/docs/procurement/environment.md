---
id: environment
title: Configuração do Ambiente
sidebar_position: 4
---

# Configuração do Ambiente

## Variáveis de Ambiente

Copia o ficheiro `.env.example` para `.env` e preenche as variáveis necessárias:

```bash
cp .env.example .env
```

### `.env.example`

```bash
# OpenAI (modelo padrão do CrewAI)
OPENAI_API_KEY=

# Alternativas (descomenta conforme o modelo escolhido):
# GOOGLE_API_KEY=
# ANTHROPIC_API_KEY=
# DEEPSEEK_API_KEY=

# TED Europa API (opcional – sem chave funciona em modo público)
# TED_API_KEY=
```

## API TED Europa

A API TED suporta dois modos de acesso:

| Modo | Autenticação | Limite |
|---|---|---|
| **Público** | Sem chave | 10 req/min |
| **Registado** | Bearer token | 100 req/min |

Para obter uma chave API TED:
1. Regista-te em [api.ted.europa.eu](https://api.ted.europa.eu)
2. Cria uma aplicação no portal
3. Copia o token para a variável `TED_API_KEY`

:::note Modo público
Para experimentar o sistema, não é necessária nenhuma chave API TED.
As ferramentas funcionam em modo público com limites mais baixos.
:::

## API BASE Portugal

O portal BASE.gov.pt disponibiliza dados públicos de contratos sem necessidade de autenticação.

🔗 [www.base.gov.pt](https://www.base.gov.pt)

## Instalação de dependências

```bash
cd procurement
pip install -r requirements.txt
```

### `requirements.txt`

```
crewai>=0.30.0
crewai-tools>=0.1.0
httpx>=0.27.0
python-dotenv>=1.0.0
```

## Próximo passo

Vê como [Executar o Projecto →](./running)
