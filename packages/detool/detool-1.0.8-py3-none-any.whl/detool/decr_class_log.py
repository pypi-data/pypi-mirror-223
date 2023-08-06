#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/6/20 18:13
# @Author  : abo123456789
# @Desc    : decors.py
import functools
from loguru import logger as logger


def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"【{func.__name__}】 method params:  {kwargs}, {args}")
        result = func(*args, **kwargs)
        if result and isinstance(result, dict) and result.get('code') == 500:
            logger.error(f"【{func.__name__}】 method result: {result}")
        else:
            logger.info(f"【{func.__name__}】 method result: {result}")
        return result

    return wrapper


def class_log_decorator(cls):
    for name, value in vars(cls).items():
        if callable(value) and name not in ['__init__']:
            setattr(cls, name, log_decorator(value))
    return cls


if __name__ == '__main__':
    @class_log_decorator
    class Cal(object):
        def __init__(self, c):
            self.c = c

        def sum(self, a, b):
            return a + b


    Cal(3).sum(a=3, b=6)


    @log_decorator
    def calculate(a, b):
        return a + b


    calculate(3, 5)
