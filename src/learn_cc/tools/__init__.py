from pathlib import Path

# 共享变量 - 先定义，避免循环引用
WORKDIR = Path.cwd()

# 然后导入其他模块
from .bash import run_bash

__all__ = ["run_bash", "WORKDIR"]
