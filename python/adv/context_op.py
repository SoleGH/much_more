# utf-8
from contextlib import contextmanager

"""
上下文操作,执行步骤:(等同于 实现__enter__和__exit__ 方法)
1. 先执行 yield 之前的代码
2. 执行 with get_something(1) as a: 代码块中的代码,
3. 执行yield 后的代码
注:如果with get_something(1) as a:中出现异常则会被 get_something 中的try捕获
"""

@contextmanager
def get_something(a):
    print('start')
    try:
        a += 1
        yield a
        print('end')
    except Exception as e:
        print('get_something:{}'.format(e))


if __name__ == '__main__':
    with get_something(1) as a:
        print('main:{}'.format(a))
        # raise Exception('nothing happened')