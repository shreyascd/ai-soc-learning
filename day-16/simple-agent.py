"""
Simple Tool-Using Agent — ReAct pattern, 1 tool (calculator).
Requires: pip install langchain langchain-anthropic
Set your API key first: export ANTHROPIC_API_KEY="your-key-here"

Uses langchain.agents.create_agent — the current recommended way to build
a tool-calling agent (create_react_agent/AgentExecutor are both deprecated).
"""

import ast
import operator

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.tools import tool

# Safe arithmetic evaluator (avoids raw eval() on model-generated input)
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '12 * (4 + 3)'."""
    try:
        result = _safe_eval(ast.parse(expression, mode="eval").body)
        return str(result)
    except Exception as e:
        return f"Error: could not evaluate '{expression}' ({e})"


agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[calculator],
    system_prompt="You are a helpful assistant. Use the calculator tool for any math.",
    middleware=[ModelCallLimitMiddleware(run_limit=5, exit_behavior="end")],  # stopping condition: max iterations
)


def run_and_print(question: str):
    print(f"Question: {question}")
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    for msg in result["messages"]:
        role = msg.__class__.__name__
        if role == "AIMessage" and getattr(msg, "tool_calls", None):
            for call in msg.tool_calls:
                print(f"  [Act]      call {call['name']}({call['args']})")
        elif role == "ToolMessage":
            print(f"  [Observe]  {msg.content}")
        elif role == "AIMessage" and msg.content:
            print(f"  [Reason/Final] {msg.content}")
    print("---")


if __name__ == "__main__":
    run_and_print("What is 47 * 89?")
    run_and_print("If I have 120 alerts and 15% are true positives, how many is that?")
    run_and_print("What's the capital of France?")  # no tool needed — tests it doesn't over-call

    # Expected trace style for question 1:
    #   [Act]      call calculator({'expression': '47 * 89'})
    #   [Observe]  4183
    #   [Reason/Final] 47 * 89 = 4183
