import json
import os
from pathlib import Path
from langchain_upstage import ChatUpstage
from langchain_core.messages import SystemMessage, HumanMessage

SUBJECTS_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "db"
    / "subject_information"
    / "subjects.json"
)

SYSTEM_PROMPT = """당신은 주토피아 영화 전문가입니다. 아래 제공된 영화 데이터만을 사용하여 사용자의 질문에 답변하세요.

규칙:
- 자연스럽고 대화체로 답변하세요. 원시 데이터를 그대로 출력하지 마세요.
- 데이터에 없는 내용은 "해당 정보가 없습니다"라고 답하세요. 추측하지 마세요.
- 반드시 한국어로 답변하세요.

영화 데이터:
{subject_data}"""


def _load_subjects() -> str:
    with open(SUBJECTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return json.dumps(data, ensure_ascii=False, indent=2)


def subject_info_node(state: dict) -> dict:
    llm = ChatUpstage(
        api_key=os.environ.get("UPSTAGE_API_KEY"),
        model="solar-mini",
    )

    subject_data = _load_subjects()

    last_user_msg = ""
    for msg in reversed(state.get("messages", [])):
        if msg.get("role") == "user":
            last_user_msg = msg.get("content", "")
            break

    lc_messages = [
        SystemMessage(content=SYSTEM_PROMPT.format(subject_data=subject_data)),
        HumanMessage(content=last_user_msg),
    ]

    response = llm.invoke(lc_messages)

    return {
        "messages": [{"role": "assistant", "content": response.content}],
        "route": "subject",
    }
