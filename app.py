import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import tempfile

# 1. API 키 설정 (보안 강화)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

# 2. 모델 설정 함수
def get_model(model_name):
    return genai.GenerativeModel(model_name=model_name)

# 3. 사이드바 구성
st.sidebar.header("⚙️ 관리 메뉴")
save_path = st.sidebar.text_input("데이터 저장 경로", value="./my_wrong_notes")
model_option = st.sidebar.radio("AI 분석 모델 선택", ["빠른 분석 (Flash)", "정밀 분석 (Pro)"])
model_name = "gemini-1.5-flash" if "Flash" in model_option else "gemini-1.5-pro"

# 4. 메인 화면 구성
st.title("🎓 AI 스마트 롱노트 프로")

# [수정된 부분] 사진과 PDF 모두 허용
uploaded_file = st.file_uploader("문제 사진이나 PDF를 올리세요", type=["jpg", "png", "jpeg", "pdf"])

# 5. 분석 로직
if uploaded_file is not None:
    # 파일 타입 확인
    if uploaded_file.type.startswith('image'):
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드한 문제", use_column_width=True)
        
        if st.button("AI 분석 시작"):
            with st.spinner("이미지를 분석 중입니다..."):
                model = get_model(model_name)
                # 이미지 분석 프롬프트 로직을 여기에 작성하세요
                st.success("이미지 분석 완료!")
                
    elif uploaded_file.type == 'application/pdf':
        st.info("PDF 파일이 업로드되었습니다.")
        if st.button("PDF 분석 시작"):
            with st.spinner("PDF 문서를 분석 중입니다..."):
                # PDF 처리 로직은 추후 추가 가능
                st.warning("PDF 분석 기능은 현재 준비 중입니다.")

# 6. 오답 리스트 관리
if not os.path.exists(save_path):
    os.makedirs(save_path)
