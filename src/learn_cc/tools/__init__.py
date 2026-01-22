from pathlib import Path

# 共享变量 - 先定义，避免循环引用
WORKDIR = Path.cwd()

# 然后导入其他模块
from .bash import run_bash
from .file import read_file, write_file, edit_file, list_files
from .todo import new_todo_tool

__all__ = [
    "WORKDIR",
    "run_bash",
    "read_file",
    "write_file",
    "edit_file",
    "list_files",
    "new_todo_tool",
]
