from typing import Any, Dict
from src.models import AgentInput

from .base_agent import BaseAgent


class BasicAgent(BaseAgent):
    def __init__(
        self,
        model: str,
        system_prompt: str,
        thread_id: str = "basic_agent",
        debug: bool = False,
    ):
        from src.learn_cc.tools import (
            run_bash,
            read_file,
            write_file,
            edit_file,
            list_files,
        )

        super().__init__(
            model=model,
            system_prompt=system_prompt,
            debug=debug,
            thread_id="bash_agent",
            tools=[
                run_bash,
                read_file,
                write_file,
                edit_file,
                list_files,
            ],
        )
