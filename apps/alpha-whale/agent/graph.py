"""AlphaWhale agent graph — LangGraph StateGraph implementation.

Replaces the manual tool-calling loop from chain.py with a declarative graph:
START → agent_node → [has tool calls?] → tools_node → agent_node → ... → END
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph

from agent.tools import calculate_rsi, fetch_btc_price, get_market_summary

TOOLS = [fetch_btc_price, calculate_rsi, get_market_summary]
TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}

SYSTEM_PROMPT = (
    "You are AlphaWhale, a cryptocurrency market analyst. "
    "Use the available tools to answer questions about Bitcoin prices, "
    "RSI indicators, and market conditions. "
    "Always provide clear, actionable insights based on the data."
)


_model: Runnable | None = None


def get_model() -> Runnable:
    """Return a cached ChatOpenAI model with tools bound.

    Lazily creates the model on first call to avoid requiring an API key at
    import time. Subsequent calls return the cached instance.
    """
    global _model  # noqa: PLW0603
    if _model is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        _model = llm.bind_tools(TOOLS)
    return _model


def agent_node(state: MessagesState) -> dict:
    """Call the LLM with the current messages and return its response."""
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = get_model().invoke(messages)
    return {"messages": [response]}


def tools_node(state: MessagesState) -> dict:
    """Execute tool calls from the last AI message and return results."""
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        return {"messages": []}
    results = []
    for call in last_message.tool_calls:
        tool = TOOLS_BY_NAME.get(call["name"])
        if tool is None:
            output = f"Error: unknown tool '{call['name']}'"
        else:
            output = tool.invoke(call["args"])
        results.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
    return {"messages": results}


def should_continue(state: MessagesState) -> str:
    """Route to tools_node if the LLM made tool calls, otherwise end."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools_node"
    return END


def build_graph() -> StateGraph:
    """Construct the AlphaWhale agent graph (uncompiled)."""
    graph = StateGraph(MessagesState)

    graph.add_node("agent_node", agent_node)
    graph.add_node("tools_node", tools_node)

    graph.add_edge(START, "agent_node")
    graph.add_conditional_edges("agent_node", should_continue, ["tools_node", END])
    graph.add_edge("tools_node", "agent_node")

    return graph


# Compiled graph ready for invocation
app = build_graph().compile()


def run(user_input: str) -> str:
    """Run the AlphaWhale agent graph on a user question.

    Args:
        user_input: The user's question about crypto markets.

    Returns:
        The agent's final text response.
    """
    config: RunnableConfig = {"run_name": "alpha-whale-agent", "tags": ["alpha-whale"]}
    result = app.invoke(
        {"messages": [HumanMessage(content=user_input)]},  # type: ignore[arg-type]
        config=config,
    )
    return str(result["messages"][-1].content)
