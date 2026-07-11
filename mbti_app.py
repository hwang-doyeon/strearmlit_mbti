import streamlit as st
import json
import google.generativeai as genai

# 데이터 로드
def load_data_fresh():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

st.set_page_config(page_title="진짜 AI MBTI 챗봇", layout="centered")

# 고급스러운 다크 모드 (검은색 테마) 스타일 CSS 추가
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 앱 배경색 검은색/어두운 톤 적용 */
    .stApp {
        background-color: #0b0c10 !important;
        background-image: radial-gradient(circle at 50% 50%, #171926 0%, #08090d 100%) !important;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 텍스트 컬러 조정 */
    h1, h2, h3, p, span, label {
        color: #f1f5f9 !important;
    }
    
    /* 사이드바 스타일 보정 */
    [data-testid="stSidebar"] {
        background-color: #121420 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* 구분선 컬러 */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# API 키 로드 (st.secrets 우선 사용, 없으면 사이드바 입력)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError):
    with st.sidebar:
        st.header("🔑 무료 API 설정")
        api_key = st.text_input("Google Gemini API Key를 입력하세요:", type="password")
        st.caption("카드 등록이 필요 없는 무료 제미나이 키를 넣어주세요.")

st.title("🧠 진짜 AI MBTI 빙의 챗봇")
st.write("구글 제미나이가 문맥을 이해하고 사람처럼 똑똑하게 대답합니다!")

try:
    data = load_data_fresh()
    mbti_keys = sorted(list(data.keys()))
except Exception as e:
    st.error("데이터를 불러올 수 없습니다.")
    mbti_keys = []

if mbti_keys:
    selected = st.selectbox("대화할 MBTI 친구를 고르세요:", mbti_keys)
    info = data[selected]
    
    best_mbti = info.get('best', '알 수 없음')
    best_desc = data.get(best_mbti, {}).get('desc', '나와 잘 맞는')

    # 제미나이에게 줄 페르소나 (역할 설정)
    system_prompt = f"""
    너는 지금부터 '{selected}' 유형의 사람이야. AI가 아니라 실제 사람처럼 친근하게 대화해.
    
    [너의 설정]
    - 성격 특징: {info['desc']}
    - 좋아하는 유형: {best_desc} 같은 성격의 {best_mbti}
    - 좋아하는 장소: {info['place']}
    - 좋아하는 칭찬: "{info.get('cheer_up', '')}"
    - 싫어하는 행동: {info.get('dont_do', '')}
    
    [규칙]
    - 말투: '{info.get('tone', '')}'를 무조건 유지해.
    - 친근하게 반말을 쓰고 이모티콘을 자연스럽게 써.
    - 사용자의 말에 문맥을 파악해서 다양하고 자연스럽게 대답해. "아하 그렇구나" 같은 기계적인 대답은 절대 하지 마.
    """

    if "current_mbti" not in st.session_state or st.session_state.current_mbti != selected:
        st.session_state.current_mbti = selected
        st.session_state.messages = [{"role": "assistant", "content": f"안녕! 난 {selected}야. 나에 대해 궁금한 거 있어? 😉"}]

    st.markdown("---")

    # 기존 대화 출력
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input(f"{selected}에게 메시지 보내기...")

    if user_input:
        if not api_key:
            st.warning("👈 왼쪽 사이드바에 복사해둔 Gemini API Key를 먼저 붙여넣어 주세요!")
        else:
            # 사용자 메시지 저장 및 출력
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            try:
                # 제미나이 API 설정
                genai.configure(api_key=api_key)
                
                # 모델 및 시스템 프롬프트(페르소나) 적용
                model = genai.GenerativeModel('gemini-3.5-flash', system_instruction=system_prompt)
                
                # 이전 대화 기록을 제미나이 형식에 맞게 변환하여 전달
                history = []
                for msg in st.session_state.messages[:-1]: 
                    role = "model" if msg["role"] == "assistant" else "user"
                    history.append({"role": role, "parts": [msg["content"]]})
                    
                chat = model.start_chat(history=history)
                
                # 제미나이 응답 생성
                with st.chat_message("assistant"):
                    response = chat.send_message(user_input)
                    ai_reply = response.text
                    st.markdown(ai_reply)
                    
                # 응답 저장
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}")
