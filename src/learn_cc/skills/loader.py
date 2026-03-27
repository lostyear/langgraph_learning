from pathlib import Path
from typing import Dict, List, Optional

from .skill import AgentSkill, AgentSkillMeta


# NOTE: 注意！！！ SKILL 应该每次对话都重新load，这样可以保证能获取到最新的SKILL内容
class SkillsLoader:
    def __init__(self, dir: Path) -> None:
        self.dir = None
        self.skills: Dict[str, AgentSkillMeta] = {}
        if dir.exists():
            self.dir = dir
            self.load_metas()

    def skill_metas(self) -> Dict[str, AgentSkillMeta]:
        return self.skills

    def skill_meta_desp(self) -> str:
        if not self.skills:
            return "No Available Skills!!!"
        return f"""
        Available Skills:
        {"\n\n".join(f"- name: {name}\n  description: {meta.Description}" for name, meta in self.skills.items())}
        """

    def load_metas(self) -> Dict[str, AgentSkillMeta]:
        skills = {}
        if not self.dir:
            return skills

        for item in self.dir.iterdir():
            if not item.is_dir():
                # skills 需要用文件夹的形式提供
                continue
            # 这里看看要不要支持大小写不敏感的读取
            md = item / "SKILL.md"
            meta = self.load_md_meta(md)
            if not meta:
                continue
            skills[item.name] = meta
        self.skills = skills
        return skills

    def load_md_meta(self, path: Path) -> Optional[AgentSkillMeta]:
        from markdown import Markdown
        from markdown.extensions.meta import MetaExtension

        if not path.exists():
            return None
        if not path.is_file():
            return None

        # load markdown file
        text = path.read_text(encoding="utf-8")
        md = Markdown(extensions=[MetaExtension()])
        md.convert(text)

        # get metadata
        meta: Dict = md.Meta  # type: ignore
        name = meta.get("name", [])
        desp = meta.get("description", [])

        if not name or not desp:
            return None
        return AgentSkillMeta(Name=name[0], Description=desp[0], Markdown=path)

    def get_skill_content(self, name: str) -> str:
        meta = self.skills.get(name)
        if not meta:
            return f"Unknown Skill: {name}\n{self.skill_meta_desp()} "
        skill = meta.load()
        if not skill:
            return f"Load Skill {name} failed!"
        return skill.get_description()


if __name__ == "__main__":
    text = """---
name: test md
description: used to test markdown parser

---

# md title
md content

"""
    from markdown import Markdown
    from markdown.extensions import meta

    ext = meta.MetaExtension()

    converter = Markdown(extensions=[ext])
    html = converter.convert(text)
    print("---------------")
    print(converter.Meta)  # type: ignore
    print("---------------")
    print(html)
    print("---------------")
