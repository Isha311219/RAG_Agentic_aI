
from app.ollama_service import generate_response
from app.intent_classifier import classify_intent
from app.memory import save_chat


async def process_query(user_message: str):

    intent = classify_intent(user_message)

    prompt = f"""
You are an AI Consultation Assistant.

User Question:
{user_message}

Intent:
{intent}

Give short helpful answer.
"""

    answer = generate_response(prompt)

    save_chat(user_message, answer)

    return {
        "intent": intent,
        "answer": answer
    }