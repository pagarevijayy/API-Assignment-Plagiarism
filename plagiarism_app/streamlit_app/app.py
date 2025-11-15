# streamlit_app.py
import streamlit as st
import requests

st.set_page_config(page_title="Plagiarism Checker", layout="wide")
st.title("📄 Plagiarism Checker")
st.markdown("Upload original and submitted text files to check for plagiarism.")

original_file = st.file_uploader("Upload Original File", type=["txt"])
submission_file = st.file_uploader("Upload Submission File", type=["txt"])

if st.button("Check Plagiarism") and original_file and submission_file:
    with st.spinner("Checking..."):
        files = {
            "original": (original_file.name or "original.txt", original_file.getvalue(), "text/plain"),
            "submission": (submission_file.name or "submission.txt", submission_file.getvalue(), "text/plain")
        }
        try:
            resp = requests.post("http://127.0.0.1:5000/check", files=files, timeout=10)
            # Debugging info (helpful if something is off)
            st.write(f"HTTP {resp.status_code}")
            if resp.status_code != 200:
                st.error("Error from Flask API")
                st.code(resp.text)
            else:
                data = resp.json()
                st.metric("Similarity Score", f"{data['similarity_score'] * 100:.2f}%")
                st.metric("Plagiarism Probability", f"{data['probability'] * 100:.2f}%")
                st.success("Plagiarism Detected" if data["plagiarized"] else "No Plagiarism Detected")

                st.markdown("### 🔍 Highlighted Matches in Original")
                st.markdown(data["highlighted_original"], unsafe_allow_html=True)

                st.markdown("### 🔍 Highlighted Matches in Submission")
                st.markdown(data["highlighted_submission"], unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Connection failed: {e}")
