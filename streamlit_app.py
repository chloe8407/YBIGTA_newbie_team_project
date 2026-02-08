"""
Streamlit 기반 영화 리뷰 RAG Agent 챗봇 UI
팀원들의 st_app 패키지와 연동
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# 프로젝트 루트를 파이썬 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


# ── 영화 정보 로드 ──────────────────────────────────────────
SUBJECTS_PATH = os.path.join(current_dir, "st_app", "db", "subject_information", "subjects.json")


def load_subjects():
    """subjects.json 로드"""
    try:
        with open(SUBJECTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data[0] if isinstance(data, list) and data else {}
    except Exception:
        return {}


def answer_subject_question(question: str, movie: dict) -> str:
    """영화 정보 질문에 규칙 기반으로 답변"""
    if not movie:
        return "영화 정보를 불러올 수 없습니다."

    q = question.lower()

    if any(kw in q for kw in ["감독", "director", "누가 만들"]):
        directors = ", ".join(movie.get("director", []))
        return f"🎬 주토피아의 감독은 **{directors}** 입니다."

    if any(kw in q for kw in ["언제", "개봉", "release", "when"]):
        return f"📅 주토피아는 **{movie.get('release_date', 'Unknown')}** 에 개봉했습니다."

    if any(kw in q for kw in ["출연", "배우", "캐릭터", "등장인물", "cast", "character"]):
        chars = ", ".join(movie.get("characters", []))
        return f"🎭 주토피아의 주요 캐릭터: **{chars}**"

    if any(kw in q for kw in ["줄거리", "plot", "story", "내용"]):
        return f"📖 **줄거리**:\n{movie.get('plot', 'No plot available')}"

    if any(kw in q for kw in ["장르", "genre"]):
        genres = ", ".join(movie.get("genre", []))
        return f"🎭 주토피아는 **{genres}** 장르입니다."

    if any(kw in q for kw in ["러닝타임", "시간", "runtime", "길이"]):
        return f"⏱️ 주토피아의 러닝타임은 **{movie.get('running_time', 'Unknown')}** 입니다."

    if any(kw in q for kw in ["플랫폼", "사이트", "platform", "어디서"]):
        platforms = ", ".join(movie.get("platform", []))
        return f"🌐 리뷰 수집 플랫폼: **{platforms}**"

    # 기본: 전체 정보 요약
    directors = ", ".join(movie.get("director", []))
    genres = ", ".join(movie.get("genre", []))
    chars = ", ".join(movie.get("characters", []))
    return (
        f"🎬 **{movie.get('title', '')}** ({movie.get('title_ko', '')})\n\n"
        f"📅 **개봉일**: {movie.get('release_date', 'Unknown')}\n"
        f"🎭 **감독**: {directors}\n"
        f"🎨 **장르**: {genres}\n"
        f"⏱️ **러닝타임**: {movie.get('running_time', 'Unknown')}\n"
        f"👥 **주요 캐릭터**: {chars}\n\n"
        f"📖 **줄거리**: {movie.get('plot', '')}"
    )


# ── LLM 기반 라우팅 ──────────────────────────────────────────
ROUTER_SYSTEM_PROMPT = """너는 사용자의 질문을 분류하는 라우터야.
주토피아(Zootopia) 영화에 대한 챗봇에서 사용되고 있어.

사용자의 질문을 아래 3가지 중 하나로 분류해. 반드시 해당 단어 하나만 답해.

- info : 영화의 기본 정보를 묻는 질문 (감독, 출연진, 줄거리, 개봉일, 장르, 러닝타임 등)
- review : 관객/사람들의 리뷰, 반응, 평가, 의견을 묻는 질문
- chat : 일상 대화, 인사, 영화와 무관한 질문

