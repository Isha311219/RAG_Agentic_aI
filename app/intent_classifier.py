def classify_intent(message: str):

    message = message.lower()

    if "gst" in message:
        return "tax_query"

    if "wallet" in message:
        return "wallet_issue"

    if "lawyer" in message:
        return "legal_query"

    return "general_question"