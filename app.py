import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# 1. API 키 설정
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

st.set_page_config(layout="wide")
st.title("🎓 AI 스마트 롱노트 프로")

# PDF를 제거하고 이미지 전용 업로더로 변경
uploaded_file = st.file_uploader("문제 사진(JPG, PNG)을 올려주세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 문제", use_column_width=True)
    
    if st.button("분석 시작"):
        with st.spinner("AI가 문제를 분석 중입니다..."):
            try:
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content(["이 문제를 풀고 해설해줘.", image])
                st.write(response.text)
            except Exception as e:
                st.error(f"오류: {e}")

st.warning("⚠️ PDF 파일은 분석할 수 없습니다. 캡처 도구(Win+Shift+S)로 문제를 캡처해서 올려주세요.")
