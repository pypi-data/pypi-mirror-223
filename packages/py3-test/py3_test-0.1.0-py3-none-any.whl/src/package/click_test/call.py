# coding: utf-8
"""
@File    :   1.py
@Time    :   2023/08/02 11:38:39
@Author  :   lijc210@163.com
@Desc    :   None
python3 src/package/click_test/call.py
"""
import click


def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")


@click.command()
# @click.argument("name")
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello_click(count, name):
    hello(count, name)


if __name__ == "__main__":
    hello(1, "aaaa")
    hello_click()
