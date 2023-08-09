# coding: utf-8
"""
@File    :   1.py
@Time    :   2023/08/02 11:38:39
@Author  :   lijc210@163.com
@Desc    :   None
python3 src/package/click_test/pass_context.py
"""
import click


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    # 确保 ctx.obj 存在并且是个 dict。 (以防 `cli()` 指定 obj 为其他类型
    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug


@cli.command()
@click.pass_context
def sync(ctx):
    click.echo("Debug is %s" % (ctx.obj["DEBUG"] and "on" or "off"))


if __name__ == "__main__":
    cli(obj={})
