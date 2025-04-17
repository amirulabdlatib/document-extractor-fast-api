from fastapi import FastAPI
from etl_pipeline.extract import extract_text
from etl_pipeline.transform import transform_text
from etl_pipeline.load import load_files
from rag_pipeline.embedding_pipeline import embed_and_store_documents
from rag_pipeline.inference import extract_information
from pathlib import Path
import time

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

    start_time = time.time()

    for pdf_file in pdf_files:
        try:
            extracted_files = extract_text(str(pdf_file))
            
            for extracted_file in extracted_files:
                with open(extracted_file, "r", encoding="utf-8") as f:
                    extracted_text = f.read()
                
                transform_text(extracted_text, extracted_file.name)

                results.append({
                    "pdf_file": pdf_file.name,
                    "extracted_file": str(extracted_file),
                })
            

        except Exception as e:
            results.append({
                "pdf_file": pdf_file.name,
                "status": "error",
                "error": str(e)
            })

    docs = load_files()
    
    embed_and_store_documents(docs)
    
    # result_json = extract_information(docs)
    # print(result_json)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f'Time taken for whole process in seconds: {elapsed_time:.2f} seconds')
    
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"Total time taken for whole process in minutes and seconds: {int(minutes)} minutes and {seconds:.2f} seconds")

    return {
        "message": f"Processed {len(pdf_files)} PDF files",
        "results": results,
        # "inference_result": result_json,
        "status": 200
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000, log_level="info")
