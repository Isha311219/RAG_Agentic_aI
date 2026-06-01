import ollama

TEXT_MODEL = "llama3.2:latest"


def summarize_chat(history_text):

    try:

        # =====================================
        # EMPTY CHECK
        # =====================================

        if not history_text:
            return ""

        # =====================================
        # SUMMARY PROMPT
        # =====================================

        prompt = f"""
You are a conversation memory summarizer.

Your job:
- summarize previous conversation
- keep only important information
- remove repetition
- keep useful user preferences
- keep important tax/legal/coding discussions
- keep important uploaded file discussions
- keep important AI project discussions

RULES:
- maximum 10 short bullet points
- clean readable summary
- no unnecessary explanation
- no hallucinations
- no fake facts
- keep latest context priority

CHAT HISTORY:
{history_text}

OUTPUT FORMAT:

- point 1
- point 2
- point 3
"""

        # =====================================
        # OLLAMA CALL
        # =====================================

        response = ollama.chat(

            model=TEXT_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            options={
                "temperature": 0.1
            }

        )

        # =====================================
        # CLEAN OUTPUT
        # =====================================

        answer = response["message"]["content"]

        if not answer:
            return ""

        return answer.strip()

    except Exception as e:

        print("SUMMARY ERROR:", str(e))

        return ""