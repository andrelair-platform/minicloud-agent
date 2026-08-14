"""Mock heavy AI/HTTP deps so tests run without a running cluster."""
import sys
from unittest.mock import AsyncMock, MagicMock

# Stub langgraph before any app import
_langgraph = MagicMock(name="langgraph")
_langgraph.prebuilt.create_react_agent = MagicMock(return_value=AsyncMock())
for mod in ("langgraph", "langgraph.prebuilt"):
    sys.modules.setdefault(mod, _langgraph)

_lc_core = MagicMock(name="langchain_core")
_lc_openai = MagicMock(name="langchain_openai")
for mod in (
    "langchain_core",
    "langchain_core.messages",
    "langchain_core.tools",
    "langchain_openai",
):
    sys.modules.setdefault(mod, _lc_core)

# Make tool decorator a pass-through
_lc_core.tools.tool = lambda f: f
