---
id: running
title: Executar o Projecto
sidebar_position: 7
---

# Executar o Projecto

## Com Docker (recomendado)

### 1. Configura as variáveis de ambiente

Cria o ficheiro `.env` na raiz do projecto:

```bash
cp .env.example .env
# Edita .env com as tuas chaves de API
```

### 2. Constrói e executa

```bash
docker compose up
```

O Docker irá:
1. Construir a imagem com todas as dependências
2. Executar o `main.py`
3. Guardar os resultados em `./output/`

### 3. Ver os resultados

```bash
cat output/relatorio_investimento.md
```

## Sem Docker (directo)

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
export OPENAI_API_KEY=sk-...
export SERPER_API_KEY=...

# Executar
python main.py
```

## Personalizar o ticker

Para analisar uma acção diferente, edita a última linha do `main.py`:

```python
# Analisar Apple em vez de NVIDIA
crew.kickoff(inputs={"ticker": "AAPL"})
```

Ou passa como argumento (versão avançada):

```python
import sys

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "NVDA"
    crew.kickoff(inputs={"ticker": ticker})
```

```bash
python main.py AAPL
```

## Output esperado

```
output/
├── relatorio_investimento.md   ← Relatório completo em Markdown
└── relatorio_investimento.pdf  ← Versão PDF (se usares a função exportar_para_pdf)
```

## Próximo passo

Explora a [Arquitectura do Sistema →](../architecture)
