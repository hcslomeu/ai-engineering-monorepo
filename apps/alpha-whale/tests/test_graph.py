"""Tests for AlphaWhale LangGraph agent.

All tests use mocked LLM responses to avoid API calls.
Tests verify graph structure, routing logic, and end-to-end execution.
"""

from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from agent.graph import (
    TOOLS,
    TOOLS_BY_NAME,
    agent_node,
    build_graph,
    run,
    should_continue,
    tools_node,
)

# --- Graph structure ---


class TestGraphStructure:
    def test_graph_compiles(self):
        graph = build_graph()
        compiled = graph.compile()
        assert compiled is not None

    def test_graph_has_expected_nodes(self):
        graph = build_graph()
        node_names = set(graph.nodes.keys())
        assert "agent_node" in node_names
        assert "tools_node" in node_names


# --- Routing logic ---


class TestShouldContinue:
    def test_routes_to_tools_when_tool_calls_present(self):
        ai_msg = AIMessage(
            content="",
            tool_calls=[
                {"name": "fetch_btc_price", "args": {}, "id": "call_1", "type": "tool_call"}
            ],
        )
        state = {"messages": [HumanMessage(content="hi"), ai_msg]}
        assert should_continue(state) == "tools_node"

    def test_routes_to_end_when_no_tool_calls(self):
        ai_msg = AIMessage(content="Bitcoin is at $50,000.")
        state = {"messages": [HumanMessage(content="hi"), ai_msg]}
        assert should_continue(state) == "__end__"

    def test_routes_to_end_for_empty_tool_calls(self):
        ai_msg = AIMessage(content="Here's the answer.", tool_calls=[])
        state = {"messages": [HumanMessage(content="hi"), ai_msg]}
        assert should_continue(state) == "__end__"


# --- Agent node ---


class TestAgentNode:
    @patch("agent.graph.get_model")
    def test_agent_node_returns_messages(self, mock_get_model: MagicMock):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="Hello!")
        mock_get_model.return_value = mock_llm

        state = {"messages": [HumanMessage(content="What is BTC price?")]}
        result = agent_node(state)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert result["messages"][0].content == "Hello!"

    @patch("agent.graph.get_model")
    def test_agent_node_passes_history(self, mock_get_model: MagicMock):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="Done")
        mock_get_model.return_value = mock_llm

        history = [
            HumanMessage(content="q1"),
            AIMessage(content="a1"),
            HumanMessage(content="q2"),
        ]
        agent_node({"messages": history})

        # LLM should receive system prompt + full history
        call_args = mock_llm.invoke.call_args[0][0]
        assert len(call_args) == 4  # system + 3 history messages


# --- Tools node ---


class TestToolsNode:
    def test_executes_fetch_btc_price(self):
        tool_call = {"name": "fetch_btc_price", "args": {}, "id": "call_1", "type": "tool_call"}
        ai_msg = AIMessage(content="", tool_calls=[tool_call])
        state = {"messages": [HumanMessage(content="price?"), ai_msg]}

        result = tools_node(state)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], ToolMessage)
        assert result["messages"][0].tool_call_id == "call_1"

    def test_executes_calculate_rsi(self):
        prices = [100 + i for i in range(20)]
        tool_call = {
            "name": "calculate_rsi",
            "args": {"prices": prices},
            "id": "call_2",
            "type": "tool_call",
        }
        ai_msg = AIMessage(content="", tool_calls=[tool_call])
        state = {"messages": [HumanMessage(content="rsi?"), ai_msg]}

        result = tools_node(state)

        assert len(result["messages"]) == 1
        assert result["messages"][0].tool_call_id == "call_2"

    def test_executes_get_market_summary(self):
        tool_call = {
            "name": "get_market_summary",
            "args": {},
            "id": "call_3",
            "type": "tool_call",
        }
        ai_msg = AIMessage(content="", tool_calls=[tool_call])
        state = {"messages": [HumanMessage(content="market?"), ai_msg]}

        result = tools_node(state)

        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], ToolMessage)
        assert result["messages"][0].tool_call_id == "call_3"

    def test_handles_unknown_tool_name(self):
        tool_call = {"name": "nonexistent_tool", "args": {}, "id": "call_x", "type": "tool_call"}
        ai_msg = AIMessage(content="", tool_calls=[tool_call])
        state = {"messages": [HumanMessage(content="test"), ai_msg]}

        result = tools_node(state)

        assert len(result["messages"]) == 1
        assert "Error: unknown tool" in result["messages"][0].content
        assert result["messages"][0].tool_call_id == "call_x"

    def test_tools_by_name_has_all_tools(self):
        assert set(TOOLS_BY_NAME.keys()) == {
            "fetch_btc_price",
            "calculate_rsi",
            "get_market_summary",
        }
        assert len(TOOLS_BY_NAME) == len(TOOLS)


# --- End-to-end (mocked LLM) ---


class TestRunFunction:
    @patch("agent.graph.get_model")
    def test_run_returns_final_answer(self, mock_get_model: MagicMock):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="BTC is at $50,000.")
        mock_get_model.return_value = mock_llm

        result = run("What is the BTC price?")
        assert result == "BTC is at $50,000."

    @patch("agent.graph.get_model")
    def test_run_with_tool_call_loop(self, mock_get_model: MagicMock):
        """Simulate: LLM requests tool -> tool runs -> LLM gives final answer."""
        tool_call_response = AIMessage(
            content="",
            tool_calls=[
                {"name": "fetch_btc_price", "args": {}, "id": "call_1", "type": "tool_call"}
            ],
        )
        final_response = AIMessage(content="Bitcoin is currently at $55,000.")

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = [tool_call_response, final_response]
        mock_get_model.return_value = mock_llm

        result = run("What is Bitcoin's price?")
        assert result == "Bitcoin is currently at $55,000."
        assert mock_llm.invoke.call_count == 2
