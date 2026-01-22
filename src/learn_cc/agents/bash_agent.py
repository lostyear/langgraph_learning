from typing import Any, Dict
from src.models import AgentInput

from .base_agent import BaseAgent


class BashAgent(BaseAgent):
    def __init__(
        self,
        model: str,
        system_prompt: str,
        thread_id: str = "bash_agent",
    ):
        from src.learn_cc.tools import run_bash

        super().__init__(
            model=model,
            system_prompt=system_prompt,
            thread_id=thread_id,
            tools=[run_bash],
        )
