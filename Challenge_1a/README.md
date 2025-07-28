
# Adobe Hackathon 2025 - Round 1A & 1B

## 📦 Structure Extractor (Round 1A)

Extracts structured outline (title, H1, H2, H3 headings) from input PDFs.

### ✅ How to Build
```bash
docker build --platform linux/amd64 -t adobe-outline:submission .
```

### ▶️ How to Run
```bash
docker run --rm -v $(pwd)/app/input:/app/input -v $(pwd)/app/output:/app/output --network none adobe-outline:submission
```

Output JSON for each PDF is created in `/app/output`.

## 🧠 Round 1B (Persona-based Extraction) [TO BE ADDED]
Coming up in next file.
