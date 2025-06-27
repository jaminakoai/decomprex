import markdown
from fpdf import FPDF
import os

def save_report(report_dict, output_dir):
    md_path = os.path.join(output_dir, "analysis_report.md")
    html_path = os.path.join(output_dir, "analysis_report.html")
    pdf_path = os.path.join(output_dir, "analysis_report.pdf")
    
    # Markdown
    md_content = f"# APK Analiz Raporu\n"
    for k, v in report_dict.items():
        md_content += f"## {k}\n{v}\n"
    with open(md_path, "w") as f:
        f.write(md_content)
    
    # HTML
    html_content = markdown.markdown(md_content)
    with open(html_path, "w") as f:
        f.write(html_content)
    
    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in md_content.split('\n'):
        pdf.cell(200, 10, txt=line, ln=1, align='L')
    pdf.output(pdf_path)
    return md_path, html_path, pdf_path
