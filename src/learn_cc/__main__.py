from typing import NamedTuple

from click import echo, group, help_option, option, pass_context, version_option
from click import Context

from .agents import AsyncAgent


class CliOptions(NamedTuple):
    debug: bool
    model: str
    system_prompt: str


global cliOptions


@group("cc")
@help_option("--help", "-h")
@version_option("0.0.1", "--version", "-v", package_name="learn claude code")
@option(
    "--debug", "-d", is_flag=True, required=False, default=False, help="开启调试日志"
)
@option("--model", "-m", required=False, default="deepseek-chat", help="选择模型")
@option(
    "--system",
    required=False,
    default="You are a helpful assistant by lostyear.",
    help="系统提示词",
)
# @option("--prompt", "-p", required=True, help="提示词的内容")
def cli(
    debug: bool,
    model: str,
    system: str,
    # prompt: str,
):
    global cliOptions
    echo("start command...")
    echo(f"system prompt is {system}")
    # echo(f"user prompt is {prompt}")

    cliOptions = CliOptions(debug, model, system)
    echo(f"now options is: {cliOptions}")


@cli.command("bash")
@pass_context
def v0_bash(ctx: Context):
    from .agents import BashAgent

    echo(ctx)
    echo("agent with bash")

    agent = BashAgent(
        cliOptions.model, cliOptions.system_prompt, debug=cliOptions.debug
    )
    run_agent_loop(agent)


def run_agent_loop(agent: AsyncAgent):
    from asyncio import run

    while True:
        try:
            user_input = input("You want to do:\n").strip()
        except (EOFError, InterruptedError):
            break
        if not user_input:
            continue
        if user_input in ("exit", "quit", "q"):
            break
        try:
            r = run(agent.ainvoke(user_input))
            # print(r)
        except Exception as e:
            print(f"run agent invoke got error: {e}")
    echo("user stop, exiting...")


if __name__ == "__main__":
    cli()
