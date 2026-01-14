from typing import TypedDict, List
from dataclasses import dataclass
from langchain.messages import AnyMessage


class AgentInvokeInput(TypedDict):
    messages: List[AnyMessage]
