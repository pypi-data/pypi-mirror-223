# coding: utf-8
"""
@File    :   1.py
@Time    :   2023/08/02 11:38:39
@Author  :   lijc210@163.com
@Desc    :   None
python3 src/package/click_test/group_add.py --help
python3 src/package/click_test/group_add.py get-user -u 123
python3 src/package/click_test/group_add.py add-user -u 123 -p "1234qwer"
"""
import click


@click.group()
def main():
    pass


@click.command()
@click.option("-u", "--user_name", type=str, help="add user_name")
def get_user(user_name):
    click.echo(f"search user:{user_name}")


@click.command()
@click.option("-u", "--user_name", required=True, type=str, help="要添加的用户名")
@click.option("-p", "--password", required=True, type=str, help="要添加的密码")
@click.option(
    "-t",
    "--id_type",
    required=True,
    default="phone",
    type=str,
    help="添加的账户类型",
    show_default=True,
)
def add_user(user_name, password, id_type):
    # do something.....
    click.echo(f"{user_name=}  {password=} {id_type=}")


main.add_command(get_user)
main.add_command(add_user)

if __name__ == "__main__":
    main()
