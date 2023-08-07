import os
import json
from getpass import getpass
from pathlib import Path
from openi.apis import OpeniAPI
from .settings import *
from openi.utils.file_utils import get_token
from openi.utils import logger
import logging

logger.setup_logger()


def login(token: str = None, endpoint: str = API.ENDPOINT) -> None:
    print(
        """\n
             ██████╗   ██████╗  ███████╗  ███╗   ██╗  ██████╗
            ██╔═══██╗  ██╔══██╗ ██╔════╝  ████╗  ██║    ██╔═╝
            ██║   ██║  ██████╔╝ █████╗    ██╔██╗ ██║    ██║
            ██║   ██║  ██╔═══╝  ██╔══╝    ██║╚██╗██║    ██║
            ╚██████╔╝  ██║      ███████╗  ██║ ╚████║  ██████╗
             ╚═════╝   ╚═╝      ╚══════╝  ╚═╝  ╚═══╝  ╚═════╝\n
         """
    )
    endpoint = endpoint[:-1] if endpoint[-1] == "/" else endpoint

    if token is None:
        print(f"点击链接获取令牌并复制粘贴到下列输入栏 {endpoint}/user/settings/applications \n")
        print(
            f"[WARNING] 若本机已存在登录令牌，本次输入的令牌会将其覆盖 \n"
            "          若粘贴时切换了本窗口，请先按 退格键⇦ 删除多余空格\n"
        )
        token = getpass(prompt="  🔒 token: ")
    _login(token=token, endpoint=endpoint)


def _login(token: str, endpoint: str) -> None:
    try:
        api = OpeniAPI(endpoint, token)
        valid_user = api.login_check()

        if not os.path.exists(PATH.OPENI_FOLDER):
            os.mkdir(PATH.OPENI_FOLDER)
        Path(PATH.TOKEN_PATH).write_text(
            json.dumps({"endpoint": endpoint, "token": token, "username": valid_user})
        )
        msg = (
            f"\n  Your token was saved to `{PATH.TOKEN_PATH}`\n"
            f"  Successfully logged in as `{valid_user}` @{endpoint}!\n"
        )
        logging.info(msg)
        print(msg)
    except:
        raise ValueError("\n  ❌ login failed: invalid token or endpoint!\n")


def whoami() -> None:
    try:
        api = OpeniAPI()
        valid_user = api.login_check()
        msg = f"\n`{valid_user}` @{api.baseURL}\n"
        logging.info(msg)
        print(msg)
    except:
        msg = f"\nCurrently not logged in.\n"
        logging.info(msg)
        print(msg)


def logout() -> None:
    try:
        valid_user = get_token()["username"]
        os.remove(PATH.TOKEN_PATH)
        msg = f"\n`{valid_user}` successfully logged out.\n"
        logging.info(msg)
        print(msg)
    except:
        msg = "\nCurrently not logged in.\n"
        logging.info(msg)
        print(msg)
