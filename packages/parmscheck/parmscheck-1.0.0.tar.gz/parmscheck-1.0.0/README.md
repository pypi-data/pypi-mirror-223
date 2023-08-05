# parmscheck

#### 介绍
支持python函数类型检查的装饰器，提供了一种方便的方式来对函数的参数进行运行时类型检查。通过使用这个装饰器，开发者可以轻松确保函数的输入参数是否为预期的类型。
#### 特点

- 简单易用：只需要在函数上应用一个装饰器，即可对任何函数进行类型检查。无需复杂的配置或额外的代码。
- 支持类型注解：装饰器与Python的类型注解完美结合。开发者可以简单地为函数的参数添加类型注解，装饰器会在运行时自动验证参数的类型。


#### 安装教程

你可以使用Python包管理工具pip来安装这个装饰器库：
`pip install parmscheck`


#### 使用说明


```
from parmscheck import check_args,check_args_for_class

T = TypeVar('T', int, float, Dict[int, str])
P = TypeVar('P')
@check_args
def multiply(a: List[int], b: T) -> int:
    return a * b

result = multiply([2], 3)  # 正常运行，返回6
result = multiply([2.5], (1,2))  # 抛出类型错误异常，因为参数类型不匹配

@check_args_for_class
class A(object):
    def __init__(self):
        super(A, self).__init__()

    def func(self, a: T):
        return a


@check_args_for_class
class B(A):
    def __init__(self):
        super(B, self).__init__()

    def func(self, a: T, b: List[int]):
        return a

a = A()
b = B()
a.func(1)    # 正常运行
a.func([1,2])    # 抛出类型错误异常，因为参数类型不匹配
b.func(1,[2])    # 正常运行
b.func(1,2)    # 抛出类型错误异常，因为参数类型不匹配
   


```


