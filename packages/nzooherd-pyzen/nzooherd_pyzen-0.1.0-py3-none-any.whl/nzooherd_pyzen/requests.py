# -*- coding: utf-8 -*-
# @Time    : 07/08/2023
# @Author  : nzooherd
# @File    : requests.py 
# @Software: PyCharm
# -*- coding: utf-8 -*-
from typing import Dict


def format_cookies(cookies: str) -> Dict[str, str]:
    return {item[0]: item[1] for item in map(lambda cookie_str: cookie_str.rstrip().split("="), cookies.split(";"))}
