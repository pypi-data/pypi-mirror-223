import argparse


def main(args):
    print("--address {}".format(args.code_address))  # args.address会报错，因为指定了dest的值
    print("--flag {}".format(args.flag))  # 如果命令行中该参数输入的值不在choices列表中，则报错
    print("--port {}".format(args.port))  # prot的类型为int类型，如果命令行中没有输入该选项则报错
    print(
        "-l {}".format(args.log)
    )  # 如果命令行中输入该参数，则该值为True。因为为短格式"-l"指定了别名"--log"，所以程序中用args.log来访问


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument(
        "--address", default=80, help="the port number.", dest="code_address"
    )

    args = parser.parse_args()
    main(args)
