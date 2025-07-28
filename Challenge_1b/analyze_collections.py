import os
import json
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util
from datetime import datetime
import re

# === USER CONFIG ===
COLLECTIONS = {
    "Collection 1": {
        "path": "Collection 1/PDFs",
        "persona": "Travel Blogger",
        "job": "Summarize the best travel tips and insights for South of France"
    },
    "Collection 2": {
        "path": "Collection 2/PDFs",
        "persona": "Product Trainer",
        "job": "Create a short summary of key features and tools available in Adobe Acrobat"
    },
    "Collection 3": {
        "path": "Collection 3/PDFs",
        "persona": "Home Cook",
        "job": "Extract easy-to-follow and unique recipes for breakfast and dinner"
    }
}
OUTPUT_DIR = "output"

# === MODEL SETUP ===
model = SentenceTransformer('all-MiniLM-L6-v2')

def simple_sent_tokenize(text):
    return [s.strip() for s in re.split(r'(?<=[.?!])\s+', text) if len(s.strip()) > 30]

def extract_sections_from_pdf(filepath):
    doc = fitz.open(filepath)
    sections = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        for para in simple_sent_tokenize(text):
            sections.append({
                "text": para.strip(),
                "page": page_num + 1
            })
    return sections

def rank_sections(sections, query_embedding):
    texts = [s["text"] for s in sections]
    embeddings = model.encode(texts, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embeddings)[0]

    ranked = sorted(zip(sections, scores), key=lambda x: x[1], reverse=True)
    return [
        {
            "document": s.get("document"),
            "page_number": s.get("page"),
            "section_title": s.get("text")[:50] + "...",
            "importance_score": float(score)
        } for s, score in ranked[:5]
    ], [
        {
            "document": s.get("document"),
            "refined_text": s.get("text"),
            "page_number": s.get("page")
        } for s, score in ranked[:5]
    ]

def process_collection(collection_name, path, persona, job):
    print(f" Processing {collection_name}...")
    metadata = {
        "input_documents": [],
        "persona": persona,
        "job_to_be_done": job,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    combined_prompt = f"{persona}. Task: {job}"
    query_embedding = model.encode(combined_prompt, convert_to_tensor=True)

    all_ranked = []
    all_subsections = []

    for filename in os.listdir(path):
        if filename.endswith(".pdf"):
            full_path = os.path.join(path, filename)
            metadata["input_documents"].append(filename)
            sections = extract_sections_from_pdf(full_path)
            for s in sections:
                s["document"] = filename
            ranked_sections, subsections = rank_sections(sections, query_embedding)
            all_ranked.extend(ranked_sections)
            all_subsections.extend(subsections)

    output_json = {
        "metadata": metadata,
        "extracted_sections": all_ranked,
        "sub_section_analysis": all_subsections
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{collection_name.lower().replace(' ', '_')}_output.json")
    with open(out_path, "w", encoding='utf-8') as f:
        json.dump(output_json, f, indent=2)

    print(f"{collection_name} output saved to: {out_path}")

if __name__ == "__main__":
    for cname, config in COLLECTIONS.items():
        process_collection(cname, config["path"], config["persona"], config["job"])
