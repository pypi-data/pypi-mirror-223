import argparse
from .login import login, logout, whoami
import openi.dataset as dataset
from .settings import *
import textwrap


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=CLI.usage,
        description=CLI.banner,
    )
    parser._action_groups.pop()
    subparsers = parser.add_subparsers(title="commands", dest="commands")
    subparsers.required = False
    # subparsers.choices = Help.openi_choices
    parse_login(subparsers)
    parse_logout(subparsers)
    parse_whoami(subparsers)
    parse_dataset(subparsers)
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    command_args = {}
    command_args.update(vars(args))
    del command_args["func"]
    del command_args["commands"]
    error = False
    try:
        out = args.func(**command_args)
    except Exception as e:
        print(e)
        out = None
        error = True
    except ValueError as e:
        print(e)
        out = None
        error = True
    except KeyboardInterrupt:
        print("User cancelled operation")
        out = None
    if out is not None:
        print(out, end="")

    # This is so that scripts that pick up on error codes can tell when there was a failure
    if error:
        exit(1)


def parse_login(subparsers):
    parse_login = subparsers.add_parser(
        "login",
        description=CLI.command_login,
        usage=CLI.login_usage,
        help=CLI.command_login,
    )
    parse_login.add_argument(
        "-e",  # '--endpoint',
        dest="endpoint",
        default=API.ENDPOINT,
        required=False,
        help=CLI.param_endpoint,
    )
    parse_login.add_argument(
        "-t",  # '--token',
        dest="token",
        default=None,
        required=False,
        help=CLI.param_token,
    )
    parse_login.set_defaults(func=login)


def parse_logout(subparsers):
    parse_logout = subparsers.add_parser(
        "logout",
        description=CLI.command_logout,
        usage="openi logout [-h]",
        help=CLI.command_logout,
    )
    parse_logout.set_defaults(func=logout)


def parse_whoami(subparsers):
    parse_whoami = subparsers.add_parser(
        "whoami",
        description=CLI.command_whoami,
        usage="openi whoami [-h]",
        help=CLI.command_whoami,
    )
    parse_whoami.set_defaults(func=whoami)


def parse_dataset(subparsers):
    parser_dataset = subparsers.add_parser(
        "dataset", usage=CLI.dataset_usage, help=CLI.command_dataset, aliases=["d"]
    )
    parser_dataset._action_groups.pop()
    subparsers_dataset = parser_dataset.add_subparsers(
        title="commands", dest="commands"
    )
    subparsers_dataset.required = True

    # dataset upload
    parser_dataset_upload = subparsers_dataset.add_parser(
        "upload",
        description=CLI.command_dataset_upload,
        usage=CLI.dataset_upload_usage,
        help=CLI.dataset_upload_help,
        # epilog=CLI.dataset_upload_epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_dataset_upload._action_groups.pop()
    parser_dataset_upload_args = parser_dataset_upload.add_argument_group("arguments")
    parser_dataset_upload_args.add_argument(
        "-f", dest="file", required=True, help=CLI.dataset_upload_param_file
    )
    parser_dataset_upload_args.add_argument(
        "-r", dest="repo_id", required=True, help=CLI.dataset_upload_param_repo_id
    )
    parser_dataset_upload_args.add_argument(
        "-c",
        dest="cluster",
        required=False,
        default="NPU",
        choices=["gpu", "npu"],
        help=CLI.dataset_upload_param_cluster,
    )
    parser_dataset_upload.set_defaults(func=dataset.upload_file)

    # dataset download
    parser_dataset_download = subparsers_dataset.add_parser(
        "download",
        description=CLI.command_dataset_download,
        usage=CLI.dataset_download_usage,
        help=CLI.dataset_download_help,
        # epilog = CLI.dataset_download_epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_dataset_download._action_groups.pop()
    parser_dataset_download_args = parser_dataset_download.add_argument_group(
        "arguments"
    )
    parser_dataset_download_args.add_argument(
        "-f", dest="file", required=True, help=CLI.dataset_download_param_file
    )
    parser_dataset_download_args.add_argument(
        "-r", dest="repo_id", required=True, help=CLI.dataset_upload_param_repo_id
    )
    parser_dataset_download_args.add_argument(
        "-c",  #'--cluster',
        dest="cluster",
        required=False,
        default="NPU",
        choices=["gpu", "npu"],
        help=CLI.dataset_upload_param_cluster,
    )
    parser_dataset_download_args.add_argument(
        "-p",  #'--save_path',
        dest="save_path",
        required=False,
        default=PATH.SAVE_PATH,
        help=CLI.dataset_download_param_save_path,
    )
    parser_dataset_download.set_defaults(func=dataset.download_file)
