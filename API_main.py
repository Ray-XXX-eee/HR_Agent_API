import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from app.utils.pydantic_model import ChatRequest
# from app.doc_processor.doc_processor import DocumentProcessor,document_processor
from app.doc_processor.new_doc_processor import document_processor
from app.main_chat.base_chat_service import base_chat_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

DATA_DIR = "data"
JD_DIR = os.path.join(DATA_DIR, "jd_files")
CV_DIR = os.path.join(DATA_DIR, "cv_files")

# Ensure directories exist
os.makedirs(JD_DIR, exist_ok=True)
os.makedirs(CV_DIR, exist_ok=True)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process_document")
async def process_document_1(file: UploadFile = File(...), file_type: str = Form(...)):
    try:
        if not file_type:
            raise HTTPException(status_code=400, detail="Missing file_type parameter")

        # Determine folder based on file_type (JD or CV)
        folder = JD_DIR if file_type == "jd" else CV_DIR
        file_path = os.path.join(folder, file.filename)

        print(f"Saving {file_type.upper()} file to: {file_path}")  # Debugging

        # Save file properly
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Process document
        document_processor.process_document(file_path)

        # return {
        #     "message": f"Document '{file.filename}' processed successfully and stored in {folder}.",
        #     "pages": pages,
        #     "final_doc": final_doc
        # }
        return {"message": "Document processed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles chat requests and generates a response."""
    return base_chat_response(request.user_prompt)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
































