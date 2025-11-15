import streamlit as st
import joblib
from utils import calculate_cosine_similarity
from utils import highlight_matching_text

# Load model
model = joblib.load("plagiarism_model.pkl")

st.title("📄 Plagiarism Checker")

# File upload
file1 = st.file_uploader("Upload Original File", type=["txt"])
file2 = st.file_uploader("Upload Submission File", type=["txt"])

if file1 and file2:
    text1 = file1.read().decode("utf-8")
    text2 = file2.read().decode("utf-8")
    
    similarity = calculate_cosine_similarity(text1, text2)
    prediction = model.predict([[similarity]])[0]
    prob = model.predict_proba([[similarity]])[0][1]

    st.markdown(f"**Cosine Similarity Score:** `{similarity:.2f}`")
    st.markdown(f"**Plagiarism Probability:** `{prob:.2f}`")
    
    if prediction == 1:
        st.error("🔴 This submission is likely plagiarized.")
    else:
        st.success("🟢 This submission seems original.")
    
    # Highlighted Text Display
    st.subheader("📌 Highlighted Matching Text")
    highlighted1, highlighted2 = highlight_matching_text(text1, text2)

    st.markdown("**Original File (Highlighted):**", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#f9f9f9;padding:10px;border-radius:8px'>{highlighted1}</div>", unsafe_allow_html=True)

    st.markdown("**Submission File (Highlighted):**", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#f0f0f0;padding:10px;border-radius:8px'>{highlighted2}</div>", unsafe_allow_html=True)
