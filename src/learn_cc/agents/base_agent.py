from typing import Any, Dict, List, Literal, Optional, TypedDict
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage
from langchain.tools import BaseTool
from langgraph.types import Interrupt, Command

from src.models import AgentInput


class BaseAgent:
    def __init__(
        self,
        model: str,
        system_prompt: str,
        thread_id: str,
        tools: List[BaseTool] = [],
        **kwargs,
    ):
        import logging
        from langchain.chat_models import init_chat_model
        from langchain.agents import create_agent
        from langgraph.checkpoint.memory import InMemorySaver
        from langchain_core.runnables import RunnableConfig

        # 配置 thread_id 可以标识相同的对话，找到对话历史
        self.cfg = RunnableConfig(configurable={"thread_id": thread_id})
        self.agent = create_agent(
            model=init_chat_model(
                model=model,
                streaming=False,
            ),
            tools=tools,
            system_prompt=system_prompt,
            # 记忆保存, 这个参数要跟别的配置搭配使用，比如thread_id
            checkpointer=InMemorySaver(),
            **kwargs,
        )
        self.logger = logging.getLogger(__name__)

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
            msg.pretty_print()
        print(messages[-1].content)
        # print(result)
        return result

    async def astream(self, prompt: str):
        from typing import cast
        from langchain.messages import HumanMessage

        inputs = cast(None, AgentInput(messages=[HumanMessage(prompt)]))

        while True:
            interrupts: List[Interrupt] = []
            async for chunk in self.agent.astream(
                inputs,
                stream_mode="updates",
                config=self.cfg,
            ):
                for step, update in chunk.items():
                    self.logger.info(f"current step: {step}")
                    if step in ("model", "tools"):
                        message = update["messages"][-1]
                        self.logger.info(f"message type: {type(message)}")
                        message.pretty_print()
                    if step == "__interrupt__":
                        interrupts.extend(update)

            # 没中断，那说明结束了，直接返回
            if not interrupts:
                return

            # 收集用户的决策
            decisions = []
            for interrupt in interrupts:
                v = interrupt.value
                actions = v.get("action_requests", [])
                cfgs = v.get("review_configs", [])
                for i, action in enumerate(actions):
                    cfg = cfgs[i]
                    name = action.get("name", "unknown")
                    choices = cfg.get("allowed_decisions", [])

                    while True:
                        print(
                            f"Please decide wheather {name} should run or not: "
                            "\n"
                            f"The args of {name} is {action.get("args", {})}"
                            "\n"
                            f"Choices: {"/".join(choices)}"
                            "\n"
                        )
                        try:
                            d = input("Your Decision: \n").strip().lower()
                        except (InterruptedError, EOFError):
                            print("user interrupt, exit...")
                            return
                        if (not d in choices) and ("edit" not in choices):
                            print(f"Invaild choice, please try again")
                            continue
                        if d in ("approve", "reject"):
                            decisions.append({"type": d})
                            break
                        # TODO: 这里应该是改arg，但是有点复杂，先不管了
                        decisions.append({"type": "edit", "message": d})
            inputs = Command(resume={"decisions": decisions})
