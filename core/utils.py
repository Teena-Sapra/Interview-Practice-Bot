from typing import List, Dict, Any

def build_contents_from_history(history: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    role_map = {"user": "user", "interviewer": "model"}
    contents = []
    for msg in history:
        if msg.get("content") == "__END_INTERVIEW__":
            continue
        role = role_map.get(msg.get("role"), "user")
        contents.append({"role": role, "parts": [{"text": msg.get("content", "")}]})
    return contents

def transcript_text(history: List[Dict[str, str]], max_chars: int = 4000) -> str:
    lines = []
    for m in history:
        if m.get("content") == "__END_INTERVIEW__":
            continue
        speaker = "Interviewer" if m.get("role") == "interviewer" else "Candidate"
        lines.append(f"{speaker}: {m.get('content')}")
    text = "\n".join(lines)
    return text if len(text) <= max_chars else text[-max_chars:]

def difficulty_descriptor(level: str) -> str:
    level = (level or "").lower()
    if level == "fresher":
        return "This is a fresher / entry-level candidate with little to no professional experience. Keep questions practical, explainable, and avoid heavy system-design or long cross-functional scenarios."
    if level == "intermediate":
        return "This is an intermediate candidate (1-4 years). Ask about real problem-solving, ownership, trade-offs, and some technical depth while keeping things focused."
    if level == "experienced":
        return "This is an experienced candidate (4+ years). Use deeper, open-ended questions, system design, leadership, architecture and cross-team trade-off discussions."
    return "No specific level guidance provided."
