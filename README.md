# AI Interview Practice Partner

## Overview

The **AI Interview Practice Partner** is a Streamlit-based conversational system that simulates real mock interviews using **Google Gemini**.  
It dynamically adjusts question difficulty, generates natural follow-up questions, handles different user behaviors, and provides end-of-interview feedback.

This system demonstrates real-world conversational AI design, prompt engineering, and agent robustness.

---

## Features

- Dynamic interview flow based on candidate answers
- Candidate level selection (Fresher / Intermediate / Experienced)
- Smart follow-up logic
- Handles confused, efficient, chatty, and edge-case users
- Natural English question generation
- End-of-interview performance evaluation
- Fully modular architecture

---

## Project Structure

```
interview_bot/
│
├── app.py
│
├── core/
│   ├── api.py
│   ├── interview.py
│   ├── prompts.py
│   └── utils.py
│
└── README.md
```

---

## Setup Instructions

### 1. Install Dependencies

```
pip install streamlit requests
```

### 2. Set Your Gemini API Key

**Windows (PowerShell)**

```
setx GEMINI_API_KEY "YOUR_KEY"
```

**macOS / Linux**

```
export GEMINI_API_KEY="YOUR_KEY"
```

### 3. Run the App

```
streamlit run app.py
```

App opens at:  
`http://localhost:8501`

---

## Architecture Notes

### Modular Design

- `app.py` handles UI
- `core/api.py` handles API communication
- `core/interview.py` manages interview logic
- `core/prompts.py` stores prompt text
- `core/utils.py` contains helper utilities

### Prompt Engineering

Prompts are written in simple English and extracted into a separate file.  
They include instructions to handle:

- Confused users
- Efficient users
- Chatty/off-topic users
- Invalid inputs

### Design Decisions

- Separation of concerns
- Adaptive interview behavior
- User-friendly language
- Safety-first model prompting

---

## Future Enhancements

- Resume-based interviewing
- Multi-language support
- Voice-based conversations
- PDF export for feedback

---

## Conclusion

A polished, modular, intelligent interview simulation system suitable for academic and practical use.
