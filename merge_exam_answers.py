from pdf2image import convert_from_path
import pytesseract
import re, json, os

# --- Step 1: OCR extract answers from the PDF ---
pdf_path = "data_exams/raw_pdfs/A20 - Jour 1 - O - Réponses.pdf"
answers_txt = "data_exams/text/A20_Jour1_answers.txt"
questions_json = "data_exams/json/A20_Jour1_questions.json"
output_path = "data_exams/json/A20_Jour1_merged.json"

os.makedirs(os.path.dirname(answers_txt), exist_ok=True)

print("🔍 Running OCR on answers PDF...")
images = convert_from_path(pdf_path)
text = ""
for img in images:
    text += pytesseract.image_to_string(img, lang="eng") + "\n"

# Save OCR output so you can review/edit it if needed
with open(answers_txt, "w", encoding="utf-8") as f:
    f.write(text)
print(f"✅ OCR text saved to {answers_txt}")

# --- Step 2: Extract answers from the OCR text ---
pattern = re.compile(
    r"QUESTION\s+(\d+)\s+([a-g](?:\)|\s*[,et]+\s*[a-g]\))*\)?)",
    re.IGNORECASE
)

answers = {}
for num, letters in pattern.findall(text):
    letters_clean = re.findall(r"[a-g]", letters, re.IGNORECASE)
    answers[num] = [l.upper() for l in letters_clean]

print(f"✅ Found {len(answers)} answers")

# --- Step 3: Merge answers into question data ---
with open(questions_json, "r", encoding="utf-8") as f:
    questions = json.load(f)

missing = []
for q in questions:
    num = q["number"]
    q["answer"] = answers.get(num, None)
    if q["answer"] is None:
        missing.append(num)

# --- Step 4: Save merged output ---
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"✅ Merged data saved to {output_path}")
if missing:
    print(f"⚠️ Missing answers for questions: {', '.join(missing)}")
else:
    print("🎉 All answers matched successfully!")
