"""
Procurement AI – Ferramentas de Contratação Pública

Ferramentas CrewAI para pesquisar anúncios de contratos públicos via:
  - TED (Tenders Electronic Daily) API da Europa
  - BASE.gov.pt API de Portugal
  - SIMAP CPV para lookup de códigos CPV
"""

import os
import httpx
from crewai.tools import tool


TED_API_BASE = "https://api.ted.europa.eu/v3"
BASE_API_BASE = "https://www.base.gov.pt/Base4"
SIMAP_CPV_API = "https://simap.ted.europa.eu/api/cpv"


@tool("ted_search_tool")
def ted_search_tool(cpv_code: str, country: str = "PT", page_size: int = 10) -> dict:
    """
    Pesquisa anúncios de contratos públicos na plataforma TED (Tenders Electronic Daily) da UE.

    Usa a API REST de TED para pesquisar notícias de contratos pelo código CPV e país.

    Args:
        cpv_code: Código CPV da categoria de contrato (ex: '72000000' para TI,
                  '45000000' para construção, '33000000' para produtos médicos).
        country:  Código ISO-3166-1 alpha-2 do país (por omissão 'PT' para Portugal).
        page_size: Número máximo de resultados a retornar (por omissão 10).

    Returns:
        Dicionário com a lista de anúncios encontrados e metadados de paginação.
    """
    query = f"cpv=={cpv_code}"
    if country:
        query += f" AND notice-country=={country}"

    params = {
        "q": query,
        "fields": "BT-21-Procedure,BT-22-Procedure,BT-24-Procedure,BT-300-Contract,"
                  "BT-727-Place,BT-14-notice,notice-id,publication-date,"
                  "estimated-value,BT-500-Organization",
        "pageSize": page_size,
        "page": 1,
    }

    try:
        response = httpx.get(
            f"{TED_API_BASE}/notices/search",
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        notices = data.get("notices", [])
        return {
            "total": data.get("total", 0),
            "page": data.get("page", 1),
            "results": [
                {
                    "id": n.get("notice-id", ""),
                    "title": n.get("BT-21-Procedure") or n.get("BT-24-Procedure", ""),
                    "description": n.get("BT-22-Procedure", ""),
                    "contract_title": n.get("BT-300-Contract", ""),
                    "publication_date": n.get("publication-date", ""),
                    "estimated_value": n.get("estimated-value", ""),
                    "place": n.get("BT-727-Place", ""),
                    "buyer": n.get("BT-500-Organization", ""),
                    "url": f"https://ted.europa.eu/en/notice/{n.get('notice-id', '')}",
                }
                for n in notices
            ],
        }
    except httpx.HTTPStatusError as e:
        return {"error": f"Erro HTTP {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}


@tool("cpv_lookup_tool")
def cpv_lookup_tool(keyword: str, lang: str = "pt") -> dict:
    """
    Pesquisa códigos CPV (Common Procurement Vocabulary) pelo SIMAP da UE.

    Permite encontrar o código CPV correto para uma categoria de produto/serviço.
    Utiliza a API SIMAP de TED Europa em https://simap.ted.europa.eu.

    Args:
        keyword: Palavra-chave em português (ou noutro idioma) para pesquisar
                 (ex: 'software', 'construção', 'consultoria').
        lang:    Código de idioma ISO 639-1 (por omissão 'pt' para português).

    Returns:
        Dicionário com a lista de códigos CPV correspondentes.
    """
    params = {
        "keyword": keyword,
        "lang": lang,
    }

    try:
        response = httpx.get(
            f"{SIMAP_CPV_API}/search",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "keyword": keyword,
            "results": [
                {
                    "code": item.get("code", ""),
                    "description": item.get("description", ""),
                    "parent": item.get("parent", ""),
                }
                for item in data.get("cpvs", data if isinstance(data, list) else [])
            ],
        }
    except httpx.HTTPStatusError as e:
        return {"error": f"Erro HTTP {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}


@tool("base_portugal_search_tool")
def base_portugal_search_tool(keyword: str = "", cpv_code: str = "", page: int = 1) -> dict:
    """
    Pesquisa contratos públicos no portal BASE de Portugal (base.gov.pt).

    O portal BASE é a plataforma oficial portuguesa de contratação pública e
    disponibiliza todos os contratos celebrados por entidades públicas em Portugal.

    Args:
        keyword:  Texto livre para pesquisar no objeto do contrato.
        cpv_code: Código CPV para filtrar por categoria (opcional).
        page:     Número de página de resultados (por omissão 1).

    Returns:
        Dicionário com lista de contratos e metadados.
    """
    params = {
        "tipo": "contratos",
        "texto": keyword,
        "cpv": cpv_code,
        "pag": page,
    }

    try:
        response = httpx.get(
            f"{BASE_API_BASE}/pt/resultados/",
            params={k: v for k, v in params.items() if v},
            headers={"Accept": "application/json"},
            timeout=15,
        )
        response.raise_for_status()

        # BASE returns HTML or JSON depending on Accept header; handle both
        try:
            data = response.json()
        except Exception:
            # Fallback: return raw URL for the agent to inspect
            return {
                "url": str(response.url),
                "note": "BASE portal retornou HTML. Acede diretamente ao URL para ver os contratos.",
                "results": [],
            }

        contracts = data.get("items", data.get("contratos", []))
        return {
            "total": data.get("total", len(contracts)),
            "page": page,
            "results": [
                {
                    "id": c.get("id", ""),
                    "object": c.get("objetoContrato", c.get("object", "")),
                    "entity": c.get("entidadeAdjudicante", c.get("authority", "")),
                    "contractor": c.get("adjudicatarios", c.get("contractor", "")),
                    "value": c.get("precoContratual", c.get("value", "")),
                    "date": c.get("dataCelebracaoContrato", c.get("date", "")),
                    "cpv": c.get("cpv", ""),
                    "url": f"https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id={c.get('id', '')}",
                }
                for c in contracts
            ],
        }
    except httpx.HTTPStatusError as e:
        return {"error": f"Erro HTTP {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}
