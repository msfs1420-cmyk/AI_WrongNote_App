import streamlit as st
import google.generativeai as genai
from PIL import Image

# Secrets에서 안전하게 키를 가져옵니다.
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
            # 'gemini-1.5-flash' 대신 가장 호환성이 높은 'gemini-pro'를 사용합니다.
            model = genai.GenerativeModel("gemini-1.5-flash-latest") 
            # 만약 이것도 404가 나면 위 코드 대신 아래 줄을 복사해서 사용해보세요:
            # model = genai.GenerativeModel("gemini-pro")
            
            response = model.generate_content(["이 문제를 풀고 상세히 해설해줘.", image])
            st.write("### AI 분석 결과")
            st.write(response.text)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.write("💡 팁: 오류가 계속되면 위의 코드에서 모델명을 'gemini-pro'로 변경해 보세요.")
