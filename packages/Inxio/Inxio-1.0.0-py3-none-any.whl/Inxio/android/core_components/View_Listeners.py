"""
等等
你可能进来就看到你的IDE(如Pycharm)报错，提示没有java库
请不要去尝试pip安装“java”模块
出现错误是正常的
这个模块会在安卓应用运行时被JNI赋予，所以完全不用担心

你所处的模块，封装了诸如按键监听器等等的类，它们都是继承和实现了Java中相应的接口
┗( ▔, ▔ )┛
"""

from Inxio.global_var import PROJECT_DOMAIN


def PythonUnAllowed(func):
    """
    ─=≡Σ(((つ•̀ω•́)つ
    一个完全没有用的装饰器，唯一的作用就是提示你被
    这个装饰器装饰的函数不能再Python中调用！
    :param func: emm
    :return: emm
    """
    return func


import java
from Inxio.global_var import PROJECT_DOMAIN

OCL = java.jclass(PROJECT_DOMAIN + ".VOnClickListener")


class VOnClickListener(java.dynamic_proxy(OCL)):
    """
    通过JNI，重写了OnClickListener
    """

    def __init__(self):
        super().__init__()
        self.click_func = None

    def register_onClick(self, func):
        self.click_func = func
        return self

    @PythonUnAllowed
    def onClick(self, view):
        self.click_func(view)


DOCL = java.jclass(PROJECT_DOMAIN + ".VDialogInterface").OnClickListener


class VDialogClickListener(java.dynamic_proxy(DOCL)):
    """
    通过动态代理生成集成的类，重写了对话框的回调监听接口
    """

    def __init__(self):
        super().__init__()
        self.click_func = None

    def register_onClick(self, func):
        """
        注册函数事件
        :param func:函数体或匿名函数体
        :return: None
        """
        self.click_func = func
        return self

    @PythonUnAllowed
    def onClick(self, view):
        """
        java内部调用，Python内部不允许调用
        :param view:由Java向内传递，为
        :return:
        """
        self.click_func(view)
