import streamlit as st
import json
import google.generativeai as genai

# 데이터 로드
def load_data_fresh():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 차단할 나쁜 말/욕설 리스트 (원하시는 단어를 계속 추가하시면 됩니다!)
BAD_WORDS = ["바보", "멍청이", "짜증", "개새", "존나", "시발", "지랄", "네가지", "혐오", "새끼", "죽어", "미친놈"]

# 나쁜 말이 포함되었을 때 교체할 착한 말 리스트
GOOD_WORDS = [
    "앗, 방금 내 MBTI 성격이 너무 튀어나와서 실례할 뻔했어! 미안해 지켜봐줘 대화하자 헤헤 🥰",
    "이쁜 말 고운 말! 다시 예쁘게 대답해 줄게! 소중한 친구야 고마워 내 맘 알지? 대화하자 💖",
    "잠시 마음을 가다듬고 다시 말할게! 우리는 좋은 친구잖아 그치? 반가워 대화하자 우헤헤 🌟"
]

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
st.write("MBTI, 성별, 그리고 원하는 상황과 장소를 마음대로 설정해 대화해 보세요!")

try:
    data = load_data_fresh()
    mbti_keys = sorted(list(data.keys()))
except Exception as e:
    st.error("데이터를 불러올 수 없습니다.")
    mbti_keys = []

