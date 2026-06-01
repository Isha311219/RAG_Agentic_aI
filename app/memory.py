
import json
import os

MEMORY_FILE = "memory/chat_memory.json"

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        cleaned = []

        for item in data:
            if isinstance(item, dict) and "role" in item and "content" in item:
                cleaned.append(item)

        return cleaned

    except:
        return []


def save_memory(memory):

    safe_memory = []

    for m in memory:
        if isinstance(m, dict):
            if "role" in m and "content" in m:
                safe_memory.append({
                    "role": str(m["role"]),
                    "content": str(m["content"])
                })

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(safe_memory, f, indent=2)
