---
id: docker
title: Docker
sidebar_position: 5
---

# Docker

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p output

CMD ["python", "main.py"]
```

## docker-compose.yml

```yaml
services:
  procurement:
    build: .
    env_file: .env
    volumes:
      - ./output:/app/output
    command: python main.py "${KEYWORD:-software gestão}" "${CPV_CODE:-72000000}" "${COUNTRY:-PT}"
```

## Executar com Docker Compose

```bash
# Análise padrão (software de gestão, CPV 72000000, Portugal)
docker compose up

# Personalizar a pesquisa via variáveis de ambiente
KEYWORD="obras construção" CPV_CODE="45000000" COUNTRY="PT" docker compose up

# Reconstruir a imagem após alterações
docker compose up --build
```

## Verificar o output

```bash
# Ver o relatório gerado
cat output/relatorio_contratacao.md
```

## Próximo passo

Vê as [Instruções de Execução →](./running)
