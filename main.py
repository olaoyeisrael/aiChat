from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.whisper import transcribe_audio
from services.parser import extract_pdf_text
from services.chunker import chunk_text
from services.embedder import embed_chunks, embed_query
from services.vector_store import store_chunks, search_chunks
from services.qa import answer_question
from services.vector_store import print_all_chunks
from services.parser import extract_ppt_text
import os
import shutil
from typing import Dict, List


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
    file: UploadFile = File(...)
):
    # Save file
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Detect file type via MIME or extension
    content_type = file.content_type  # e.g ., "application/pdf" or "audio/mpeg"
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

chat_sessions: Dict[str, List[Dict]] = {}


import html

def clean_response_text(text: str) -> str:
    text = text.replace("\\n", "\n").replace('\\"', '"')  # fix escaped newlines and quotes
    return html.unescape(text)

# @app.post("/api/ask")
# async def ask_question(
#     question: AskInput ,
#     user: UserOutput = Depends(get_current_user)):
#     if user.role != "student":  f
#         return {
#             "msg": 'kindly login'
#         }
#     # query_type = classify_query_type(question.question)
#     user_id = str(user.id)
#     # chat_sessions[user_id] = []
#     if user_id not in chat_sessions:
#         chat_sessions[user_id] = [
#             {"role": "system", "content":"You are an academic assistant."}
#          ]
#     # if query_type == "ch":
#     #     chat_sessions[user_id].append({
#     #         "role": "system",
#     #         "content": (
#     #             "The user seems to be engaging in small talk. "
#     #             "Respond in a friendly, casual way. Keep it light and polite."
#     #         )
#     #     })

#         # 
#     top_chunks = search_chunks(question.question,3, 0.75)

#     context = "\n\n".join([chunk['text'] for chunk in top_chunks])
#     answer, updated_history = answer_question(question.question, context, chat_sessions[user_id])
#     clean_response = clean_response_text(answer)
#     chat_sessions[user_id] = updated_history
#     # chat_sessions[user_id].append({ "role": "user", "content": question })
#     # chat_sessions[user_id].append({ "role": "assistant", "content": answer })
#     print(context)
#     # print(chat_sessions)

#     return {"question": question, "answer": clean_response, "search": context}


@app.post("/api/ask")
async def ask_question(
    question: AskInput):
    user_id = "guest_user" 
    if user_id not in chat_sessions:
        chat_sessions[user_id] = [
            {"role": "system", "content":"You are an academic assistant."}
         ]
    top_chunks = search_chunks(question.question,3, 0.75)

    context = "\n\n".join([chunk['text'] for chunk in top_chunks])
    answer, updated_history = answer_question(question.question, context, chat_sessions[user_id])
    clean_response = clean_response_text(answer)
    chat_sessions[user_id] = updated_history
    print(context)
    return {"question": question, "answer": clean_response, "search": context}



@app.get("/api/debug/chunks")
def debug_chunks():
    print_all_chunks()
    return {"status": "Printed chunks to console"}


@app.get("/")
def root():
    return {"message": "AI Tutor Backend Ready"}