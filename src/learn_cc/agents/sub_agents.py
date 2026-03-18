from typing import Any, Dict, List, Literal, NamedTuple
from src.models import AgentInput
from langchain.tools import tool
from langchain.agents.middleware import AgentMiddleware

from .base_agent import BaseAgent

subAgentType = Literal["explore", "plan", "edit"]


class SubAgents(BaseAgent):
    from pathlib import Path
    from langchain.agents.middleware import (
        FilesystemFileSearchMiddleware,
        HostExecutionPolicy,
        ShellToolMiddleware,
    )
    from deepagents.middleware import FilesystemMiddleware

    class subAgentConfig(NamedTuple):
        Description: str
        SystemPrompt: str
        Midwares: List

    workspace_root = Path().cwd()
    subAgentConfigMap = {
        "explore": subAgentConfig(
            Description="Read-only agent for exploring code, finding files, searching",
            SystemPrompt="You are an exploration agent. Search and analyze, but never modify files. Return a concise summary.",
            Midwares=[
                # 用这个可能会检索到大量文件撑爆上下文窗口，需要增加上下文压缩能力才可用
                FilesystemFileSearchMiddleware(
                    root_path=str(workspace_root), max_file_size_mb=1
                ),
                ShellToolMiddleware(
                    workspace_root=workspace_root,
                    execution_policy=HostExecutionPolicy(),
                ),
            ],  # 没有写权限
        ),
        # Code: 完全代理用于实现
        # 有所有工具 - 用于实际编码工作
        "code": subAgentConfig(
            Description="Full agent for implementing features and fixing bugs",
            SystemPrompt="You are a coding agent. Implement the requested changes efficiently.",
            Midwares=[FilesystemMiddleware()],  # 所有工具
        ),
        # Plan: 分析代理用于设计工作
        # 只读，专注于生成计划和策略
        "plan": subAgentConfig(
            Description="Planning agent for designing implementation strategies",
            SystemPrompt="You are a planning agent. Analyze the codebase and output a numbered implementation plan. Do NOT make changes.",
            Midwares=[
                FilesystemFileSearchMiddleware(root_path=str(workspace_root)),
                ShellToolMiddleware(
                    workspace_root=workspace_root,
                    execution_policy=HostExecutionPolicy(),
                ),
            ],  # 只读
        ),
    }
    subAgentDescription = "\n".join(
        f"{name}: {desp}\n" for name, desp in subAgentConfigMap.items()
    )

    def __init__(
        self,
        model: str,
        system_prompt: str,
        thread_id: str = "sub_agent",
    ):
        from functools import partial
        from langchain_core.tools import StructuredTool

        self.subAgents = {
            name: BaseAgent(
                model=model,
                system_prompt=cfg.SystemPrompt,
                thread_id=f"{thread_id}_{name}",
                tools=[],
                middleware=cfg.Midwares,
                # subagent开启记忆会出现序列化异常导致无法完成agent任务
                # TODO: 需要研究一下深层原因，但是没有记忆的话Agent上下文会比较干净，目前可以接
                save_history=False,
            )
            for name, cfg in self.subAgentConfigMap.items()
        }
        super().__init__(
            model=model,
            system_prompt=system_prompt,
            thread_id=thread_id,
            tools=[
                StructuredTool.from_function(
                    coroutine=self.SubAgentTask,
                    name="subagent_task",
                    description=f"""
                        run SubAgent to do a task

                        Args:
                        agent: Agent type
                        description: the job will do (3-5 words, used for display to user)
                        prompt: the prompt to run the sub agent

                        Agent Types:
                        {self.subAgentDescription}
                    """,
                ),
            ],
        )
        # partial(self.SubAgentTask, self)

    # @tool(
    # )
    async def SubAgentTask(self, agent: subAgentType, desprction: str, prompt: str):
        currentAgent = self.subAgents.get(agent)
        if not currentAgent:
            print(f"Can not find agent {agent}!!!")
            return
        print("=" * 40 + f"使用{agent}进行子任务" + "=" * 40)
        print(f"{agent} 使用prompt: {prompt}")
        print("=" * 60)

        result = await currentAgent.astream(prompt=prompt)
        print("=" * 40 + f"{agent} 返回结果：" + "=" * 40)
        print(result)
        print("=" * 60)
        return result
