import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# API 키 설정
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

st.title("🎓 AI 스마트 롱노트 프로")

# 파일 업로드 (이미지 전용)
uploaded_file = st.file_uploader("문제 사진(JPG, PNG)을 올려주세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 문제", use_column_width=True)
    
    # 버튼 없이 바로 분석
    try:
        with st.spinner("분석 중..."):
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(["이 문제를 풀고 해설해줘.", image])
            st.write(response.text)
    except Exception as e:
        st.error(f"오류: {e}")
