# -*- coding: utf-8 -*-
# @Time    : 2023/8/7 21:48
# @Author  : abo123456789
# @Desc    : 异常捕获装饰器
import functools
import traceback

from loguru import logger


def exception_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except(Exception,):
            logger.error(f'{func.__name__} error')
            logger.error(traceback.format_exc())
            return {'code': 500, 'msg': traceback.format_exc(), 'result': None}

    return wrapper


def class_exception_decorator(cls):
    for name, value in vars(cls).items():
        if callable(value) and name not in ["__init__"]:
            setattr(cls, name, exception_decorator(value))
    return cls


if __name__ == '__main__':
    @exception_decorator
    def r_exception():
        raise Exception("function Exception raised")


    @class_exception_decorator
    class ClassException(object):
        def r_exception(self):
            raise Exception("class Exception raised")


    r_exception()
    ClassException().r_exception()
