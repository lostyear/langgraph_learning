from typing import TypedDict, List
from langchain.messages import AnyMessage


class AgentInput(TypedDict):
    messages: List[AnyMessage]