반드시 info, review, chat 중 하나만 답해. 다른 말은 하지 마."""


def classify_question(question: str) -> str:
    """LLM 기반 질문 분류"""
    try:
        from st_app.rag.llm import generate_text
        result = generate_text(
            system_prompt=ROUTER_SYSTEM_PROMPT,
            user_prompt=question,
            temperature=0.0,
        )
        # LLM 응답에서 분류 결과 추출
        result = result.strip().lower()
        if "info" in result:
            return "info"
        if "review" in result:
            return "review"
        return "chat"
    except Exception:
        # API 오류 시 기본값: chat
        return "chat"


def get_bot_response(user_message: str) -> str:
    """사용자 메시지에 대한 봇 응답 생성"""
    category = classify_question(user_message)

    # 1) 영화 정보 질문
    if category == "info":
        movie = load_subjects()
        return answer_subject_question(user_message, movie)

    # 2) 리뷰 질문 → RAG Review Node 호출
    if category == "review":
        try:
            from st_app.graph.nodes.rag_review_node import rag_review_node
            return rag_review_node(question=user_message, top_k=3)
        except FileNotFoundError:
            return "⚠️ FAISS 인덱스를 찾을 수 없습니다. embedder를 먼저 실행해주세요."
        except ValueError as e:
            return f"⚠️ API 키 오류: {e}\n\n`.env` 파일에 `UPSTAGE_API_KEY`를 설정해주세요."
        except Exception as e:
            return f"⚠️ 리뷰 검색 중 오류가 발생했습니다: {e}"

    # 3) 일반 대화 → LLM 호출
    try:
        from st_app.rag.llm import generate_text
        return generate_text(
            system_prompt="너는 친절하고 자연스러운 대화를 하는 챗봇이야. 한국어로 답변하고, 간결하게 대화해.",
            user_prompt=user_message,
        )
    except ValueError:
        return "안녕하세요! 무엇이든 편하게 물어보세요 😊"
    except Exception:
        return "안녕하세요! 무엇이든 편하게 물어보세요 😊"


# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title="Zootopia Review Chatbot",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 커스텀 CSS ──────────────────────────────────────────
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f0fe 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stChatMessage {
        background-color: white;
        border-radius: 18px;
        padding: 16px 20px;
        margin: 12px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        animation: fadeIn 0.4s ease-in;
        transition: all 0.2s ease;
        border: 1px solid rgba(0,0,0,0.05);
    }
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.12);
    }
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 35px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        animation: slideDown 0.6s ease-out;
    }
    .chat-header h1 {
        font-size: 2.5em; font-weight: bold; margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2); letter-spacing: 1px;
    }
    .chat-header p {
        font-size: 1.15em; margin: 12px 0 0 0; opacity: 0.95;
    }
    .sidebar-info {
        background-color: #f0f2f6;
        padding: 15px; border-radius: 10px; margin: 10px 0;
    }
    .sidebar-info strong {
        font-size: 1em; display: block; margin-bottom: 8px;
    }
    .message-timestamp {
        font-size: 0.75em; color: #666; margin-top: 8px;
        opacity: 0.7; font-style: italic;
    }
    .input-container {
        position: sticky; top: 0; background: transparent;
        padding: 15px 0; z-index: 100; margin-bottom: 20px;
    }
    .stTextInput > div > div > input {
        border-radius: 30px; border: 2px solid #667eea;
        padding: 14px 24px; font-size: 1.05em;
        transition: all 0.3s ease; background: white;
    }
    .stTextInput > div > div > input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
        outline: none;
    }
    .stButton > button {
        border-radius: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none;
        padding: 14px 28px; font-weight: bold; font-size: 1.05em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @media (max-width: 768px) {
        .chat-header h1 { font-size: 1.8em; }
    }
    </style>
""", unsafe_allow_html=True)


# ── 세션 초기화 ──────────────────────────────────────────
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "안녕하세요! 🐰🥕 주토피아 리뷰 챗봇입니다.\n\n"
                       "저는 주디예요! 주토피아 영화에 대한 모든 정보를 알려드릴 수 있어요! 🎬✨\n\n"
                       "궁금한 점이 있으시면 편하게 물어보세요! 🦊",
            "timestamp": datetime.now().strftime("%H:%M"),
        }]


def display_chat_history():
    for msg in st.session_state.messages:
        avatar = "🐰" if msg["role"] == "assistant" else "🦊"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if "timestamp" in msg:
                st.markdown(
                    f'<div class="message-timestamp">{msg["timestamp"]}</div>',
                    unsafe_allow_html=True,
                )


# ── 메인 ──────────────────────────────────────────────────
def main():
    initialize_session_state()

    # 헤더
    st.markdown("""
        <div class="chat-header">
            <h1>🎬 Zootopia Review Chatbot 🥕</h1>
            <p>✨ 주토피아 영화 정보 & 리뷰 AI 어시스턴트 ✨</p>
        </div>
    """, unsafe_allow_html=True)

    # 사이드바
    with st.sidebar:
        st.markdown("### 📊 챗봇 정보")
        st.markdown("""
            <div class="sidebar-info">
                <strong>🎯 기능</strong><br>
                • 영화 기본 정보 제공<br>
                • 사용자 리뷰 검색 (RAG)<br>
                • 자연어 대화 지원<br>
            </div>
        """, unsafe_allow_html=True)

        # 대화 초기화
        if st.button("🗑️ 대화 내역 초기화", use_container_width=True):
            st.session_state.messages = [{
                "role": "assistant",
                "content": "대화 내역이 초기화되었습니다. 다시 시작해볼까요? 🐰🥕",
                "timestamp": datetime.now().strftime("%H:%M"),
            }]
            st.rerun()

        st.markdown("---")
        st.markdown("""
            <div class="sidebar-info">
                <strong>💡 질문 예시</strong><br>
                🎭 "감독이 누구야?"<br>
                📅 "언제 개봉했어?"<br>
                📖 "줄거리 알려줘"<br>
                ⭐ "사람들 반응 어때?"<br>
                💬 "어떤 점이 좋았대?"<br>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: #888; font-size: 0.9em;">
                Made by YBIGTA<br>
                5조: 안재후, 이근하, 변민주
            </div>
        """, unsafe_allow_html=True)

    # 메인 채팅 영역
    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:
        # 입력창 (상단 고정)
        with st.form(key="chat_form", clear_on_submit=True):
            input_col1, input_col2 = st.columns([5, 1])
            with input_col1:
                user_input = st.text_input(
                    "메시지를 입력하세요...",
                    key="user_input",
                    label_visibility="collapsed",
                    placeholder="주토피아에 대해 물어보세요...",
                )
            with input_col2:
                send_button = st.form_submit_button(
                    "전송", use_container_width=True, type="primary"
                )

        # 전송 처리
        if send_button and user_input.strip():
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": timestamp,
            })

            with st.spinner("🐰 생각 중..."):
                response = get_bot_response(user_input)
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": timestamp,
                })
            st.rerun()

        # 채팅 히스토리
        display_chat_history()


if __name__ == "__main__":
    main()
