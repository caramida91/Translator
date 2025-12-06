import PyPDF2
from fpdf import FPDF

class PDFHandler:
    def extract(self, path):
        try:
            text = ""
            with open(path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except:
            return None

    def save_pdf(self, text, out_path):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, text)
            pdf.output(out_path)
            return True
        except:
            return False
