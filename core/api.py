import os
import json
import time
import requests
from typing import List, Dict, Any

# mirrors original config
apiKey = os.environ.get("GEMINI_API_KEY", "")

MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
MAX_OUTPUT_TOKENS = 4096

def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("API_KEY") or apiKey
    return key

def safe_json_snippet(obj: Any, length: int = 500) -> str:
    try:
        return json.dumps(obj)[:length]
    except Exception:
        return str(obj)[:length]

def call_gemini_api(system_prompt: str, contents: List[Dict[str, Any]], retries: int = 3, timeout: int = 60) -> str:
    key = get_api_key()
    if not key:
        return "FATAL ERROR: API Key is missing. Please set the 'GEMINI_API_KEY' environment variable."

    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": contents if contents else [{"role": "user", "parts": [{"text": "Start."}]}],
        "generationConfig": {"maxOutputTokens": MAX_OUTPUT_TOKENS}
    }

    headers = {"Content-Type": "application/json"}

    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(API_URL, params={"key": key}, headers=headers, data=json.dumps(payload), timeout=timeout)
        except requests.exceptions.RequestException as e:
            if attempt == retries:
                return f"Error connecting to the model after {retries} attempts: {e}"
            time.sleep(2 ** (attempt - 1))
            continue

        if resp.status_code == 400:
            return f"API Error (HTTP 400 Bad Request): {resp.text[:300]}"
        if resp.status_code == 404:
            return f"API Error (HTTP 404 Not Found): Model '{MODEL_NAME}' unavailable at endpoint."

        try:
            result = resp.json()
        except ValueError:
            return f"API Error: Non-JSON response: {resp.text[:500]}"

        try:
            candidates = result.get("candidates", [])
            if candidates:
                extracted_texts = []
                for cand in candidates:
                    content = cand.get("content", {})
                    parts = content.get("parts") or []
                    for p in parts:
                        if isinstance(p, dict) and "text" in p and p["text"]:
                            extracted_texts.append(p["text"])
                    if not parts and isinstance(content, dict) and "text" in content and content["text"]:
                        extracted_texts.append(content["text"])

                if extracted_texts:
                    return "\n\n".join(extracted_texts)

            if "outputText" in result and result["outputText"]:
                return result["outputText"]

            if isinstance(result, dict) and "text" in result and result["text"]:
                return result["text"]

            return f"Error: Could not extract content from the API response. Raw response snippet: {safe_json_snippet(result)}"

        except Exception as e:
            return f"Error extracting model output: {e}. Raw response snippet: {safe_json_snippet(result)}"

    return "API call failed after retries."
