import streamlit as st
import google.generativeai as genai
import os
import PyPDF2
from streamlit_pdf_viewer import pdf_viewer

# 1. API 키 설정
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

st.set_page_config(layout="wide")
st.title("🎓 AI 스마트 롱노트 프로")

uploaded_file = st.file_uploader("PDF 파일을 올리세요", type=["pdf"])

if uploaded_file is not None:
    # 1. PDF 뷰어로 화면에 보여주기 (서버 변환 없음)
    pdf_viewer(uploaded_file.read())
    
    if st.button("AI 텍스트 분석 시작"):
        with st.spinner("PDF에서 텍스트를 추출하여 분석 중입니다..."):
            try:
                # 2. PyPDF2로 텍스트 추출
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # 3. 모델 분석
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content(f"다음 문제 내용을 분석하고 상세히 해설해줘:\n\n{text}")
                
                st.subheader("AI 분석 결과")
                st.write(response.text)
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")

st.info("💡 텍스트 기반 분석이라 매우 빠르고 정확합니다!")
