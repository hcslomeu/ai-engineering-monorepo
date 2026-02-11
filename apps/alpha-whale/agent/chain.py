"""AlphaWhale agent chain — connects finance tools to a ChatModel.

Implements the tool-calling loop: the LLM decides which tools to call,
we execute them, and feed the results back until the LLM has a final answer.
"""

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.messages.tool import ToolCall
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

from agent.tools import calculate_rsi, fetch_btc_price, get_market_summary

TOOLS = [fetch_btc_price, calculate_rsi, get_market_summary]
TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are AlphaWhale, a cryptocurrency market analyst. "
            "Use the available tools to answer questions about Bitcoin prices, "
            "RSI indicators, and market conditions. "
            "Always provide clear, actionable insights based on the data.",
        ),
        ("placeholder", "{messages}"),
    ]
)


def create_model(temperature: float = 0.0) -> Runnable:
    """Create a ChatOpenAI model with tools bound.

    Args:
        temperature: Controls randomness. 0.0 = deterministic, 1.0 = creative.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=temperature)
    return llm.bind_tools(TOOLS)


def invoke_tools(tool_calls: list[ToolCall]) -> list[ToolMessage]:
    """Execute tool calls and return results as ToolMessages."""
    results = []
    for call in tool_calls:
        tool = TOOLS_BY_NAME[call["name"]]
        output = tool.invoke(call["args"])
        results.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
    return results


def run(user_input: str, temperature: float = 0.0) -> str:
    """Run the AlphaWhale agent on a user question.

    Args:
        user_input: The user's question about crypto markets.
        temperature: LLM temperature setting.

    Returns:
        The agent's final text response.
    """
    model = create_model(temperature=temperature)
    messages = PROMPT.invoke({"messages": [HumanMessage(content=user_input)]})

    # Tool-calling loop: keep going until the LLM stops requesting tools
    while True:
        response: AIMessage = model.invoke(messages.to_messages())

        # If no tool calls, the LLM has a final answer
        if not response.tool_calls:
            return str(response.content)

        # Execute the requested tools and add results to the conversation
        messages_list = messages.to_messages() + [response]
        tool_results = invoke_tools(response.tool_calls)
        messages_list.extend(tool_results)

        # Replace messages for next iteration (prompt + history + tool results)
        messages = PROMPT.invoke(
            {"messages": messages_list[1:]}  # skip system (prompt re-adds it)
        )
