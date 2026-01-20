from typing import List
from langchain.tools import tool, BaseTool
from langchain_core.vectorstores import VectorStoreRetriever


@tool
def get_location() -> str:
    """Get the user's location."""
    import random

    return random.choice(("北京", "上海", "石家庄"))


@tool
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny. wind 10km/h North; temperature: 3°C"


def math_tools() -> List[BaseTool]:
    @tool
    def add(x: int, y: int) -> int:
        """
        add 用来计算两数之和

        返回 x+y
        """
        return x + y

    @tool
    def sub(x: int, y: int) -> int:
        """
        add 用来计算两数之差

        返回 x-y
        """
        return x - y

    @tool
    def mul(x, y: int) -> int:
        """
        add 用来计算两数之积

        返回 x*y
        """
        return x * y

    @tool
    def div(x, y: int) -> int:
        """
        add 用来计算除法

        返回 x/y
        """
        return x / y

    return [add, sub, mul, div]


def create_retrieve_tool(retriever: VectorStoreRetriever) -> BaseTool:
    @tool
    def retrieve(query: str) -> str:
        """Search and return information about gorm cli."""
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs])

    return retrieve
