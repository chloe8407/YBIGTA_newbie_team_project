import os
from langchain_upstage import ChatUpstage
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SYSTEM_PROMPT = (
    "당신은 친절하고 자연스러운 대화를 하는 챗봇입니다. "
    "사용자와 일상적인 대화를 자연스럽게 나누세요. "
    "반드시 한국어로 답변하고, 간결하게 대화하세요."
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
