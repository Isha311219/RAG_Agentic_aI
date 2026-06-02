from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil

# =====================================
# IMPORTS
# =====================================

from app.intent_classifier import classify_intent
from app.rag import retrieve_context
from app.ollama_service import generate_answer

from app.memory import load_memory, save_memory
from app.summarizer import summarize_chat

from app.vision import analyze_image
from app.audio import transcribe_audio
from app.ocr import extract_text

# =====================================
# CREATE UPLOADS FOLDER
# =====================================

os.makedirs("uploads", exist_ok=True)

# =====================================
# FASTAPI APP
# =====================================

app = FastAPI(
    title="Offline Agentic AI",
    version="9.0.0"
)

# =====================================
# CORS
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# SUMMARY MEMORY
# =====================================

summary_memory = ""

# =====================================
# HOME ROUTE
# =====================================

@app.get("/")
def home():

    return {
        "message": "Offline Agentic AI Running Successfully"
    }

# =====================================
# CHAT ROUTE
# =====================================

@app.post("/chat")
async def chat(

    question: str = Form(""),
    image: UploadFile = File(None),
    audio: UploadFile = File(None),

):

    global summary_memory

    try:

        # =====================================
        # CLEAN QUESTION
        # =====================================

        question = question.strip()

        # =====================================
        # AUTO QUESTIONS
        # =====================================

        if not question and image:
            question = "Analyze uploaded image"

        if not question and audio:
            question = "Transcribe uploaded audio"

        # =====================================
        # EMPTY CHECK
        # =====================================

        if not question and not image and not audio:

            return {
                "success": False,
                "answer": "Please ask something or upload file"
            }

        # =====================================
        # SAVE IMAGE
        # =====================================

        image_path = None

        if image and image.filename:

            image_path = f"uploads/{image.filename}"

            with open(image_path, "wb") as buffer:

                shutil.copyfileobj(
                    image.file,
                    buffer
                )

            print(f"\nImage Saved: {image_path}")

        # =====================================
        # SAVE AUDIO
        # =====================================

        audio_path = None

        if audio and audio.filename:

            audio_path = f"uploads/{audio.filename}"

            with open(audio_path, "wb") as buffer:

                shutil.copyfileobj(
                    audio.file,
                    buffer
                )

            print(f"\nAudio Saved: {audio_path}")

        # =====================================
        # LOAD MEMORY
        # =====================================

        try:

            memory = load_memory()

            if memory is None:
                memory = []

        except Exception as e:

            print("Memory Load Error:", str(e))

            memory = []

        # =====================================
        # SAVE USER QUESTION
        # =====================================

        memory.append({

            "role": "user",
            "content": question

        })

        # =====================================
        # SUMMARY MEMORY
        # =====================================

        if len(memory) >= 8:

            try:

                history_text = "\n".join([

                    f"{m['role']}: {m['content']}"

                    for m in memory
                ])

                summary_memory = summarize_chat(
                    history_text
                )

                memory = memory[-4:]

            except Exception as e:

                print("Summary Error:", str(e))

        # =====================================
        # SAVE MEMORY
        # =====================================

        try:

            save_memory(memory)

        except Exception as e:

            print("Memory Save Error:", str(e))

        # =====================================
        # INTENT
        # =====================================

        try:

            intent = classify_intent(question)

        except Exception as e:

            print("Intent Error:", str(e))

            intent = "general"

        # =====================================
        # FINAL CONTEXT
        # =====================================

        context = ""

        # =====================================
        # OCR EXTRACTION
        # =====================================

        ocr_text = ""

        if image_path:

            try:

                ocr_text = extract_text(image_path)

                print("\n========== OCR TEXT ==========\n")
                print(ocr_text)
                print("\n==============================\n")

                context += f"""

=========================
OCR TEXT
=========================

{ocr_text}

"""

            except Exception as e:

                print("OCR Error:", str(e))

        # =====================================
        # IMAGE UNDERSTANDING
        # =====================================

        image_analysis = ""

        if image_path:

            try:

                image_analysis = analyze_image(
                    image_path,
                    ocr_text
                )

                context += f"""

=========================
IMAGE UNDERSTANDING
=========================

{image_analysis}

"""

            except Exception as e:

                print("Vision Error:", str(e))

        # =====================================
        # AUDIO TRANSCRIPTION
        # =====================================

        if audio_path:

            try:

                audio_text = transcribe_audio(audio_path)

                context += f"""

=========================
AUDIO TRANSCRIPTION
=========================

{audio_text}

"""

            except Exception as e:

                print("Audio Error:", str(e))

        # =====================================
        # RAG KNOWLEDGE
        # =====================================

        try:

            rag_context = retrieve_context(question)

            if rag_context.strip():

                context += f"""

=========================
RAG KNOWLEDGE
=========================

{rag_context}

"""

        except Exception as e:

            print("RAG Error:", str(e))

        # =====================================
        # FINAL QUESTION
        # =====================================

        final_question = f"""
You are an intelligent AI assistant.

IMPORTANT:
- Answer ALL questions from uploaded image.
- If image contains multiple questions,
  answer EVERY question one by one.
- Give detailed answers.
- Correct OCR mistakes intelligently.
- Never invent fake laws.
- Never invent fake tax sections.
- If image has non-tax questions,
  answer them too.

USER QUESTION:
{question}

OCR TEXT:
{ocr_text}

IMAGE UNDERSTANDING:
{image_analysis}
"""

        # =====================================
        # DEBUG
        # =====================================

        print("\n========== FINAL QUESTION ==========\n")
        print(final_question)

        print("\n========== FINAL CONTEXT ==========\n")
        print(context)

        print("\n===================================\n")

        # =====================================
        # GENERATE ANSWER
        # =====================================

        try:

            answer = generate_answer(

                question=final_question,

                context=context,

                summary=summary_memory,

                memory=memory[-3:],

                image_path=image_path

            )

        except Exception as e:

            print("Generate Answer Error:", str(e))

            return {

                "success": False,
                "error": str(e),
                "answer": "AI generation failed"

            }

        # =====================================
        # SAVE ASSISTANT RESPONSE
        # =====================================

        memory.append({

            "role": "assistant",

            # MEMORY EXPLOSION FIX
            "content": answer[:1500]

        })

        try:

            save_memory(memory)

        except Exception as e:

            print("Memory Save Error:", str(e))

        # =====================================
        # FINAL RESPONSE
        # =====================================

        return {

            "success": True,
            "question": question,
            "intent": intent,
            "summary_memory": summary_memory,
            "context_used": bool(context),
            "image_uploaded": bool(image),
            "audio_uploaded": bool(audio),
            "answer": answer,
            "memory_size": len(memory)

        }

    except Exception as e:

        print("\nBACKEND ERROR:", str(e))

        return {

            "success": False,
            "error": str(e),
            "answer": "Backend failed"

        }
