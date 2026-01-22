from .base_agent import BaseAgent


class OriginLangChainAgent(BaseAgent):
    def __init__(
        self,
        model: str,
        system_prompt: str,
        thread_id: str = "origin_langchain_agent",
    ):
        from pathlib import Path
        from langchain.agents.middleware import (
            FilesystemFileSearchMiddleware,
            HostExecutionPolicy,
            ShellToolMiddleware,
            TodoListMiddleware,
        )

        from src.learn_cc.tools import run_bash

        self.workspace_root = Path().cwd()

        super().__init__(
            model=model,
            system_prompt=system_prompt,
            thread_id=thread_id,
            tools=[run_bash],
            middleware=[
                FilesystemFileSearchMiddleware(
                    root_path=str(self.workspace_root),
                ),
                ShellToolMiddleware(
                    workspace_root=self.workspace_root,
                    # ShellToolMiddleware 暂时不支持Human-In-Loop
                    # 只能通过execution_policy设置安全策略
                    execution_policy=HostExecutionPolicy(),
                ),
                TodoListMiddleware(),
            ],
        )
