"""
Logged Agent — Day 16 simple agent with detailed logging.
Logs each LLM call, each tool call, and each observation.
Requires: pip install langchain langchain-anthropic
Set your API key first: export ANTHROPIC_API_KEY="your-key-here"
"""

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("agent")

import ast
import operator
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.tools import tool

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
    logger.info(f"[TOOL_CALL] calculator(expression='{expression}')")
    try:
        result = _safe_eval(ast.parse(expression, mode="eval").body)
        logger.info(f"[TOOL_RESULT] calculator returned: {result}")
        return str(result)
    except Exception as e:
        error_msg = f"Error: could not evaluate '{expression}' ({e})"
        logger.error(f"[TOOL_ERROR] calculator: {error_msg}")
        return error_msg


class LoggingAgent:
    def __init__(self):
        self.call_count = 0
        self.tool_call_count = 0
        
        self.agent = create_agent(
            model="anthropic:claude-sonnet-4-6",
            tools=[calculator],
            system_prompt="You are a helpful math assistant. Use the calculator tool for any arithmetic.",
            middleware=[ModelCallLimitMiddleware(run_limit=5, exit_behavior="end")],
        )
    
    def run(self, question: str):
        self.call_count += 1
        self.tool_call_count = 0
        logger.info(f"\n[QUERY #{self.call_count}] {question}")
        
        result = self.agent.invoke({"messages": [{"role": "user", "content": question}]})
        
        final_answer = ""
        for msg in result["messages"]:
            role = msg.__class__.__name__
            if role == "AIMessage" and getattr(msg, "tool_calls", None):
                for call in msg.tool_calls:
                    self.tool_call_count += 1
                    logger.info(f"[LLM_DECISION] Call tool: {call['name']}")
            elif role == "ToolMessage":
                logger.info(f"[OBSERVATION] {msg.content}")
            elif role == "AIMessage" and msg.content:
                final_answer = msg.content
                logger.info(f"[FINAL_ANSWER] {msg.content}")
        
        logger.info(f"[STATS] Query {self.call_count}: {self.tool_call_count} tool calls\n")
        return final_answer


if __name__ == "__main__":
    agent = LoggingAgent()
    
    agent.run("What is 47 * 89?")
    agent.run("If I have 120 alerts and 15% are true positives, how many is that?")
    agent.run("What's 2 + 2?")  # Simple, no tool needed
    
    logger.info(f"Total queries: {agent.call_count}")
