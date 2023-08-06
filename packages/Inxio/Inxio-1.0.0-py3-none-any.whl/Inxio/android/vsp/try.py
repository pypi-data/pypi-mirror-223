from VSPparser import VSP


class A:
    def __init__(self):
        self.a = 10


def a():
    ...


v = VSP(path="../../../../../Desktop/android_layout.vsp", template_var={"try_obj": a, "print": "你好啊", "new": "登录", "das": "牛逼l666", "dict_key": "heh"})

v.recursive_rendering_sons(with_attr=True)
