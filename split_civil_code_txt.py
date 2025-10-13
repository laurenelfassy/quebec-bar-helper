import os
import re

input_path = "raw_materials/Civil_Code_clean.txt"
output_folder = "data/Civil_Code"
os.makedirs(output_folder, exist_ok=True)

print(" Splitting Civil Code articles (simple next-number rule)...")

with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# Clean weird spacing
text = re.sub(r"\s+", " ", text)

# Match: article number (1–4 digits, maybe .digit), then everything until next article number
pattern = r"(\d{1,4}(?:\.\d{1,2})?)\.\s(.*?)(?=\d{1,4}(?:\.\d{1,2})?\.\s|$)"

matches = re.findall(pattern, text)
print(f"✅ Found {len(matches)} raw chunks.")

for num, content in matches:
    # Filter out junk like table of contents by requiring at least one '1991,' or '2020,' etc.
    if "1991" in content or "2020" in content or "2022" in content:
        filename = os.path.join(output_folder, f"article_{num}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Article {num}\n\n{content.strip()}")

print(f"Saved {len(os.listdir(output_folder))} articles to {output_folder}")
