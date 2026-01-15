def show_path():
    import sys

    for path in sys.path:
        print(path)


def chat_deepseek():
    from langchain_deepseek import ChatDeepSeek

    model = ChatDeepSeek(model="deepseek-chat")
    result = model.invoke(
        [
            ("system", "You are a helpful assistant by lostyear."),
            # ("user", "What is the capital of France?"),
            ("user", "Who are you?"),
        ]
    )
    print(result.content)


def chat_deepseek_reasoner():
    from langchain_deepseek import ChatDeepSeek

    model = ChatDeepSeek(model="deepseek-reasoner")
    result = model.invoke(
        [
            ("system", "You are a helpful assistant by lostyear."),
            # ("user", "What is the capital of France?"),
            ("user", "Who are you?"),
        ]
    )
    print(result)


def init_chat_model():
    from langchain.chat_models import init_chat_model

    model = init_chat_model(model="deepseek-chat")
    result = model.invoke(
        [
            ("system", "You are a helpful assistant by lostyear."),
            # ("user", "What is the capital of France?"),
            ("user", "Who are you?"),
        ]
    )
    print(result.content)


def create_agent():
    from typing import cast
    from langchain.agents import create_agent

    agent = create_agent(
        model="deepseek-chat",
        tools=[],
        system_prompt="You are a helpful assistant by lostyear.",
    )
    result = agent.invoke(cast(None, {"messages": [("user", "Who are you?")]}))
    print(result)


def create_structured_type():
    from dataclasses import dataclass

    @dataclass
    class Introduce:
        """自我介绍"""

        # 名字
        name: str
        # 自我描述
        description: str

    return Introduce


def structured_output():
    from typing import cast
    from langchain.agents import create_agent
    from langchain.agents.structured_output import ToolStrategy

    agent = create_agent(
        model="deepseek-chat",
        tools=[],
        system_prompt="You are a helpful assistant by lostyear.",
        response_format=ToolStrategy(create_structured_type()),
    )
    result = agent.invoke(cast(None, {"messages": [("user", "Who are you?")]}))
    print(result)


def structured_list_output():
    from typing import cast
    from dataclasses import dataclass

    from langchain.agents import create_agent
    from langchain.agents.structured_output import ToolStrategy

    @dataclass
    class City:
        """城市信息"""

        # 城市名称
        name: str
        # 城市介绍
        description: str

    @dataclass
    class CityList:
        from typing import List

        """
        CityList 城市列表
        """

        # 城市列表数据
        data: List[City]

    agent = create_agent(
        model="deepseek-chat",
        tools=[],
        system_prompt="You are a helpful assistant by lostyear.",
        response_format=ToolStrategy(CityList),
    )
    result = agent.invoke(
        cast(None, {"messages": [("user", "中国人口最多的三个城市？")]})
    )
    print(result)


def with_tool_agent():
    from typing import cast
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage
    from .dataclass import AgentInvokeInput
    from .tools import get_weather

    agent = create_agent(
        model="deepseek-chat",
        tools=[get_weather],
        system_prompt="You are a helpful assistant by lostyear.",
    )

    input = AgentInvokeInput(messages=[HumanMessage("北京现在的温度是多少？")])

    # invoke 里面要包装一层 cast(None, xxx) 因为不用case这里类型检查过不去
    result = agent.invoke(cast(None, input))
    print(result)


def with_chat_history():
    from typing import cast
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage
    from langgraph.checkpoint.memory import InMemorySaver
    from langchain_core.runnables import RunnableConfig
    from .dataclass import AgentInvokeInput
    from .tools import get_weather, get_location

    agent = create_agent(
        model="deepseek-chat",
        tools=[get_location, get_weather],
        system_prompt="You are a helpful assistant by lostyear.",
        # 记忆保存, 这个参数要跟别的配置搭配使用，比如thread_id
        checkpointer=InMemorySaver(),
    )

    # 配置 thread_id 可以标识相同的对话，找到对话历史
    cfg = RunnableConfig(configurable={"thread_id": "test_agent"})

    input = AgentInvokeInput(messages=[HumanMessage("根据天气给我一些出门的建议。")])
    result = agent.invoke(cast(None, input), config=cfg)
    print("round 1: ", result)

    input = AgentInvokeInput(messages=[HumanMessage("我穿什么衣服出门合适？")])
    result = agent.invoke(cast(None, input), config=cfg)
    print("round 2: ", result)


def with_rag():
    from typing import cast
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage

    from .dataclass import AgentInvokeInput
    from .tools import create_retrieve_tool
    from .loader import load_rag

    # 创建rag工具
    rag_tool = create_retrieve_tool(load_rag())
    # rag_res = rag_tool.invoke("gorm cli的用法")
    # print("rag result: ", rag_res)

    agent = create_agent(
        model="deepseek-chat",
        tools=[rag_tool],
        system_prompt="You are a helpful assistant by lostyear.",
    )

    result = agent.invoke(
        input=cast(
            None,
            AgentInvokeInput(messages=[HumanMessage("gorm cli工具怎么使用？")]),
        )
    )
    for msg in result.get("messages", []):
        msg.pretty_print()


async def run_with_rag_async():
    from typing import cast
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage

    from .dataclass import AgentInvokeInput
    from .tools import create_retrieve_tool
    from .loader import load_rag

    # 创建rag工具
    rag_tool = create_retrieve_tool(load_rag())
    # rag_res = rag_tool.invoke("gorm cli的用法")
    # print("rag result: ", rag_res)

    agent = create_agent(
        model="deepseek-chat",
        tools=[rag_tool],
        system_prompt="You are a helpful assistant by lostyear.",
    )

    result = await agent.ainvoke(
        input=cast(
            None,
            AgentInvokeInput(messages=[HumanMessage("gorm cli工具怎么使用？")]),
        )
    )
    for msg in result.get("messages", []):
        msg.pretty_print()


if __name__ == "__main__":
    from dotenv import load_dotenv
    from asyncio import run

    load_dotenv()
    chat_deepseek_reasoner()
    # create_agent()
    # structured_output()
    # structured_list_output()
    # with_tool_agent()
    # with_chat_history()
    # with_rag()
    # run(run_with_rag_async())
