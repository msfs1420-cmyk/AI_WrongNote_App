import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# 1. API 키 설정 (보안 유지)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

# 2. UI 설정
st.set_page_config(layout="wide")
st.title("🎓 AI 스마트 롱노트 프로")

# 3. 파일 업로드 (이미지 전용)
uploaded_file = st.file_uploader("문제 사진(JPG, PNG)을 올리세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 이미지 열기
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 문제", use_column_width=True)
    
    # 4. 분석 시작 버튼
    if st.button("AI 분석 시작"):
        with st.spinner("AI가 문제를 분석 중입니다..."):
            try:
                # Gemini 모델 호출
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content(["이 문제를 풀고 상세히 해설해줘.", image])
                
                # 결과 출력
                st.subheader("AI 분석 결과")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

# 5. 안내 문구
st.info("💡 PDF 파일이 있다면, 캡처 도구로 사진을 찍어 JPG/PNG로 저장해 올리시면 가장 빠르고 정확하게 분석됩니다!")
