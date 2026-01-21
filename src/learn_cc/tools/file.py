from typing import Optional
from pathlib import Path
from langchain.tools import tool

from . import WORKDIR


def safe_path(p: str) -> Path:
    """Ensure path stays within workspace."""
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path


@tool
def read_file(path: str, limit: int = 300) -> str:
    """Read file contents."""
    try:
        text = safe_path(path).read_text()
        lines = text.splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(text.splitlines()) - limit} more)"]
        return "\n".join(lines)[:50000]
    except Exception as e:
        return f"Error: {e}"


@tool
def write_file(path: str, content: str) -> str:
    """
    Write content to file, creating parent directories if needed.

    This is for complete file creation/overwrite.
    For partial edits, use edit_file instead.
    """
    try:
        fp = safe_path(path)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} bytes to {path}"

    except Exception as e:
        return f"Error: {e}"


@tool
def edit_file(path: str, old_text: str, new_text: str) -> str:
    """
    Replace exact text in a file (surgical edit).

    Uses exact string matching - the old_text must appear verbatim.
    Only replaces the first occurrence to prevent accidental mass changes.
    """
    try:
        fp = safe_path(path)
        content = fp.read_text()

        if old_text not in content:
            return f"Error: Text not found in {path}"

        # Replace only first occurrence for safety
        new_content = content.replace(old_text, new_text, 1)
        fp.write_text(new_content)
        return f"Edited {path}"

    except Exception as e:
        return f"Error: {e}"


@tool
def list_files(pattern: str, limit: int = 100) -> str:
    """
    list files by pattern.

    Args:
    pattern: file match glob pattern, example: "**/*.py"
    limit: max files output
    """
    files = WORKDIR.glob(pattern=pattern)
    l = [str(f) for f in files]
    if len(l) > limit:
        l = l[:limit]
    return "\n".join(l)
