from fastapi import FastAPI, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from src.loaders import load_documents
from src.text_splitter import chunk_documents
from src.embeddings import create_vectorstore
from src.rag_chain import create_rag_chain
from src.chat_handler import handle_chat
import os
from typing import List
os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "MyFastAPIApp/1.0")

app=FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
vectorstore=None
chain=None


@app.get("/")
async def welcome():
    return FileResponse("static/index.html", media_type="text/html")

@app.post("/upload")
async def upload_docs(files: List[UploadFile] = File(...)):
    print("Upload request received")
    print(f"Files received: {len(files) if files else 0}")
    try:
        global vectorstore, chain
        paths = []
        for file in files:
            print(f"Processing file: {file.filename}")
            contents = await file.read()
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as f:
                f.write(contents)
            paths.append(temp_path)
        docs = load_documents(paths)
        chunks=chunk_documents(docs)
        vectorstore = create_vectorstore(chunks)
        chain=create_rag_chain(vectorstore)
        return {"message":"Documents processed and stored!"}
    except Exception as e:
        print(f"Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Upload failed: {str(e)}"}

@app.post("/chat")
async def chat(query: str = Form(...)):
    if not chain:
        return {"error":"No documents uploaded yet!"}
    answer=handle_chat(query,chain)
    return {"response":answer}
