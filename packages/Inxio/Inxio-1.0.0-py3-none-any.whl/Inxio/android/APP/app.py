import os
import shutil
import sys

from Inxio.android.core_components.Intent import VIntent
from Inxio.android.core_components.Activity import _ActivityType


def IntermediateCall(func):
    """
    又是一个没什么用的装饰器
    仅仅为了提示这个函数是中间调用级别的
    注：中间调用：即被Java层的Python代码调用
    :param func: func
    :return: None
    """
    return func


class TemplateKeyError(Exception):
    ...


def template_write(file_path, **kwargs):
    """
    用于写入模版文件
    例如，有一个文件内部有{{%site%}}这一部分，在kwargs里只需填写site=...即可为其赋值
    :param file_path: 文件目录
    :param kwargs: 键值对
    :return: None
    """

    old_text = ""
    dicts = [("{{%" + str(key) + "%}}", str(value)) for key, value in kwargs.items()]
    with open(file_path, "r", encoding="utf-8") as f:
        old_text = f.read()

    with open(file_path, "w", encoding="utf-8") as f:
        for item in dicts:
            if not item[0] in old_text:
                raise TemplateKeyError(f"[!]NotFoundKey【{item[0][3:-3]}】,Please check again. (>_<)")
            old_text = old_text.replace(item[0], item[1])

        f.write(old_text)


def walkFile(file):
    root_path = file
    file_list = []
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            file_list.append([root.split(root_path)[-1], f])
    return file_list


def only_copy(old_path, new_path, update=False):
    """new_path必须存在！不支持复制空文件夹"""
    if update:
        shutil.rmtree(new_path)
    p = ["\\", "/"][int("/" in old_path)]
    p2 = ["\\", "/"][int("/" in new_path)]
    if old_path[-1] != p:
        old_path += p
    if new_path[-1] != p2:
        new_path += p2
    for i in walkFile(old_path):
        if os.path.exists(f"{new_path}{i[0]}"):
            shutil.copy(f"{old_path}{i[0]}{p}{i[1]}", f"{new_path}{i[0]}{p2}{i[1]}")
        else:
            print(f"{new_path}{i[0]}", f"{old_path}{i[0]}{i[1]}", f"{new_path}{i[0]}{p2}{i[1]}")
            os.mkdir(f"{new_path}{i[0]}")
            shutil.copy(f"{old_path}{i[0]}{p}{i[1]}", f"{new_path}{i[0]}{p2}{i[1]}")


class AndroidAPP:
    """
    这里是Inxio程序的入口，你的APP需要继承这个！
    """

    def __init__(self):
        self.exe_blocks = []
        self.now_activity = None
        self.old_flap_activity = None
        self.activity_dict = {}

        self.ASK_PERMISSIONS = []

    def append_exe_block(self, block):
        """
        添加可执行块
        :param block:块文件
        :return: None
        """
        self.exe_blocks.append(block)

    @IntermediateCall
    def get_exe_blocks(self):
        """
        返回运行块
        :return:
        """
        return self.exe_blocks

    def bind_activity(self, activity_name: str):
        """
        绑定Activity
        :param activity_name: str
        :return: None
        """
        self.now_activity = self.activity_dict[activity_name]

    def set_permissions(self, permission_list):
        """
        设置运行时需要获取的权限
        :param permission_list: list
        :return:
        """
        self.ASK_PERMISSIONS = permission_list

    def append_activities(self, activity_list: list):
        """
        批量添加Activities
        :param activity_list: list
        :return: None
        """
        for i in activity_list:
            self.activity_dict[i.ID] = i

    def change_activity(self, new_activity_name, self_defined_bundle=None):
        """
        切换为新的Activity
        :param self_defined_bundle: 可能存在的自定义VBundle，用于传递数据
        :param new_activity_name: 新Activity的名字
        :return: None
        """
        if self.now_activity.java_activity:
            intent = VIntent(self.now_activity, new_activity_name)
            if self_defined_bundle:
                intent.setExtraDataBundle(self_defined_bundle)
            intent.setExtraData("new_activity", new_activity_name)
            self.old_flap_activity = self.now_activity
            self.now_activity = self.activity_dict[new_activity_name]

            self.old_flap_activity.java_activity.startActivity(intent.android_intent)

        elif self.old_flap_activity:
            self.now_activity = self.activity_dict[new_activity_name]
            intent = VIntent(self.old_flap_activity, new_activity_name)
            if self_defined_bundle:
                intent.setExtraDataBundle(self_defined_bundle)
            intent.setExtraData("new_activity", new_activity_name)
            self.old_flap_activity.java_activity.startActivity(intent.android_intent)

    def startActivityForResult(self, new_activity_name, request_code, self_defined_bundle=None):
        """
        切换为新的Activity,并且以获取结果的方式
        :param request_code: 请求的目标状态码
        :param self_defined_bundle: 可能存在的自定义VBundle，用于传递数据
        :param new_activity_name: 新Activity的名字
        :return: None
        """
        if self.now_activity.java_activity:
            intent = VIntent(self.now_activity, new_activity_name)
            if self_defined_bundle:
                intent.setExtraDataBundle(self_defined_bundle)
            intent.setExtraData("new_activity", new_activity_name)
            self.old_flap_activity = self.now_activity
            self.now_activity = self.activity_dict[new_activity_name]

            self.old_flap_activity.java_activity.startActivityForResult(intent.android_intent,
                                                                        request_code)

        elif self.old_flap_activity:
            self.now_activity = self.activity_dict[new_activity_name]
            intent = VIntent(self.old_flap_activity, new_activity_name)
            if self_defined_bundle:
                intent.setExtraDataBundle(self_defined_bundle)
            intent.setExtraData("new_activity", new_activity_name)
            self.old_flap_activity.java_activity.startActivityForResult(intent.android_intent,
                                                                        request_code)

    def get_target_activity(self, activity_name):
        return self.activity_dict[activity_name]

