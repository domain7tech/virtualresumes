import os
from PyPDF2 import PdfReader

def convert_all_pdfs_to_txt():
    # Get this script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Fix: use 'resumes/resumePDF' and 'resumes/resumeTXT'
    pdf_folder = os.path.join(base_dir, "resumes", "resumePDF")
    txt_folder = os.path.join(base_dir, "resumes", "resumeTXT")

    if not os.path.exists(pdf_folder):
        print(f"Source folder does not exist: {pdf_folder}")
        return
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in {pdf_folder}")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        txt_file = os.path.splitext(pdf_file)[0] + '.txt'
        txt_path = os.path.join(txt_folder, txt_file)
        try:
            reader = PdfReader(pdf_path)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() or ""
            full_text = full_text.strip()
            with open(txt_path, "w", encoding="utf-8") as out_txt:
                out_txt.write(full_text)
            print(f"Converted: {pdf_file} → {txt_file}")
        except Exception as e:
            print(f"Error with {pdf_file}: {e}")

if __name__ == "__main__":
    convert_all_pdfs_to_txt()
