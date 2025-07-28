# import os
# import fitz  # PyMuPDF
# import re
# import json

# def is_heading(text):
#     text = text.strip()
#     if len(text) < 5 or len(text) > 120:
#         return False
#     if re.search(r"\b\d{1,2} (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[A-Z]* \d{4}\b", text.upper()):
#         return False
#     if re.match(r"^\d+\.\s+[A-Z]?[a-z]+", text) and len(text.split()) > 10:
#         return False
#     return re.match(r"^\d+(\.\d+)*\s+[A-Z]?[a-zA-Z]", text)

# def extract_outline_from_pdf(filepath):
#     doc = fitz.open(filepath)
#     outline = []

#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         blocks = page.get_text("blocks")
#         for block in blocks:
#             text = block[4].strip()
#             if is_heading(text):
#                 outline.append({
#                     "text": text,
#                     "page": page_num + 1
#                 })
#     return outline

# def process_folder(input_dir, output_dir):
#     for filename in os.listdir(input_dir):
#         if filename.endswith(".pdf"):
#             path = os.path.join(input_dir, filename)
#             outline = extract_outline_from_pdf(path)
#             out_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_outline.json")
#             with open(out_file, "w", encoding="utf-8") as f:
#                 json.dump(outline, f, indent=2, ensure_ascii=False)

# if __name__ == "__main__":
#     input_dir = "input"
#     output_dir = "output"
#     os.makedirs(output_dir, exist_ok=True)
#     process_folder(input_dir, output_dir)


import os
import json
import fitz  
import re

# Define regex patterns for heading detection
heading_patterns = {
    'H1': re.compile(r'^\d+\.\s+[A-Z][\w\s,()\-\.]+$'),
    'H2': re.compile(r'^\d+\.\d+\s+[A-Z][\w\s,()\-\.]+$')
}

# Fallback pattern to identify possible H1 by visual prominence
fallback_h1_pattern = re.compile(r'^[A-Z][A-Za-z0-9\s,()\-\.]{3,}$')

def classify_heading(text):
    if heading_patterns['H2'].match(text.strip()):
        return 'H2'
    elif heading_patterns['H1'].match(text.strip()):
        return 'H1'
    elif fallback_h1_pattern.match(text.strip()) and len(text.strip()) < 80:
        return 'H1'
    return None

def extract_outline_from_pdf(filepath):
    doc = fitz.open(filepath)
    outline = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("blocks")  # returns a list of text blocks

        for b in blocks:
            text = b[4].strip()
            if not text or len(text) > 150:
                continue
            level = classify_heading(text)
            if level:
                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num + 1
                })

    return {
        "title": os.path.splitext(os.path.basename(filepath))[0],
        "outline": outline
    }

# Save output to JSON
def save_outline_to_json(pdf_path, output_path):
    outline_data = extract_outline_from_pdf(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(outline_data, f, indent=2, ensure_ascii=False)
