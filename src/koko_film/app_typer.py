"""
=========================================================================
@File Name: app_typer.py
@Time: 2025/6/28 13:26
@Program IDE: PyCharm
@Create by Author: 一一风和橘
@Motto: "The trick, William Potter, is not minding that it hurts."
@Description:
- 
- 
=========================================================================
"""
import typer
from raf_tools.raf_archive import raf_archive

app = typer.Typer()


@app.command()
def arch(path: str = typer.Argument(None)):
    raf_archive(path)


@app.command()
def push(path: str = typer.Argument(None)):
    if path == "all" or path is None:
        pass
    else:
        typer.echo(f"Hello, {path}!")


@app.command()
def greet(name: str, age: int = 18):
    typer.echo(f"你好，{name}！今年{age}岁啦！")


@app.command()
def add(a: int, b: int):
    result = a + b
    typer.echo(f"{a} + {b} = {result}")


if __name__ == "__main__":
    app()
