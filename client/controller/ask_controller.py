from fastapi import APIRouter
from dto.chat_input import ChatInput
from dto.chat_output import ChatOutput
import logging
from ai.graph import create_graph
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)
router = APIRouter()


graph = create_graph()

@router.post("/ask")
async def ask(chat_input: ChatInput):

    logger.info(f"thread_id: {chat_input.thread_id} - Received question: {chat_input.question}")

    config = {
        "configurable": {
            "thread_id": chat_input.thread_id
        }
    }

    response = await graph.ainvoke({
        "thread_id": chat_input.thread_id,
        "messages": [HumanMessage(content=chat_input.question)]
    }, config=config)

    ai_answer = response["messages"][-1].content

    logger.info(f"thread_id: {chat_input.thread_id} - AI answer: {ai_answer}")

    return ChatOutput(answer=ai_answer)