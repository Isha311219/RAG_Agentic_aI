import ollama
import json
import re

VISION_MODEL = "llava:latest"


def clean_json_response(text):

    text = text.strip()

    # remove markdown json blocks
    text = text.replace("```json", "")
    text = text.replace("```", "")

    return text.strip()


def analyze_image(image_path, ocr_text=""):

    try:

        prompt = f"""
You are an advanced OCR + Image Understanding AI.

Your task is to analyze uploaded images carefully.

The image may contain:
- tax questions
- legal questions
- salary slips
- invoices
- forms
- handwritten notes
- screenshots
- general knowledge questions

IMPORTANT RULES:

1. Read OCR carefully.
2. Detect ALL meaningful questions.
3. Ignore OCR garbage.
4. Correct broken OCR words intelligently.
5. NEVER invent fake values.
6. NEVER invent fake laws/sections.
7. If value unclear:
   say "Value unclear"

IMPORTANT:
- If image contains only questions,
  extract ALL questions properly.
- If image contains salary slip,
  identify salary components.
- If image contains invoice,
  identify GST values if visible.
- If image contains forms,
  identify form type.

Return ONLY VALID JSON.

FORMAT:

{{
  "document_type": "questions/salary slip/invoice/form/notes/other",

  "questions": [
    "...",
    "..."
  ],

  "important_points": [
    "...",
    "..."
  ],

  "summary": "short summary"
}}

OCR TEXT:
{ocr_text}
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
                "temperature": 0.1
            }

        )

        result = response["message"]["content"]

        result = clean_json_response(result)

        # validate json
        try:
            parsed = json.loads(result)

            return json.dumps(
                parsed,
                indent=2
            )

        except:
            return result

    except Exception as e:

        print("VISION ERROR:", str(e))

        return ""