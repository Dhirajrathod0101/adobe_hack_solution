import os
import json
from pathlib import Path
from heading_extractor import extract_outline_from_pdf

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in input_dir.glob("*.pdf"):
        try:
            result = extract_outline_from_pdf(pdf_path)
            output_path = output_dir / f"{pdf_path.stem}.json"
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)
            print(f" Processed: {pdf_path.name}")
        except Exception as e:
            print(f" Failed to process {pdf_path.name}: {e}")

if __name__ == "__main__":
    print(" Starting PDF Outline Extraction")
    process_pdfs()
    print("Done.")
