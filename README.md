# MCP Server & LangChain + LangGraph Client Implementation 🦜⛓️
MCP server with FastMCP and LLM client with LangChain + LangGraph with the OpenAI LLM

## MCP Client Implementation

The client is a FastAPI application with LangChain + LangGraph. The main structure of the client is a State Graph, used to manage the state and the flow of the conversation. The thread id is the key to identify the conversation and the state of the conversation, allowing the agent to have memory, similar to what Agent LLMs applications do (e.g. ChatGPT, Claude Desktop, etc).

The agent (`attendance_agent.py`) is the ReAct (Reasoning + Action) agent. It is responsible for reasoning about the user's request and deciding which tool to use, calling the tool and returning the result to the user.[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629).

### Running the client

1. Install the dependencies with uv:

```bash
uv sync
```

2. Run the client:

```bash
uv run python main.py --port 8080
```

3. Call the Ask endpoint:

```bash
curl -X POST http://localhost:8080/ask -H "Content-Type: application/json" -d '{"thread_id": "123", "question": "How many orders did John Doe place in March 2025?"}'
```

## MCP Server Implementation

The MCP server is implemented with FastMCP. The server is responsible for providing the tools to the client.

### Running the MCP server

1. Install the dependencies with uv:

```bash
uv sync
```

2. Run the ngrok tunnel:

```bash
ngrok http --url={ngrok_url} 8000
```

3. Run the MCP server:

```bash
uv run python main.py --port 8000
```

### Running tool tests
1. Inside the server folder, run:
```bash
uv run pytest tests/ -v
```

## Improvements
- Use a guardrail (like AWS Bedrock Guardrails) to avoid prompt injection, hallucinations, security issues, unwanted topics, etc.
- Use a more rebust checkpointer, like a Redis or a database, with TTL and message summary to don't spend too much tokens and memory.
- Improve error handling
- Add thread_id to the logs, like a "trace". 
- Propagate the thread_id to the tools via personalized HTTP header to maintain the tracing of the conversation.
- Add a security layer to the MCP server, like a token or a key to authenticate the client.
- Refine the prompt and add more information about the business, the persona, the context, etc.
- End the unit tests for the tools and integration tests
- Use HTTP errors codes to return the error to the client with a friendly message to be disposed in the chat/frontend.

## Assumptions
- To give state to the graph, I added the thread_id to ask payload. 
