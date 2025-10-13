import re

input_path = "raw_materials/Civil_Code_text.txt"
output_path = "raw_materials/Civil_Code_clean.txt"

with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove table of contents (everything before "1. Tout être humain...")
text = re.split(r"\b1\.\s+Tout être humain", text, maxsplit=1)[-1]
text = "1. Tout être humain " + text  # reattach the first article number

# 2. Remove random page numbers, © lines, and “À jour au...” references
text = re.sub(r"À jour au.*?CCQ-1991.*?\n", "", text)
text = re.sub(r"©.*?\n", "", text)
text = re.sub(r"\b\d+\s+sur\s+\d+\b", "", text)
text = re.sub(r"\s+", " ", text).strip()

with open(output_path, "w", encoding="utf-8") as f:
    f.write(text)

print("✅ Clean Civil Code text saved to", output_path)
