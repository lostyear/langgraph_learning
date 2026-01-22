from typing import Any, Dict
from src.models import AgentInput

from .base_agent import BaseAgent


class TodoAgent(BaseAgent):
    def __init__(
        self,
        model: str,
        system_prompt: str,
        thread_id: str = "basic_agent",
    ):
        from langchain.agents.middleware import (
            HumanInTheLoopMiddleware,
            InterruptOnConfig,
        )
        from src.learn_cc.tools import (
            run_bash,
            read_file,
            write_file,
            edit_file,
            list_files,
            new_todo_tool,
        )

        super().__init__(
            model=model,
            system_prompt=system_prompt,
            thread_id=thread_id,
            tools=[
                run_bash,
                read_file,
                write_file,
                edit_file,
                list_files,
                # TODO: 这里按示例是有个超过N个轮次没用todo就要提示一下的，但是没想好怎么注入
                new_todo_tool(),
            ],
            middleware=[
                # 用户确认节点，用这个必须有checkpointer，不然用户确认完无法恢复
                HumanInTheLoopMiddleware(
                    interrupt_on={
                        run_bash.get_name(): InterruptOnConfig(
                            allowed_decisions=["approve", "reject"]
                        ),
                        write_file.get_name(): True,
                        edit_file.get_name(): True,
                    },
                    description_prefix="write operation, must check it can be done or not.\n",
                )
            ],
        )
