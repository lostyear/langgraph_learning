from typing import Any, Dict
from src.models import AgentInput


class BashAgent:
    def __init__(
        self,
        model: str,
        system_prompt: str,
        debug: bool = False,
        thread_id: str = "bash_agent",
    ):
        from langchain.agents import create_agent
        from langgraph.checkpoint.memory import InMemorySaver
        from langchain_core.runnables import RunnableConfig

        from src.learn_cc.tools import run_bash

        # 配置 thread_id 可以标识相同的对话，找到对话历史
        self.cfg = RunnableConfig(configurable={"thread_id": thread_id})
        self.agent = create_agent(
            model=model,
            tools=[run_bash],
            system_prompt=system_prompt,
            # 记忆保存, 这个参数要跟别的配置搭配使用，比如thread_id
            checkpointer=InMemorySaver(),
        )
        self.debug = debug

    async def ainvoke(self, prompt: str) -> Dict[str, Any] | Any:
        from typing import cast
        from langchain.messages import HumanMessage

        result = await self.agent.ainvoke(
            cast(None, AgentInput(messages=[HumanMessage(prompt)])),
            config=self.cfg,
        )
        messages = result.get("messages", [])
        if not messages:
            return result
        for msg in messages:
            if self.debug:
                msg.pretty_print()
        print(messages[-1].content)
        # print(result)
        return result
