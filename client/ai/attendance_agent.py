
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from ai.state import State
from ai.mcp_client import get_mcp_client
import os
import logging
from utils.exception_handler import handle_agent_exception

logger = logging.getLogger(__name__)

load_dotenv()

async def attendance_agent(state: State) -> State:
    try:
        logger.debug(f"thread_id: {state['thread_id']} - Starting agent execution")
        model = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.33,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", """
                    You're a helpful attendance agent that answers questions about customers and orders.
                 
                    Always answer in plain text, never use markdown or JSON.
                """),
                ("placeholder", "{messages}")
            ]
        )

        logger.debug(f"thread_id: {state['thread_id']} - Getting MCP tools")
        mcp_client = get_mcp_client()

        mcp_tools = await mcp_client.get_tools()

        agent = create_react_agent(
            model=model,
            tools=mcp_tools,
            checkpointer=False,
            prompt=prompt_template
        )

        logger.debug(f"thread_id: {state['thread_id']} - Invoking agent")
        response = await agent.ainvoke(
            {"messages": state["messages"]},
            config={
                "configurable": {
                    "max_iterations": 3,
                    "max_execution_time": 30,
                    "max_retries": 3
                }
            }
        )

        logger.debug(f"thread_id: {state['thread_id']} - Agent response: {response}")

        last_message = response["messages"][-1]

        state["messages"].append(last_message)
        return state
    except Exception as e:
        error_message = handle_agent_exception(e, logger, state["thread_id"])
        state["messages"].append(error_message)
        return state