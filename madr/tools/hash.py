import re

import bcrypt

from madr.infra import config


def hash_pwd(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode(), config.AUTH_SALT.encode()).decode()


def check_pwd(pwd: str, hashed_pwd: str) -> bool:
    return bcrypt.checkpw(pwd.encode(), hashed_pwd.encode())


def is_hashed_pwd(pwd: str):
    pattern = r'^\$2[aby]?\$[0-9]{2}\$.{53}$'
    return bool(re.match(pattern, pwd))
