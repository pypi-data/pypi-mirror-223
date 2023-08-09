# coding: utf-8
"""
@File    :   1.py
@Time    :   2023/08/02 11:38:39
@Author  :   lijc210@163.com
@Desc    :   None
python3 src/package/click_test/invoke.py
"""
import click


cli = click.Group()


@cli.command()
@click.option("--count", default=1)
def test(count):
    click.echo("Count: %d" % count)


@cli.command()
@click.option("--count", default=1)
@click.pass_context
def dist(ctx, count):
    ctx.forward(test, count=42)
    ctx.invoke(test, count=42)


if __name__ == "__main__":
    cli()