if mbti_keys:
    # 레이아웃 구성
    col1, col2 = st.columns(2)
    with col1:
        selected = st.selectbox("대화할 MBTI 친구를 고르세요:", mbti_keys)
    with col2:
        gender = st.radio("나의 성별을 선택하세요:", ["남자", "여자"], horizontal=True)
        
    # [추가] 2층 레이아웃: AI 얼굴(아이콘) 및 내 아이콘 선택 리스트
    icon_options = {
        "❓ 물음표": "❓",
        "👩 여자 사람": "👩",
        "👨 남자 사람": "👨",
        "🤖 로봇": "🤖",
        "🔵 동그라미": "🔵",
        "🟩 네모": "🟩",
        "🔥 불": "🔥",
        "🌳 나무": "🌳",
        "😄 웃는 사람": "😄",
        "😉 윙크하는 사람": "😉",
        "😋 맛있는 걸 먹는 사람": "😋",
        "🌈 무지개": "🌈",
        "🪨 돌": "🪨",
        "😎 멋쟁이": "😎",
        "🥰 하트 뿅뿅": "🥰",
        "👽 외계인": "👽",
        "👻 유령": "👻",
        "🐱 고양이": "🐱",
        "🐶 강아지": "🐶",
        "☁️ 구름": "☁️",
        "☀️ 맑은 하늘": "☀️",
        "🌙 달": "🌙",
        "⭐ 별": "⭐",
        "🌊 파도": "🌊",
        "❄️ 눈송이": "❄️",
        "🌸 벚꽃": "🌸",
        "🍀 네잎클로버": "🍀",
        "🍔 햄버거": "🍔",
        "🍕 피자": "🍕",
        "🍓 딸기": "🍓",
        "☕ 커피": "☕",
        "🎸 기타": "🎸",
        "🎮 게임기": "🎮",
        "🚗 자동차": "🚗",
        "✈️ 비행기": "✈️",
        "🧸 곰인형": "🧸",
        "🎈 풍선": "🎈",
        "🎁 선물": "🎁",
        "🏀 농구공": "🏀",
        "⚽ 축구공": "⚽",
        "🐧 펭귄": "🐧",
        "🦉 부엉이": "🦉",
        "🦊 여우": "🦊"
    }
    
    col3, col4, col5 = st.columns([1, 1, 2])
    with col3:
        selected_ai_icon = st.selectbox("AI의 얼굴(아이콘):", list(icon_options.keys()), index=3)
        ai_avatar = icon_options[selected_ai_icon]
        
    with col4:
        selected_user_icon = st.selectbox("나의 얼굴(아이콘):", list(icon_options.keys()), index=0)
        user_avatar = icon_options[selected_user_icon]
        
    with col5:
        situation = st.text_input(
            "장소나 분위기를 적어주세요:", 
            value="아늑한 카페", 
            placeholder="예시: 수영장, 길 한복판 등"
        )

    info = data[selected]
    
    best_mbti = info.get('best', '알 수 없음')
    best_desc = data.get(best_mbti, {}).get('desc', '나와 잘 맞는')

    # 제미나이에게 줄 페르소나 (성별 + 주관식 상황 정보 주입)
    system_prompt = f"""
    너는 지금부터 '{selected}' 유형의 사람이야. AI가 아니라 실제 사람처럼 친근하게 대화해.
    
    [현재 대화 환경 설정]
    - 대화 상대방(유저)의 성별: '{gender}' (성별에 맞는 자연스러운 호칭과 리액션 사용)
    - 대화가 이루어지는 장소/분위기: '{situation}' 
      👉 매우 중요: 너는 지금 반드시 이 장소와 분위기 속에 있다고 생각하고 대화해야 해. 주변 환경(소음, 날씨, 장소의 특징 등)을 대화 내용에 적극적으로 반영해줘!
    
    [너의 기본 설정]
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

    # MBTI, 성별, 혹은 설정된 상황이 바뀌면 대화 기록 초기화
    if ("current_mbti" not in st.session_state or st.session_state.current_mbti != selected or 
        "current_gender" not in st.session_state or st.session_state.current_gender != gender or
        "current_situation" not in st.session_state or st.session_state.current_situation != situation):
        
        st.session_state.current_mbti = selected
        st.session_state.current_gender = gender
        st.session_state.current_situation = situation
        st.session_state.messages = [{"role": "assistant", "content": f"안녕! 난 {selected}야. 지금 우리 '{situation}'에 있네? 궁금한 거 있어? 😉", "is_edited": False, "original": ""}]

    st.markdown("---")

    # 기존 대화 출력 (선택한 ai_avatar 및 user_avatar 적용)
    for msg in st.session_state.messages:
        avatar = user_avatar if msg["role"] == "user" else ai_avatar
        with st.chat_message(msg["role"], avatar=avatar):
            if msg.get("is_edited"):
                st.write(f"{msg['content']} *(수정됨)* ⚠️", help=f"🚨 원본 대답: {msg['original']}")
            else:
                st.markdown(msg["content"])

    user_input = st.chat_input(f"[{situation}]에서 {selected}에게 메시지 보내기...")

    if user_input:
        if not api_key:
            st.warning("👈 왼쪽 사이드바에 복사해둔 Gemini API Key를 먼저 붙여넣어 주세요!")
        else:
            # 사용자 메시지 저장 및 출력
            st.session_state.messages.append({"role": "user", "content": user_input, "is_edited": False, "original": ""})
            with st.chat_message("user", avatar=user_avatar):
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
                    content = msg["original"] if msg.get("is_edited") else msg["content"]
                    history.append({"role": role, "parts": [content]})
                    
                chat = model.start_chat(history=history)
                
                with st.chat_message("assistant", avatar=ai_avatar):
                    response = chat.send_message(user_input)
                    ai_reply = response.text
                    
                    # 나쁜 말 필터링 검사 시스템
                    is_bad = any(bad_word in ai_reply for bad_word in BAD_WORDS)
                    
                    if is_bad:
                        import random
                        original_reply = ai_reply 
                        safe_reply = random.choice(GOOD_WORDS) 
                        
                        st.write(f"{safe_reply} *(수정됨)* ⚠️", help=f"🚨 원본 대답: {original_reply}")
                        st.session_state.messages.append({
                            "role": "assistant", "content": safe_reply, "is_edited": True, "original": original_reply
                        })
                    else:
                        st.markdown(ai_reply)
                        st.session_state.messages.append({
                            "role": "assistant", "content": ai_reply, "is_edited": False, "original": ""
                        })
                
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}")
