from typing import List, Dict
from .api import call_gemini_api
from .utils import transcript_text, build_contents_from_history, difficulty_descriptor
from .prompts import (
    INITIAL_PROMPT, INITIAL_USER_PROMPT,
    FOLLOWUP_PROMPT, FOLLOWUP_USER_PROMPT,
    FEEDBACK_SYSTEM_PROMPT, FEEDBACK_USER_PROMPT_TEMPLATE
)

def generate_initial_question(role: str, level: str) -> str:
    system_prompt = INITIAL_PROMPT.format(role=role, level=level)
    contents = [{"role": "user", "parts": [{"text": INITIAL_USER_PROMPT}]}]
    return call_gemini_api(system_prompt, contents)

def generate_next_question(role: str, level: str, history: List[Dict[str, str]]) -> str:
    short_history = history[-6:] if len(history) >= 6 else history
    transcript = transcript_text(short_history, max_chars=2000)

    system_prompt = FOLLOWUP_PROMPT.format(role=role, level=level)
    contents = build_contents_from_history(short_history) or [{"role": "user", "parts": [{"text": FOLLOWUP_USER_PROMPT}]}]
    return call_gemini_api(system_prompt, contents)

def generate_feedback(role: str, history: List[Dict[str, str]]) -> str:
    transcript = transcript_text(history, max_chars=6000)
    user_prompt = FEEDBACK_USER_PROMPT_TEMPLATE.format(role=role, transcript=transcript)
    contents = [{"role": "user", "parts": [{"text": user_prompt}]}]
    return call_gemini_api(FEEDBACK_SYSTEM_PROMPT, contents)
