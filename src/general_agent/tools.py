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


def create_retrieve_tool(retriever: VectorStoreRetriever) -> BaseTool:
    @tool
    def retrieve(query: str) -> str:
        """Search and return information about gorm cli."""
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs])

    return retrieve
