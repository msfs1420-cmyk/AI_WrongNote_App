import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# API 키 설정
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.title("🎓 AI 스마트 롱노트 프로")
uploaded_file = st.file_uploader("사진을 올리세요", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=500) # 경고가 뜨던 use_column_width 대신 width 사용
    
    if st.button("분석 실행"):
        try:
            # 모델 호출 전 확인
            st.write("모델 호출 중...")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(["이 문제를 풀어줘", image])
            st.write("결과:", response.text)
        except Exception as e:
            # 에러가 나면 화면에 바로 출력
            st.error(f"상세 에러 내용: {str(e)}")
            print(f"DEBUG_ERROR: {e}") # 로그창에도 출력
