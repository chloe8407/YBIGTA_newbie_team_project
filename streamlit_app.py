import streamlit as st
import sys
import os
from datetime import datetime
from dotenv import load_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


load_dotenv()



def get_bot_response(messages: list) -> str:
    """팀원들이 만든 LangGraph app을 호출하여 응답 생성"""
    try:
        from st_app.graph import app

        state = {"messages": messages, "route": "", "retrieved_docs": []}
        result = app.invoke(state)

      
        for msg in reversed(result.get("messages", [])):
            if msg.get("role") == "assistant":
                return msg.get("content", "")

        return "응답을 생성하지 못했습니다."
    except FileNotFoundError:
        return "⚠️ FAISS 인덱스를 찾을 수 없습니다. embedder를 먼저 실행해주세요."
    except ValueError as e:
        return f"⚠️ API 키 오류: {e}\n\n`.env` 파일에 `UPSTAGE_API_KEY`를 설정해주세요."
    except Exception as e:
        return f"⚠️ 오류가 발생했습니다: {e}"



st.set_page_config(
    page_title="Zootopia Review Chatbot",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


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



def main():
    initialize_session_state()


    st.markdown("""
        <div class="chat-header">
            <h1>🎬 Zootopia Review Chatbot 🥕</h1>
            <p>✨ 주토피아 영화 정보 & 리뷰 AI 어시스턴트 ✨</p>
        </div>
    """, unsafe_allow_html=True)


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

    
    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:
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

        
        if send_button and user_input.strip():
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": timestamp,
            })

            
            graph_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[1:]
            ]

            with st.spinner("🐰 생각 중..."):
                response = get_bot_response(graph_messages)
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": timestamp,
                })
            st.rerun()

       
        display_chat_history()


if __name__ == "__main__":
    main()
