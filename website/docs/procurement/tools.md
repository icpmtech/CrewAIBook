---
id: tools
title: Ferramentas de API
sidebar_position: 2
---

# Ferramentas de API de Contratação Pública

O ficheiro `tools.py` implementa quatro ferramentas CrewAI para aceder às APIs oficiais de contratação pública.

## Ferramenta 1: `ted_search_tool`

Pesquisa anúncios de contratos públicos na plataforma **TED (Tenders Electronic Daily)** da União Europeia.

```python
from crewai.tools import tool
import httpx

TED_API_BASE = "https://api.ted.europa.eu/v3"

@tool("ted_search_tool")
def ted_search_tool(cpv_code: str, country: str = "PT", page_size: int = 10) -> dict:
    """
    Pesquisa anúncios de contratos públicos na plataforma TED da UE.

    Args:
        cpv_code:  Código CPV (ex: '72000000' para TI).
        country:   Código ISO do país (ex: 'PT' para Portugal, 'FR' para França).
        page_size: Número de resultados (por omissão 10).
    """
    query = f"cpv=={cpv_code} AND notice-country=={country}"
    params = {
        "q": query,
        "fields": "notice-id,publication-date,BT-21-Procedure,BT-500-Organization,estimated-value",
        "pageSize": page_size,
        "page": 1,
    }
    response = httpx.get(f"{TED_API_BASE}/notices/search", params=params, timeout=15)
    response.raise_for_status()
    return response.json()
```

### Parâmetros de pesquisa TED

A API TED suporta uma linguagem de pesquisa avançada. Exemplos:

| Filtro | Sintaxe | Exemplo |
|---|---|---|
| Código CPV | `cpv==XXXXXXXX` | `cpv==72000000` |
| País | `notice-country==XX` | `notice-country==PT` |
| Intervalo de datas | `publication-date>=[YYYY-MM-DD]` | `publication-date>=[2024-01-01]` |
| Valor estimado | `estimated-value>=N` | `estimated-value>=100000` |

🔗 Documentação completa: [api.ted.europa.eu](https://api.ted.europa.eu)

---

## Ferramenta 2: `cpv_lookup_tool`

Pesquisa códigos **CPV (Common Procurement Vocabulary)** pelo SIMAP da UE.

```python
SIMAP_CPV_API = "https://simap.ted.europa.eu/api/cpv"

@tool("cpv_lookup_tool")
def cpv_lookup_tool(keyword: str, lang: str = "pt") -> dict:
    """
    Pesquisa códigos CPV pelo SIMAP da UE.

    Args:
        keyword: Palavra-chave (ex: 'software', 'construção').
        lang:    Idioma ('pt', 'en', 'fr', etc.).
    """
    params = {"keyword": keyword, "lang": lang}
    response = httpx.get(f"{SIMAP_CPV_API}/search", params=params, timeout=10)
    response.raise_for_status()
    return response.json()
```

### Estrutura dos códigos CPV

Os códigos CPV têm 8 dígitos com a seguinte hierarquia:

```
72000000  ← Divisão (2 dígitos significativos)
  72200000  ← Grupo (3 dígitos)
    72210000  ← Classe (4 dígitos)
      72212000  ← Categoria (5 dígitos)
```

:::tip Portal SIMAP
Pode explorar todos os códigos CPV em:
[ted.europa.eu/pt/simap/cpv](https://ted.europa.eu/pt/simap/cpv)
:::

---

## Ferramenta 3: `base_portugal_search_tool`

Obtém contratos públicos celebrados em Portugal via a **API REST JSON do portal BASE.gov.pt**.

A abordagem usa o endpoint `base2/rest/contratos` com paginação por cabeçalho `Range`,
conforme documentado no projeto [ajcerejeira/base.gov.pt](https://github.com/ajcerejeira/base.gov.pt).

```python
# Endpoint REST JSON canónico do BASE Portugal
BASE_REST_API = "https://www.base.gov.pt/base2/rest/contratos"

@tool("base_portugal_search_tool")
def base_portugal_search_tool(start: int = 1, count: int = 20) -> dict:
    """
    Obtém contratos públicos do portal BASE de Portugal via API REST JSON.

    Args:
        start: Índice do primeiro contrato (por omissão 1).
        count: Número de contratos a obter (por omissão 20, máx. 100).
    """
    end = start + min(count, 100) - 1
    headers = {"Range": f"{start}-{end}"}
    response = httpx.get(BASE_REST_API, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()
```

### Paginação com cabeçalho `Range`

O endpoint `base2/rest/contratos` usa o cabeçalho HTTP `Range` para paginar os resultados:

```
Range: 1-20    → contratos 1 a 20
Range: 21-40   → contratos 21 a 40
Range: 101-200 → contratos 101 a 200
```

---

## Ferramenta 4: `base_contract_detail_tool`

Obtém os **detalhes completos** de um contrato específico pelo seu ID.

```python
@tool("base_contract_detail_tool")
def base_contract_detail_tool(contract_id: int) -> dict:
    """
    Obtém os detalhes de um contrato público português pelo seu ID.

    Args:
        contract_id: Identificador numérico único do contrato no BASE.
    """
    response = httpx.get(f"{BASE_REST_API}/{contract_id}", timeout=15)
    response.raise_for_status()
    return response.json()
```

O agente `base_researcher` usa esta ferramenta para obter informação detalhada (concorrentes,
documentos, CPVs, etc.) dos contratos mais relevantes identificados pela ferramenta anterior.

### BASE vs TED

| Característica | BASE Portugal | TED Europa |
|---|---|---|
| Cobertura | Apenas Portugal | 27 países da UE |
| Tipo de dados | Contratos celebrados | Anúncios de concursos |
| Limites financeiros | Todos os contratos | Acima dos limiares comunitários |
| API | `base2/rest/contratos` | `api.ted.europa.eu/v3` |
| Autenticação | Nenhuma | Opcional (público) |

:::info Referência
A estrutura da API BASE Portugal foi documentada pelo projeto open-source
[ajcerejeira/base.gov.pt](https://github.com/ajcerejeira/base.gov.pt).
:::

## Próximo passo

Vê o [Script Principal →](./main)
