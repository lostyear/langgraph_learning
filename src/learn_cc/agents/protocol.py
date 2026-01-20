from typing import Any, Dict, Protocol


class AsyncAgent(Protocol):
    async def ainvoke(self, prompt: str) -> Dict[str, Any] | Any: ...
