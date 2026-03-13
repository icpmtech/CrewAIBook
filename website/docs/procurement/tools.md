---
id: tools
title: Ferramentas de API
sidebar_position: 2
---

# Ferramentas de API de Contratação Pública

O ficheiro `tools.py` implementa três ferramentas CrewAI para aceder às APIs oficiais de contratação pública.

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

Pesquisa contratos públicos celebrados em Portugal no portal **BASE.gov.pt**.

```python
BASE_API_BASE = "https://www.base.gov.pt/Base4"

@tool("base_portugal_search_tool")
def base_portugal_search_tool(keyword: str = "", cpv_code: str = "", page: int = 1) -> dict:
    """
    Pesquisa contratos públicos no portal BASE de Portugal.

    Args:
        keyword:  Texto livre para pesquisar no objeto do contrato.
        cpv_code: Código CPV para filtrar por categoria (opcional).
        page:     Número de página de resultados.
    """
    params = {"tipo": "contratos", "texto": keyword, "cpv": cpv_code, "pag": page}
    response = httpx.get(
        f"{BASE_API_BASE}/pt/resultados/",
        params={k: v for k, v in params.items() if v},
        headers={"Accept": "application/json"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
```

### BASE vs TED

| Característica | BASE Portugal | TED Europa |
|---|---|---|
| Cobertura | Apenas Portugal | 27 países da UE |
| Tipo de dados | Contratos celebrados | Anúncios de concursos |
| Limites financeiros | Todos os contratos | Acima dos limiares comunitários |
| URL | base.gov.pt | ted.europa.eu |

## Próximo passo

Vê o [Script Principal →](./main)
