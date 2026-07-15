import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from pdf2image import convert_from_bytes

# 1. API 키 설정
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

def get_model(model_name):
    return genai.GenerativeModel(model_name=model_name)

st.title("🎓 AI 스마트 롱노트 프로")

uploaded_file = st.file_uploader("문제 사진이나 PDF를 올리세요", type=["jpg", "png", "jpeg", "pdf"])

if uploaded_file is not None:
    model_name = "gemini-1.5-flash"
    model = get_model(model_name)

    # 이미지 파일 처리
    if uploaded_file.type.startswith('image'):
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드한 문제", use_column_width=True)
        if st.button("이미지 분석 시작"):
            with st.spinner("분석 중..."):
                response = model.generate_content(["이 문제를 풀고 상세히 해설해줘.", image])
                st.write(response.text)

    # PDF 파일 처리
    elif uploaded_file.type == 'application/pdf':
        st.info("PDF 파일이 감지되었습니다.")
        if st.button("PDF 분석 시작"):
            with st.spinner("PDF를 이미지로 변환하여 분석 중입니다..."):
                try:
                    # PDF를 이미지로 변환 (첫 페이지 기준)
                    images = convert_from_bytes(uploaded_file.read())
                    if images:
                        st.image(images[0], caption="PDF 첫 페이지", use_column_width=True)
                        response = model.generate_content(["이 문제지 내용을 분석하고 문제를 풀어줘.", images[0]])
                        st.subheader("AI 분석 결과")
                        st.write(response.text)
                    else:
                        st.error("PDF에서 이미지를 추출할 수 없습니다.")
                except Exception as e:
                    st.error(f"오류 발생: {e}")
