"""
Procurement AI – Ferramentas de Contratação Pública

Ferramentas CrewAI para pesquisar anúncios de contratos públicos via:
  - TED (Tenders Electronic Daily) API da Europa
  - BASE.gov.pt REST API de Portugal (base2/rest/contratos)
    Abordagem inspirada em https://github.com/ajcerejeira/base.gov.pt
  - SIMAP CPV para lookup de códigos CPV
"""

import httpx
from crewai.tools import tool


TED_API_BASE = "https://api.ted.europa.eu/v3"
# BASE Portugal canonical JSON REST API (used by ajcerejeira/base.gov.pt)
BASE_REST_API = "https://www.base.gov.pt/base2/rest/contratos"
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
def base_portugal_search_tool(start: int = 1, count: int = 20) -> dict:
    """
    Obtém contratos públicos do portal BASE de Portugal via API REST JSON.

    Usa o endpoint base2/rest/contratos com cabeçalho Range para paginação,
    seguindo a abordagem documentada em https://github.com/ajcerejeira/base.gov.pt.
    Retorna os campos principais de cada contrato sem necessidade de autenticação.

    Args:
        start: Índice do primeiro contrato a obter (por omissão 1).
        count: Número de contratos a obter por página (por omissão 20, máx. 100).

    Returns:
        Dicionário com a lista de contratos e os índices de paginação usados.
    """
    end = start + min(count, 100) - 1
    headers = {"Range": f"{start}-{end}"}

    try:
        response = httpx.get(
            BASE_REST_API,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()
        contracts = response.json()
        return {
            "range_start": start,
            "range_end": end,
            "count": len(contracts),
            "results": [
                {
                    "id": c.get("id", ""),
                    "object": c.get("objectContractDescription", c.get("contractObject", "")),
                    "entity": c.get("contractingAuthority", c.get("entidade", "")),
                    "contractor": c.get("awardedTo", c.get("adjudicatario", "")),
                    "value": c.get("contractPrice", c.get("preco", "")),
                    "date": c.get("signingDate", c.get("dataCelebracaoContrato", "")),
                    "cpv": c.get("cpvs", c.get("cpv", "")),
                    "url": f"https://www.base.gov.pt/base2/rest/contratos/{c.get('id', '')}",
                }
                for c in (contracts if isinstance(contracts, list) else [])
            ],
        }
    except httpx.HTTPStatusError as e:
        return {"error": f"Erro HTTP {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}


@tool("base_contract_detail_tool")
def base_contract_detail_tool(contract_id: int) -> dict:
    """
    Obtém os detalhes completos de um contrato público português pelo seu ID.

    Usa o endpoint base2/rest/contratos/{id} do portal BASE.gov.pt,
    seguindo a abordagem documentada em https://github.com/ajcerejeira/base.gov.pt.

    Args:
        contract_id: Identificador numérico único do contrato no portal BASE.

    Returns:
        Dicionário com todos os campos do contrato (objeto, entidade, adjudicatário,
        valor, datas, CPVs, concorrentes, documentos, etc.).
    """
    try:
        response = httpx.get(
            f"{BASE_REST_API}/{contract_id}",
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"Erro HTTP {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {"error": str(e)}
