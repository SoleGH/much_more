<!-- TOC -->

- [上下文操作](#上下文操作)
- [md5 加密字符串](#md5-加密字符串)
- [变量赋值封装](#变量赋值封装)

<!-- /TOC -->
### 上下文操作
```python
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
```

### md5 加密字符串
```python
import hashlib

def my_md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


if __name__ == "__main__":
    print(my_md5("test md5"))
```

### 变量赋值封装
* 示例,test未返回值,但传入参数`dict_`已经赋值完成.

```python
def test(dict_, value):
    dict_[str(value)] = value


if __name__ == '__main__':
    my_dict = {}
    for i in range(5):
        test(my_dict, i)
        print("current my_dict:{}".format(my_dict))
    print(my_dict)
# 输出
"""
current my_dict:{'0': 0}
current my_dict:{'1': 1, '0': 0}
current my_dict:{'2': 2, '1': 1, '0': 0}
current my_dict:{'2': 2, '3': 3, '1': 1, '0': 0}
current my_dict:{'4': 4, '2': 2, '3': 3, '1': 1, '0': 0}
{'4': 4, '2': 2, '3': 3, '1': 1, '0': 0}
"""
```
