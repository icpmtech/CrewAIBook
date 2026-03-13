"""
AI Investor – Utilitário de Exportação para PDF
"""

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
    pdf.set_auto_page_break(auto=True, margin=15)

    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            # Títulos
            if line.startswith("# "):
                pdf.set_font("Arial", "B", size=16)
                text = line[2:].strip()
            elif line.startswith("## "):
                pdf.set_font("Arial", "B", size=13)
                text = line[3:].strip()
            elif line.startswith("### "):
                pdf.set_font("Arial", "B", size=11)
                text = line[4:].strip()
            else:
                pdf.set_font("Arial", size=10)
                text = line.strip()

            # Encode para latin-1 (compatibilidade FPDF)
            safe_text = text.encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 7, safe_text)

    pdf.output(pdf_path)
