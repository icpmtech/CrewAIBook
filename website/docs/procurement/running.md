---
id: running
title: Executar o Projecto
sidebar_position: 6
---

# Executar o Projecto

## Pré-requisitos

- Python 3.10+
- Chave de API OpenAI (ou alternativa compatível com CrewAI)
- Ligação à Internet (para aceder a TED Europa e BASE Portugal)

## Execução local

```bash
cd procurement

# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
cp .env.example .env
# edita .env e preenche OPENAI_API_KEY

# 3. Executar com os parâmetros padrão
python main.py

# 4. Executar com parâmetros personalizados
python main.py "KEYWORD" "CPV_CODE" "COUNTRY"
```

## Exemplos

```bash
# Software de gestão em Portugal (CPV 72000000)
python main.py "software gestão" 72000000 PT

# Obras de construção em Portugal (CPV 45000000)
python main.py "obras construção" 45000000 PT

# Serviços de consultoria em Portugal (CPV 73000000)
python main.py "consultoria" 73000000 PT

# Equipamento médico a nível europeu (CPV 33000000)
python main.py "equipamento médico" 33000000 EU

# Serviços de limpeza em Espanha (CPV 90910000)
python main.py "limpeza" 90910000 ES
```

## Output

O relatório é guardado em `output/relatorio_contratacao.md`:

```markdown
# Relatório de Inteligência de Mercado – Software de Gestão

## 1. Resumo Executivo
...

## 2. Enquadramento CPV
CPV 72000000 – Serviços de tecnologias de informação
...

## 3. Mercado Europeu (TED Europa)
| ID | Título | Entidade | Valor | Data |
|---|---|---|---|---|
...

## 4. Mercado Português (BASE.gov.pt)
...

## 5. Análise de Mercado
...

## 6. Oportunidades e Recomendações
...
```

## Execução com Docker

Consulta a secção [Docker →](./docker) para executar via contentor.

## Referências de API

| API | URL | Documentação |
|---|---|---|
| TED Europa REST API | api.ted.europa.eu | [Swagger](https://api.ted.europa.eu/swagger-ui.html) |
| SIMAP CPV Browser | ted.europa.eu/pt/simap/cpv | [Portal](https://ted.europa.eu/pt/simap/cpv) |
| BASE Portugal | base.gov.pt | [Portal](https://www.base.gov.pt) |
