import fitz

# basically: 'Give me extracted pdf and ill return it as a properly displayed string. Also i expect pdf_bytes= UploadFile'
def extract_pdf(pdf_data):
    doc = fitz.open(stream=pdf_data, filetype=".pdf")
    
    pdf_text = ""
    for page in doc:
        pdf_text += f"\n{page.get_text()}"
        
    return pdf_text