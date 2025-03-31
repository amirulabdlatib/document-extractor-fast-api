from fastapi import FastAPI
from etl_pipeline.extract import extract_text
from etl_pipeline.transform import transform_text
from pathlib import Path

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/process-pdf")
async def process_pdf():
    input_dir = Path("input_files")
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        return {"message": "No PDF files found in the input_files directory"}
    
    results = []
    for pdf_file in pdf_files:
        try:
            extracted_files = extract_text(str(pdf_file))
            
            for extracted_file in extracted_files:
                with open(extracted_file, "r", encoding="utf-8") as f:
                    extracted_text = f.read()
                
                transformed_text, transformed_file = transform_text(extracted_text, extracted_file.name)
                
                results.append({
                    "pdf_file": pdf_file.name,
                    "extracted_file": str(extracted_file),
                    "transformed_file": str(transformed_file),
                    "status": "success"
                })
        except Exception as e:
            results.append({
                "pdf_file": pdf_file.name,
                "status": "error",
                "error": str(e)
            })
    
    return {
        "message": f"Processed {len(pdf_files)} PDF files",
        "results": results
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000, log_level="info")
