"""
LangGraph node that wraps the RAG pipeline: retrieves relevant review
chunks via FAISS and generates an LLM answer grounded in those reviews.
"""
from st_app.rag.llm import generate_text
from st_app.rag.prompt import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT_TEMPLATE
from st_app.rag.retriever import retrieve

MAX_CONTEXT_CHARS = 12_000


def rag_review_node(state: dict) -> dict:
    last_user_msg = ""
    for msg in reversed(state.get("messages", [])):
        if msg.get("role") == "user":
            last_user_msg = msg.get("content", "")
            break

    docs = retrieve(query=last_user_msg, top_k=3)

    if not docs:
        return {
            "messages": [{"role": "assistant", "content": "리뷰 정보를 충분히 찾지 못했습니다."}],
            "route": "review",
            "retrieved_docs": [],
        }

    context_parts = [d.page_content for d in docs]
    context = "\n\n---\n\n".join(context_parts)

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS] + "\n\n[... truncated]"

    user_prompt = RAG_USER_PROMPT_TEMPLATE.format(
        question=last_user_msg, context=context,
    )
    answer = generate_text(
        system_prompt=RAG_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.2,
    )

    retrieved_docs = [
        {"content": d.page_content, "metadata": d.metadata} for d in docs
    ]

    return {
        "messages": [{"role": "assistant", "content": answer.strip() if answer else "리뷰에서 답변을 생성하지 못했습니다."}],
        "route": "review",
        "retrieved_docs": retrieved_docs,
    }
