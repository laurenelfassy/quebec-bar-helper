import os
import re
import json
from pdf2image import convert_from_path
import pytesseract
from tqdm import tqdm  # for nice progress bars

# --- CONFIG ---
RAW_DIR = "data_exams/raw_pdfs"
TEXT_DIR = "data_exams/text"
JSON_DIR = "data_exams/json"

os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# --- FUNCTIONS ---

def pdf_to_text(pdf_path, output_txt):
    """Convert PDF to plain text using OCR."""
    text = ""
    images = convert_from_path(pdf_path)
    for img in images:
        text += pytesseract.image_to_string(img, lang="fra") + "\n"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)
    return output_txt


def extract_questions(text):
    """Extract questions and choices from the question text."""
    questions = []
    pattern = re.compile(r"QUESTION\s+(\d+)(.*?)(?=QUESTION\s+\d+|$)", re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(text)

    for num, content in matches:
        context = content.strip().replace("\n", " ")
        choices = re.findall(r"[a-e]\)", content)
        questions.append({
            "number": num.strip(),
            "context": context[:300],  # keep summary short
            "choices": choices,
        })
    return questions


def extract_answers(text):
    """Extract answers from corrigé text."""
    pattern = re.compile(
        r"QUEST\s*ION\s*(\d+)\s*([a-g](?:\)|\s*[,et]+\s*[a-g]\))*\)?)",
        re.IGNORECASE
    )
    answers = {}
    for num, letters in pattern.findall(text):
        letters_clean = re.findall(r"[a-g]", letters, re.IGNORECASE)
        if letters_clean:
            answers[num] = [l.upper() for l in letters_clean]
    return answers


def merge_and_save(questions, answers, out_path):
    """Merge question JSON with answers."""
    missing = []
    for q in questions:
        q["answer"] = answers.get(q["number"], None)
        if q["answer"] is None:
            missing.append(q["number"])
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    return missing


# --- MAIN LOOP ---
for file in tqdm(os.listdir(RAW_DIR)):
    if "Question" in file or "Questionnaire" in file:
        exam_name = re.sub(r"[-_\s]*Question.*\.pdf$", "", file, flags=re.IGNORECASE)
        q_pdf = os.path.join(RAW_DIR, file)
        
        # Try to automatically find the matching "answers" file
        possible_suffixes = ["- Réponses", "- Reponses", "- Corrigé", "- Corrige", "Correction", "- CORRIGÉ", "- CORRIGE", "- CORRECTION", "- RÉPONSES"]
        a_pdf = None

        for suffix in possible_suffixes:
            for ext in [".pdf", ".PDF"]:
                candidate = os.path.join(RAW_DIR, f"{exam_name} {suffix}{ext}")
                if os.path.exists(candidate):
                    a_pdf = candidate
                    break
            if a_pdf:
                break

        if not a_pdf:
            print(f"⚠️ Could not find answers file for {exam_name}")
            continue


        q_txt = os.path.join(TEXT_DIR, f"{exam_name}_questions.txt")
        a_txt = os.path.join(TEXT_DIR, f"{exam_name}_answers.txt")
        q_json = os.path.join(JSON_DIR, f"{exam_name}_merged.json")

        print(f"\n🧾 Processing {exam_name}...")

        # Convert PDFs to text
        pdf_to_text(q_pdf, q_txt)
        pdf_to_text(a_pdf, a_txt)

        # Extract data
        with open(q_txt, "r", encoding="utf-8") as f:
            q_text = f.read()
        with open(a_txt, "r", encoding="utf-8") as f:
            a_text = f.read()

        questions = extract_questions(q_text)
        answers = extract_answers(a_text)

        # Merge
        missing = merge_and_save(questions, answers, q_json)

        if missing:
            print(f"⚠️ Missing answers for: {', '.join(missing)}")
        else:
            print(f"✅ All answers matched for {exam_name}")

print("\n🎉 All exams processed.")
