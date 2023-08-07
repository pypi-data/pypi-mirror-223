# -*- coding: utf-8 -*-
# @Time    : 07/08/2023
# @Author  : nzooherd
# @File    : limit.py 
# @Software: PyCharm
# -*- coding: utf-8 -*-
import functools
import time
from datetime import datetime, timedelta
from typing import Optional, Callable


def frequency_limit(func: Optional[Callable] = None,
                    duration: timedelta = None,
                    limit: int = 0) -> Callable:
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
        return functools.partial(frequency_limit, duration=duration, limit=limit)

    if not duration:
        raise NotImplementedError

    period_first_call_time, count = None, 0

    @functools.wraps(func)
    def _func(*args, **kwargs):
        nonlocal period_first_call_time, count

        duration_seconds = duration.total_seconds()
        cur_time = int(datetime.timestamp(datetime.now()))

        if period_first_call_time is not None and cur_time < (
                period_first_call_time + duration_seconds) and count >= limit:
            time.sleep(duration_seconds + period_first_call_time - cur_time + 1)
            count = 0
            period_first_call_time = int(datetime.timestamp(datetime.now()))

        result = func(*args, **kwargs)
        count += 1
        return result

    return _func
