[![Supported Versions](https://img.shields.io/pypi/pyversions/leek.svg)](https://pypi.org/project/leek)
### 常用装饰器工具集
                  
#### pip安装
```shell
pip install detool
```

#### 1.统计函数执行时长装饰器
```python
import time
from detool import timer_cost

@timer_cost
def t_time():
    time.sleep(0.01)
    print(123)
```

#### 2.redis缓存装饰器
```python
    from detool import RedisCache
    
    redis_cache = RedisCache(host='127.0.0.1', password='', port=6379, db=0)
    
    @redis_cache.cache(ttl=30)
    def sum_t(a, b):
        print(f'{a}+{b}={a + b}')
        return a + b

    r = sum_t(1, 2)
    print(r)
```
#### 3.日志装饰器
```python
    from detool import class_log_decorator,log_decorator
    
    @class_log_decorator
    class Cal(object):
        def __init__(self, c):
            self.c = c

        def sum(self, a, b):
            return a + b
    @log_decorator
    def calculate(a, b):
        return a + b

    Cal(3).sum(a=3, b=6)
```

#### 4.异常捕获装饰器
```python
    from detool import class_exception_decorator,exception_decorator

    @exception_decorator
    def r_exception():
        raise Exception("function Exception raised")


    @class_exception_decorator
    class ClassException(object):
        def r_exception(self):
            raise Exception("class Exception raised")


    r_exception()
    ClassException().r_exception()
```

#### 5.分析内装饰器
```python
    from detool import profile

    @profile
    def t_memory():
        return [i for i in range(1, 1001)]
    
    t_memory()
```
