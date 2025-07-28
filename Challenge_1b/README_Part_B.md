# Adobe India Hackathon 2025 – Round 1B
## 🧠 Persona-Driven Document Intelligence

---

## 📌 Overview

This project demonstrates how to extract and analyze contextually important sections from a collection of documents, tailored to a specific user **persona** and **job to be done**.

Using embeddings and similarity search (via `sentence-transformers`), the system ranks and refines relevant PDF content, producing a structured JSON output per collection.

---

## 🔍 Problem Statement

> **Given:** A collection of PDFs  
> **Goal:** Identify the most relevant content based on the **persona** and their **intent** (job to be done).

Each collection has:
- A different **persona** (e.g., Travel Blogger, Product Trainer, Home Cook)
- A unique **job to be done** (e.g., extract travel tips, summarize features, extract recipes)

---

## 🧰 Tech Stack

| Component               | Tool/Library                    |
|------------------------|---------------------------------|
| Embeddings             | SentenceTransformers (MiniLM)   |
| PDF Parsing            | PyMuPDF (`fitz`)                |
| Ranking                | Cosine Similarity (SBERT)       |
| Output Format          | JSON                            |
| Language               | Python 3                        |

---

## 🗂️ Project Structure

```
.
├── Collection 1/
│   └── PDFs/
├── Collection 2/
│   └── PDFs/
├── Collection 3/
│   └── PDFs/
├── output/
│   └── collection_1_output.json
│   └── collection_2_output.json
│   └── collection_3_output.json
├── analyze_all_collections.py
└── README.md
```

---

## 🧪 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`** (for your convenience):

```txt
sentence-transformers
pymupdf
```

---

### 2. Add Your PDF Files

Place your PDFs inside the respective folders:
- `Collection 1/PDFs`
- `Collection 2/PDFs`
- `Collection 3/PDFs`

---

### 3. Run the Script

```bash
python analyze_all_collections.py
```

This will:
- Read all PDFs
- Tokenize and encode content
- Rank sections based on persona-job relevance
- Output structured results to `output/` as JSON

---

## 📤 Output Format

Each output JSON includes:

- `metadata`: input files, persona, job, timestamp
- `extracted_sections`: top 5 important sections (title, score, page)
- `sub_section_analysis`: actual refined content of the above sections

Sample:
```json
{
  "metadata": {
    "persona": "Travel Blogger",
    "job_to_be_done": "Summarize the best travel tips...",
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "timestamp": "2025-07-28T12:45:00Z"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Top 10 tips for the French Riviera...",
      "importance_score": 0.87,
      "page_number": 4
    }
  ],
  "sub_section_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "If you're visiting Nice in summer...",
      "page_number": 4
    }
  ]
}
```

---

## 🧠 Customization

You can easily add more collections or tweak the persona/job definitions inside the `COLLECTIONS` dictionary in `analyze_all_collections.py`.

---

## ✅ Status

- ✅ Completed full pipeline for multi-document and multi-persona document intelligence
- ✅ Outputs context-rich summaries aligned with user personas

---

## 🏁 Team

- **Participant:** [Your Name]
- **Hackathon:** Adobe India Hackathon 2025 – Round 1B