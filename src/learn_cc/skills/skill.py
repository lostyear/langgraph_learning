from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field


class AgentSkillMeta(BaseModel):
    Name: str = Field(..., description="Skill Name")
    Description: str = Field(..., description="Skill Description")
    Markdown: Path = Field(..., description="SKILL.md path of the skill")

    def load(self) -> Optional["AgentSkill"]:
        body = self.Markdown.read_text(encoding="utf-8")
        resources = []
        for folder in ("scripts", "references", "assets"):
            fp = self.Markdown.parent / folder
            files = ",".join(f.name for f in fp.glob("*"))
            if files:
                resources.append(f"{folder}: {files}")

        skill = AgentSkill(
            Name=self.Name,
            Description=self.Description,
            Markdown=self.Markdown,
            Body=body,
            DirPath=self.Markdown.parent,
            Resources=resources,
        )
        return skill


class AgentSkill(AgentSkillMeta):
    Body: str = Field(..., description="Content of SKILL.md")
    DirPath: Path = Field(..., description="Dir path of the skill")
    Resources: List[str] = Field(..., description="Other Resources of the Skill")

    def get_description(self) -> str:
        return f"""<skill-loaded name="{self.Name}">
        {self.Body}

        {self.resource_description()}
        </skill-loaded>"""

    def resource_description(self) -> str:
        if not self.Resources:
            return ""
        return f"""**Available resources:
        {"\n".join(f"- {r}" for r in self.Resources)}
        """

    # def load_resources(self) -> List[str]:
    #     resources = []
    #     for folder in "scripts":
    #         fp = self.Path / folder
    #         files = ",".join(f.name for f in fp.glob("*"))
    #         if files:
    #             resources.append(f"{folder}: {files}")
    #     return resources
