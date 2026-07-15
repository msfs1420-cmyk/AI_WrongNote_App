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
            # 'models/'를 앞에 붙여서 정확하게 지정합니다.
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            response = model.generate_content(["이 문제를 풀고 상세히 해설해줘.", image])
            st.write("### AI 분석 결과")
            st.write(response.text)
        except Exception as e:
            st.error(f"오류 발생: {e}")
            st.write("---")
            st.write("💡 팁: 만약 또 오류가 나면 'gemini-1.5-pro'로 모델명을 바꿔보세요.")
