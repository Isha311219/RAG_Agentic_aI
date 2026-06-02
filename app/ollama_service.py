import ollama
import re

TEXT_MODEL = "llama3.2:latest"
VISION_MODEL = "llava:latest"


# =========================================
# CLEAN TEXT
# =========================================

def clean_text(text):

    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()


# =========================================
# GENERATE ANSWER
# =========================================

def generate_answer(

    question,
    context="",
    summary="",
    memory=None,
    image_path=None

):

    try:

        # =====================================
        # MEMORY TEXT
        # =====================================

        memory_text = ""

        if memory:

            memory_text = "\n".join([

                f"{m['role']}: {m['content']}"

                for m in memory[-5:]

            ])

        # =====================================
        # IMAGE MODE
        # =====================================

        if image_path:

            prompt = f"""
You are a highly accurate AI Assistant.

The uploaded image may contain:
- tax questions
- legal questions
- salary slips
- invoices
- screenshots
- forms
- notes
- general knowledge questions

YOUR JOB:

1. Read OCR carefully.
2. Detect ALL questions.
3. Answer EVERY question one by one.
4. Give DETAILED answers.
5. Use clean formatting.
6. Correct OCR mistakes intelligently.
7. NEVER invent fake laws.
8. NEVER invent fake sections.
9. NEVER invent fake invoice values.
10. If values unclear:
    say "Value unclear in image."

VERY IMPORTANT TAX FACTS:

- Education loan deduction:
  Section 80E only.

- Late ITR filing fee:
  Section 234F.

- HRA and home loan:
  BOTH can be claimed together
  if conditions are satisfied.

- Freelancers:
  Usually use ITR-3 or ITR-4.

- GST:
  Indirect tax on goods/services.

- TDS:
  Tax deducted before payment.

- Capital gains:
  Depends on asset type and holding period.

VERY IMPORTANT:
If image contains NON-tax questions,
answer them too.

FORMAT STRICTLY:

# Question 1
Answer:
Detailed answer.

# Question 2
Answer:
Detailed answer.

At the end give:

# Final Summary

- short summary of all questions answered
- important tax/legal points

SUMMARY MEMORY:
{summary}

MEMORY:
{memory_text}

CONTEXT:
{context}

USER QUESTION:
{question}
"""

            response = ollama.chat(

                model=VISION_MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image_path]
                    }
                ],

                options={
                    "temperature": 0.2
                }

            )

            answer = response["message"]["content"]

            return clean_text(answer)

        # =====================================
        # NORMAL CHAT MODE
        # =====================================

        else:

            prompt = f"""
You are a smart and accurate AI assistant.

You answer:
- tax
- legal basics
- finance
- coding
- technology
- education
- business
- consumer rights
- general knowledge

RULES:

1. Give accurate answers.
2. Do NOT hallucinate.
3. Give detailed explanations.
4. Use clean formatting.
5. Give practical examples when useful.
6. Use latest Indian tax knowledge.
7. If unsure, clearly say uncertainty.

FORMAT:

# Answer
Detailed explanation.

At the end give:

# Final Summary

- short summary
- key points

SUMMARY:
{summary}

MEMORY:
{memory_text}

CONTEXT:
{context}

QUESTION:
{question}
"""

            response = ollama.chat(

                model=TEXT_MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                options={
                    "temperature": 0.2
                }

            )

            answer = response["message"]["content"]

            return clean_text(answer)

    except Exception as e:

        print("OLLAMA ERROR:", str(e))

        return f"Generation failed: {str(e)}"
