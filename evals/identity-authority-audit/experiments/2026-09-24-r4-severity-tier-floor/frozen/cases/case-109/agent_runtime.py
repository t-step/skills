"""Executes tool calls the agent decides to make.

Today, every call -- read or destructive -- pauses for a human approval
in the support console before running. The team wants to keep that gate
for destructive calls while removing it for routine lookups.
"""

from agent_tools import TOOLS_BY_NAME
import approval_console


def dispatch_tool_call(tool_name: str, args: dict, session_id: str):
    tool = TOOLS_BY_NAME[tool_name]

    # Every call goes through the same approval gate today, regardless of
    # the tool's own "destructive" flag above -- dispatch_tool_call never
    # reads that field. The flag exists on the tool definition but nothing
    # in this function, or anywhere else in this file, branches on it.
    approved = approval_console.wait_for_human_approval(session_id, tool_name, args)
    if not approved:
        return {"error": "not approved"}

    return tool["fn"](**args)
