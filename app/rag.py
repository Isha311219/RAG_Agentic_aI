
import re

STOPWORDS = {
    "what", "is", "the", "a", "an", "and", "of", "to",
    "in", "for", "on", "how", "do", "does", "did",
    "can", "could", "should", "would", "i", "you"
}


def clean_tokens(text):
    tokens = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
    return [t for t in tokens if t not in STOPWORDS]


def retrieve_context(question):

    try:
        with open("app/info.txt", "r", encoding="utf-8") as f:
            knowledge = f.read()

        q_tokens = clean_tokens(question)

        if not q_tokens:
            return ""

        scored = []

        for line in knowledge.split("\n"):

            line_tokens = set(clean_tokens(line))

            score = sum(1 for t in q_tokens if t in line_tokens)
            score = score / max(len(q_tokens), 1)

            if score >= 0.4:
                scored.append((score, line))

        scored.sort(reverse=True, key=lambda x: x[0])

        return "\n".join([l for _, l in scored[:5]])

    except Exception as e:
        print("RAG ERROR:", str(e))
        return ""  
