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
    from langchain.tools import tool
    from langchain.messages import HumanMessage
    from .dataclass import AgentInvokeInput

    @tool
    def get_weather(location: str) -> str:
        """Get the weather for a location."""
        return (
            f"The weather in {location} is sunny. wind 10km/h North; temperature: 3°C"
        )

    agent = create_agent(
        model="deepseek-chat",
        tools=[get_weather],
        system_prompt="You are a helpful assistant by lostyear.",
    )

    input = AgentInvokeInput(messages=[HumanMessage("北京现在的温度是多少？")])

    # invoke 里面要包装一层 cast(None, xxx) 因为不用case这里类型检查过不去
    result = agent.invoke(cast(None, input))
    print(result)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    # create_agent()
    # structured_output()
    # structured_list_output()
    with_tool_agent()
