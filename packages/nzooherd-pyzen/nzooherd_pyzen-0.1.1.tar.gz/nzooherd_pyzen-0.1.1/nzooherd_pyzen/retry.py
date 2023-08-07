# -*- coding: utf-8 -*-
# @Time    : 07/08/2023
# @Author  : nzooherd
# @File    : retry.py 
# @Software: PyCharm
# -*- coding: utf-8 -*-
import functools
import time
from datetime import timedelta
from typing import Optional, Callable


def retry(func: Optional[Callable] = None, duration: timedelta = timedelta(seconds=2), limit: int = 10) -> Callable:
    """

    :param func:
    :type func:
    :param duration:
    :type duration:
    :param limit:
    :type limit:
    :return:
    :rtype:
    """
    if not func:
        return functools.partial(retry, duration=duration, limit=limit)

    @functools.wraps(func)
    def _func(*args, **kwargs):
        duration_seconds = duration.total_seconds()
        count = 1
        while count <= limit:
            try:
                result = func(*args, **kwargs)
                return result
            except:
                count += 1
                time.sleep(duration_seconds)
                continue

    return _func
