from typing import List, Literal
from pydantic import BaseModel, Field
from langchain.tools import tool, BaseTool


class TodoItem(BaseModel):
    content: str = Field(..., description="item content string")
    status: Literal["pending", "completed", "in_progress"] = Field(
        default="pending", description="item is done or not"
    )
    activeForm: str = Field(..., description="now doing things")


class TodoManager(BaseModel):
    items: List[TodoItem] = Field(
        ..., description="list of todo items, only one item can be in progress"
    )

    def validate(self, list: List[TodoItem]):
        if len(list) > 20:
            raise ValueError("list items should less than 20")

        activeCnt = 0
        for item in list:
            if item.status == "in_progress":
                activeCnt += 1

        if activeCnt > 1:
            raise ValueError("more than one item is in progress")

    def render(self) -> str:
        if not self.items:
            return "no items in todo list"
        lines: List[str] = []
        doneCnt = 0
        for item in self.items:
            if item.status == "completed":
                doneCnt += 1
            lines.append(
                f"[{"*" if item.status == "completed" else " " if item.status == "pending" else ">"}]"
                f" {item.content}"
                f"{f" <- {item.activeForm}" if item.status == "in_progress" else ""}"
            )
        lines.append(f"\n({doneCnt}/{len(self.items)} has been done)")

        return "\n".join(lines)

    def update(self, new: List[TodoItem]) -> str:
        try:
            self.validate(new)
        except Exception as e:
            return "Error: {e}"
        self.items = new
        return self.render()


def new_todo_tool() -> BaseTool:
    manager = TodoManager(items=[])

    @tool
    def update_todo(items: List[TodoItem]) -> str:
        """
        use todo list to tracking works.

        should use complete list to replace exits items
        will return the new items
        """
        return manager.update(items)

    return update_todo
