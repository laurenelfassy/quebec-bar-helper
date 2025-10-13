import os
from docx import Document
from PyPDF2 import PdfReader

# --- Settings ---
source_folder = "raw_materials"   # root folder with all your topic folders
output_folder = "data"            # where converted .txt files will go

os.makedirs(output_folder, exist_ok=True)

def convert_docx_to_txt(filepath, output_path):
    doc = Document(filepath)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def convert_pdf_to_txt(filepath, output_path):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

# --- Walk through all subfolders ---
for root, _, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith((".docx", ".pdf")):
            # Figure out where to save this file under data/
            relative_path = os.path.relpath(root, source_folder)
            out_dir = os.path.join(output_folder, relative_path)
            os.makedirs(out_dir, exist_ok=True)

            input_path = os.path.join(root, file)
            output_name = os.path.splitext(file)[0] + ".txt"
            output_path = os.path.join(out_dir, output_name)

            try:
                if file.lower().endswith(".docx"):
                    convert_docx_to_txt(input_path, output_path)
                    print(f"✅ Converted Word → {output_path}")
                else:
                    convert_pdf_to_txt(input_path, output_path)
                    print(f"✅ Converted PDF → {output_path}")
            except Exception as e:
                print(f"⚠️ Error converting {input_path}: {e}")
        else:
            # Ignore hidden system files like .DS_Store
            if not file.startswith("."):
                print(f"Skipping unsupported file: {file}")
