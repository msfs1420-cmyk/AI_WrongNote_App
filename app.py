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
            # 모델을 직접 지정하는 대신 'gemini-1.5-flash'를 호출하는 가장 기본적인 방법입니다.
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(["이 문제를 풀어줘", image])
            
            st.write("### AI 분석 결과")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.write("---")
            st.write("💡 만약 여전히 404가 뜬다면, 아래 코드를 대신 사용해보세요:")
            st.code('model = genai.GenerativeModel("gemini-1.5-flash-001")')
