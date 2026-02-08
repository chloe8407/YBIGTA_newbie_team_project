"""
<<<<<<< HEAD
LangGraph node that wraps the RAG pipeline: retrieves relevant review
chunks via FAISS and generates an LLM answer grounded in those reviews.
=======
FAISS-based Review RAG node: retrieves relevant review chunks and generates
an LLM answer grounded in those reviews. Use when the user asks for
reviews, opinions, or audience reactions.
>>>>>>> 33ccc5758dca8c4e90bbf07724094032f68f1a57
"""
from st_app.rag.llm import generate_text
from st_app.rag.prompt import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT_TEMPLATE
from st_app.rag.retriever import retrieve

<<<<<<< HEAD
MAX_CONTEXT_CHARS = 12_000


def rag_review_node(state: dict) -> dict:
    last_user_msg = ""
    for msg in reversed(state.get("messages", [])):
        if msg.get("role") == "user":
            last_user_msg = msg.get("content", "")
            break

    docs = retrieve(query=last_user_msg, top_k=3)
=======
# Optional: cap total context length to avoid overflow (chars)
MAX_CONTEXT_CHARS = 12_000


def rag_review_node(question: str, top_k: int = 3) -> str:
    """
    Retrieve relevant review chunks via FAISS, then generate an LLM answer
    grounded in those reviews.

    Args:
        question: User question (e.g. about reviews/opinions/audience reactions).
        top_k: Number of documents to retrieve (default 3).

    Returns:
        Final natural language answer as a plain string. On empty retrieval,
        returns a safe fallback message.
    """
    docs = retrieve(query=question, top_k=top_k)
>>>>>>> 33ccc5758dca8c4e90bbf07724094032f68f1a57

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

<<<<<<< HEAD
    return {
        "messages": [{"role": "assistant", "content": answer.strip() if answer else "리뷰에서 답변을 생성하지 못했습니다."}],
        "route": "review",
        "retrieved_docs": retrieved_docs,
    }
=======
if __name__ == "__main__":
    sample_query = "What do people think about the acting and the ending?"
    print("Query:", sample_query)
    print("-" * 60)
    try:
        out = rag_review_node(question=sample_query, top_k=3)
        print(out)
    except FileNotFoundError as e:
        print("Error:", e)
        print("Run the embedder first to create the FAISS index.")
    except ValueError as e:
        print("Error:", e)
        print("Set UPSTAGE_API_KEY in your environment or .env file.")
>>>>>>> 33ccc5758dca8c4e90bbf07724094032f68f1a57
