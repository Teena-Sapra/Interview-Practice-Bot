import streamlit as st
from core.api import get_api_key
from core.interview import (
    generate_initial_question,
    generate_next_question,
    generate_feedback,
)

def initialize_state():
    if "interview_state" not in st.session_state:
        st.session_state.interview_state = "setup"
        st.session_state.role = ""
        st.session_state.level = "Fresher"
        st.session_state.chat_history = []
        st.session_state.user_input = ""
        st.session_state.feedback = ""

def start_interview():
    if not st.session_state.role:
        st.error("Please enter a job role to begin.")
        return

    if not get_api_key():
        st.error("API Key is missing. Set GEMINI_API_KEY environment variable and refresh.")
        return

    st.session_state.chat_history = []
    st.session_state.interview_state = "running"

    with st.spinner("Generating initial question..."):
        q = generate_initial_question(st.session_state.role, st.session_state.level)
        first_msg = f"Welcome to your mock interview for the **{st.session_state.role}** role.\n\n**Question 1:** {q}"
        st.session_state.chat_history.append({"role": "interviewer", "content": first_msg})

def send_answer():
    user_answer = st.session_state.user_input.strip()
    if not user_answer:
        st.warning("Please type your answer before sending.")
        return

    st.session_state.chat_history.append({"role": "user", "content": user_answer})
    st.session_state.user_input = ""

    if user_answer.upper().strip() in ("END INTERVIEW", "END_INTERVIEW", "__END_INTERVIEW__"):
        end_interview()
        return

    with st.spinner("Generating follow-up question..."):
        next_q = generate_next_question(st.session_state.role, st.session_state.level, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "interviewer", "content": next_q})

def end_interview():
    st.session_state.interview_state = "feedback"
    st.session_state.chat_history.append({"role": "user", "content": "__END_INTERVIEW__"})

    with st.spinner("Generating performance evaluation..."):
        feedback_text = generate_feedback(st.session_state.role, st.session_state.chat_history)
        st.session_state.feedback = feedback_text or "The model did not return feedback. Please try again."

st.set_page_config(page_title="AI Interview Practice Partner", layout="wide", initial_sidebar_state="expanded")
initialize_state()

def main():
    st.title("🤖 AI Interview Practice Partner")
    st.markdown("Select a role and candidate level, then start a mock interview. Type **END INTERVIEW** to finish and get feedback.")

    if st.session_state.interview_state == "setup":
        st.subheader("Setup Interview")
        st.session_state.role = st.text_input("Job Role (e.g., Software Engineer)", value=st.session_state.role or "Software Engineer", key="role_input")
        st.session_state.level = st.selectbox("Candidate Level", options=["Fresher", "Intermediate", "Experienced"])
        
        if st.button("🚀 Start Interview", type="primary"):
            start_interview()

        if not get_api_key():
            st.warning("⚠️ GEMINI API Key not found. Set the GEMINI_API_KEY environment variable to run the app.")

    elif st.session_state.interview_state == "running":
        st.subheader(f"Mock Interview — Role: {st.session_state.role} | Level: {st.session_state.level}")

        chat_area = st.container()
        with chat_area:
            for msg in st.session_state.chat_history:
                if msg.get("content") == "__END_INTERVIEW__":
                    continue
                if msg.get("role") == "user":
                    with st.chat_message("user"):
                        st.markdown(msg.get("content"))
                else:
                    with st.chat_message("assistant", avatar="💼"):
                        st.markdown(msg.get("content"))

        col1, col2 = st.columns([4, 1])
        with col1:
            st.text_input("Your Answer:", key="user_input", placeholder="Type your response here...")
        with col2:
            st.button("Send Answer", on_click=send_answer, type="secondary", use_container_width=True)

        st.button("🛑 End Interview Now", on_click=end_interview, type="secondary")

    elif st.session_state.interview_state == "feedback":
        st.subheader(f"✅ Performance Evaluation for: {st.session_state.role}")
        feedback = st.session_state.get("feedback", "")

        if feedback.startswith("FATAL ERROR") or feedback.startswith("API Error") or feedback.startswith("Error:"):
            st.error(feedback)
        else:
            st.markdown(feedback)

        with st.expander("Review Full Interview Transcript"):
            for msg in st.session_state.chat_history:
                if msg.get("content") == "__END_INTERVIEW__":
                    continue
                if msg.get("role") == "user":
                    st.text_area("Candidate Answer:", value=msg.get("content"), height=140, disabled=True)
                else:
                    st.text_area("Interviewer Question:", value=msg.get("content"), height=140, disabled=True)

        if st.button("Start New Interview"):
            st.session_state.interview_state = "setup"
            st.session_state.chat_history = []
            st.session_state.feedback = ""
            st.session_state.user_input = ""

if __name__ == "__main__":
    main()
