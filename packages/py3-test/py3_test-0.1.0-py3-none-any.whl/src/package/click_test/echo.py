# coding: utf-8
"""
@File    :   1.py
@Time    :   2023/08/02 11:38:39
@Author  :   lijc210@163.com
@Desc    :   None
python3 src/package/click_test/1.py --count=3
python3 src/package/click_test/1.py --help
"""
import click


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def echo(count, name):
    """获取返回值"""
    return click.echo(name)


if __name__ == "__main__":
    echo()
