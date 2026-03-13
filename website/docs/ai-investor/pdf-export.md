---
id: pdf-export
title: Exportação para PDF
sidebar_position: 6
---

# Exportação para PDF

Após o crew gerar o relatório em Markdown, podes convertê-lo automaticamente para PDF usando a biblioteca `fpdf2`.

## Função de exportação

```python
from fpdf import FPDF

def exportar_para_pdf(md_path: str, pdf_path: str) -> None:
    """
    Converte um ficheiro Markdown para PDF.

    Args:
        md_path: Caminho para o ficheiro Markdown de entrada.
        pdf_path: Caminho para o ficheiro PDF de saída.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            # Remove caracteres que o FPDF não suporta
            clean_line = line.encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 8, clean_line)

    pdf.output(pdf_path)
```

## Como integrar no `main.py`

Adiciona ao final do `main.py`, após o `crew.kickoff()`:

```python
from pdf_utils import exportar_para_pdf

if __name__ == "__main__":
    crew.kickoff(inputs={"ticker": "NVDA"})

    # Converter relatório para PDF
    exportar_para_pdf(
        md_path="output/relatorio_investimento.md",
        pdf_path="output/relatorio_investimento.pdf",
    )
    print("✅ Relatório PDF gerado em output/relatorio_investimento.pdf")
```

## Output esperado

```
output/
├── relatorio_investimento.md
└── relatorio_investimento.pdf
```

## Alternativas mais avançadas

Para melhor suporte a Markdown (headers, bold, listas):

| Biblioteca | Vantagem |
|---|---|
| `fpdf2` | Simples, sem dependências externas |
| `weasyprint` | Converte HTML/CSS para PDF (melhor qualidade) |
| `reportlab` | Muito configurável, ideal para relatórios complexos |
| `pandoc` (CLI) | Conversão universal de formatos |

## Próximo passo

Aprende a [Executar o projecto →](./running)
