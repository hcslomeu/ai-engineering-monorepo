---
name: agent-development
description: LangGraph agent development patterns and conventions for this monorepo. Reference when building or modifying agents in apps/*/agent/
user-invocable: true
---

# Skill: Agent Development Patterns

Reference patterns and conventions for building LangGraph agents in this monorepo.

## When to Use

- When building a new agent module in `apps/*/agent/`
- When modifying an existing agent's graph structure
- When adding tools, nodes, or routing logic to an agent
- When the user asks about LangGraph patterns

## Version

These patterns target **langgraph ^1.0** (LangGraph 1.x stable API). If the project upgrades to a new major version, review this skill for breaking changes.

## Agent Module Structure

Every agent lives in `apps/<project>/agent/` with this layout:

```
apps/<project>/agent/
├── __init__.py         # Re-exports: app, run
├── tools.py            # @tool-decorated functions
├── graph.py            # StateGraph definition, nodes, routing
└── (optional) chain.py # Simple chain for comparison/reference
```

## LangGraph StateGraph Pattern

### Graph Architecture

```
START → agent_node → [should_continue?] → tools_node → agent_node → ... → END
```

### State

Use LangGraph's built-in `MessagesState` — it wraps `list[BaseMessage]` with automatic message accumulation:

```python
from langgraph.graph import MessagesState
```

### Nodes

Two standard nodes:

```python
def agent_node(state: MessagesState) -> dict:
    """Call the LLM with the current messages."""
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = get_model().invoke(messages)
    return {"messages": [response]}

def tools_node(state: MessagesState) -> dict:
    """Execute tool calls from the last AI message."""
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
```

### Routing

```python
def should_continue(state: MessagesState) -> str:
    """Route to tools_node if tool calls present, otherwise END."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools_node"
    return END
```

### Graph Assembly

```python
from langgraph.graph import END, START, StateGraph

def build_graph() -> StateGraph:
    graph = StateGraph(MessagesState)
    graph.add_node("agent_node", agent_node)
    graph.add_node("tools_node", tools_node)
    graph.add_edge(START, "agent_node")
    graph.add_conditional_edges("agent_node", should_continue, ["tools_node", END])
    graph.add_edge("tools_node", "agent_node")
    return graph

app = build_graph().compile()
```

## Tool Development

### Creating Tools

```python
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    """Clear docstring — this is the LLM's instruction for when to use the tool."""
    return result
```

Rules:
- Docstring = LLM instruction. Make it clear and specific.
- Type hints = Pydantic auto-schema. The LLM sees the JSON Schema derived from hints.
- Return `str` for simple outputs. The result goes into a `ToolMessage`.

### Tool Registry

```python
TOOLS = [tool_a, tool_b, tool_c]
TOOLS_BY_NAME = {tool.name: tool for tool in TOOLS}
```

### Binding Tools to Model

```python
def get_model() -> Runnable:
    """Lazy-init cached model with tools bound."""
    global _model
    if _model is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        _model = llm.bind_tools(TOOLS)
    return _model
```

Note: `.bind_tools()` returns `Runnable`, not `ChatOpenAI`.

## Testing Patterns

### Mock the LLM, not the graph

```python
@patch("agent.graph.get_model")
def test_run_with_tool_call(self, mock_get_model):
    tool_call_response = AIMessage(
        content="",
        tool_calls=[{"name": "my_tool", "args": {}, "id": "call_1", "type": "tool_call"}],
    )
    final_response = AIMessage(content="Final answer.")
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = [tool_call_response, final_response]
    mock_get_model.return_value = mock_llm

    result = run("user question")
    assert result == "Final answer."
```

### Test categories

| Category | What to test | Mocking needed |
|----------|-------------|----------------|
| Graph structure | `build_graph()` compiles, has expected nodes | None |
| Routing logic | `should_continue()` with various message states | None |
| Tool execution | `tools_node()` with real tools | None (tools are pure functions) |
| Agent node | `agent_node()` calls model correctly | Mock `get_model()` |
| End-to-end | `run()` with tool call loop | Mock `get_model()` |

## Type Hints Gotchas

- `should_continue` returns `str` (not `Literal[...]`) because `END` is typed as `str`
- Narrow `last_message` to `AIMessage` via `isinstance()` before accessing `.tool_calls`
- `tool_calls` is `list[ToolCall]`, not `list[dict]` — but behaves like a TypedDict

## Future Patterns (WP-106+)

These will be added after implementation:
- LangSmith tracing integration
- Human-in-the-loop gates (WP-114)
- Checkpointing and persistence (WP-114)
- Streaming responses
