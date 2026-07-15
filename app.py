import streamlit as st
import google.generativeai as genai
from PIL import Image

# Secrets에서 키를 가져옵니다.
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

st.title("🎓 AI 스마트 롱노트 프로")
uploaded_file = st.file_uploader("사진을 올리세요", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=500)
    
    if st.button("분석 실행"):
        try:
            st.write("모델 호출 중...")
            # 모델 이름을 직접 넣지 않고, 사용 가능한 모델 중 flash 모델을 찾아 생성합니다.
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(["이 문제를 풀고 상세히 해설해줘.", image])
            st.write("### AI 분석 결과")
            st.write(response.text)
        except Exception as e:
            # 에러 발생 시, 현재 API 키에서 사용 가능한 모델 목록을 출력하게 합니다.
            st.error(f"오류가 발생했습니다: {e}")
            st.write("---")
            st.write("### 현재 사용 가능한 모델 목록:")
            for m in genai.list_models():
                st.write(f"- {m.name}")
