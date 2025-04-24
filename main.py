from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.whisper import transcribe_audio
from services.parser import extract_pdf_text
from services.chunker import chunk_text
from services.embedder import embed_chunks, embed_query
from services.vector_store import store_chunks, search_chunks
from services.qa import answer_question, classify_query_type
from services.vector_store import print_all_chunks
from services.parser import extract_ppt_text
import os
import shutil


from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectRoute import get_current_user
from app.db.schema.admin import UserOutput

@asynccontextmanager
async def lifespan(app : FastAPI):
    # Intializes the db tables when the application starts up
    create_tables()
    yield 




app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 👈 React frontend
    allow_credentials=True,
    allow_methods=["*"],   # 👈 Allow all HTTP methods (including OPTIONS)
    allow_headers=["*"],   # 👈 Allow all headers including Authorization
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

   
@app.post("/api/upload")
async def upload_material(
    file: UploadFile = File(...),
    user: UserOutput = Depends(get_current_user)
):
    if user.role != "admin":
        # return RedirectResponse(url="http://localhost:3000/question-answer")
        return {
            "msg": 'kindly login'
        }

    # Save file
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Detect file type via MIME or extension
    content_type = file.content_type  # e.g., "application/pdf" or "audio/mpeg"
    filename = file.filename.lower()

    if "audio" in content_type or filename.endswith((".mp3", ".wav", ".mp4")):
        text = transcribe_audio(filepath)
    elif content_type == "application/pdf" or filename.endswith(".pdf"):
        text = extract_pdf_text(filepath)
    elif filename.endswith((".ppt", ".pptx")) or content_type in ["application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
        text = extract_ppt_text(filepath)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    chunks = chunk_text(text)
    store_chunks(chunks)

    return {
        "message": "Material processed and stored",
        "chunks": len(chunks),
        "text": text
    }



from pydantic import BaseModel

class AskInput(BaseModel):
    question: str

@app.post("/api/ask")
async def ask_question(
    question: AskInput ,
    user: UserOutput = Depends(get_current_user)):
    if user.role != "student":
        return {
            "msg": 'kindly login'
        }
    query_type = classify_query_type(question.question)
    if query_type == "ch":
        response = answer_question(question.question, context=None, mode="chat")
        return {"question": question.question, "answer": response, "type": query_type}
    top_chunks = search_chunks(question.question,3, 0.75)

    context = "\n\n".join([chunk['text'] for chunk in top_chunks])
    answer = answer_question(question.question, context)
    print(context)

    return {"question": question, "answer": answer, "search": context}

     
@app.get("/api/debug/chunks")
def debug_chunks():
    print_all_chunks()
    return {"status": "Printed chunks to console"}


@app.get("/")
def root():
    return {"message": "AI Tutor Backend Ready"}