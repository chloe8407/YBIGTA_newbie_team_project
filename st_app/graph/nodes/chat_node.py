import os
from langchain_upstage import ChatUpstage
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SYSTEM_PROMPT = (
    "당신은 주토피아 영화 팬 커뮤니티의 친근한 챗봇입니다. "
    "자연스럽고 대화체로 답변하세요. "
    "사용자가 주토피아의 영화 정보(출연진, 줄거리, 감독 등)나 "
    "관객 리뷰/평가에 대해 질문하면, 그에 대해서도 도움을 줄 수 있다고 알려주세요. "
    "반드시 한국어로 답변하세요."
)


def chat_node(state: dict) -> dict:
    llm = ChatUpstage(
        api_key=os.environ.get("UPSTAGE_API_KEY"),
        model="solar-mini",
    )

    lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for msg in state.get("messages", []):
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))

    response = llm.invoke(lc_messages)

    return {
        "messages": [{"role": "assistant", "content": response.content}],
        "route": "chat",
    }
