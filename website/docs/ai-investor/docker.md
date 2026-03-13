---
id: docker
title: Docker e Docker Compose
sidebar_position: 4
---

# Docker e Docker Compose

Containerizar o projecto garante reprodutibilidade e facilita o deployment em qualquer ambiente.

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências primeiro (aproveitar cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY . .

# Criar directório de output
RUN mkdir -p output

CMD ["python", "main.py"]
```

## docker-compose.yml

```yaml
version: "3.8"

services:
  ai-investor:
    build: .
    volumes:
      - ./output:/app/output
    env_file:
      - .env
    restart: "no"
```

## requirements.txt

```text
crewai>=0.30.0
crewai-tools>=0.1.0
yfinance>=0.2.0
pandas>=2.0.0
fpdf2>=2.7.0
python-dotenv>=1.0.0
```

## Como funciona

1. O Docker constrói a imagem com todas as dependências
2. O volume `./output:/app/output` mapeia a pasta de output do container para a máquina local
3. As variáveis de ambiente são carregadas do ficheiro `.env`
4. O container executa `python main.py` e termina

## Boas práticas

:::tip Layers de Docker
Copiar o `requirements.txt` e instalar as dependências antes de copiar o código fonte aproveita o **layer cache** do Docker. Se o código mudar mas as dependências não, o Docker reutiliza o layer de instalação.
:::

:::warning
Nunca incluas o ficheiro `.env` na imagem Docker. Usa sempre `env_file` ou variáveis de ambiente externas.
:::

## Próximo passo

Configura as [Variáveis de Ambiente →](./environment)
