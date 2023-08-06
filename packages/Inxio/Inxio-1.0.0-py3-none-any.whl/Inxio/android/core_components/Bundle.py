from android.os import Bundle


class VBundle:
    def __init__(self):
        """
        该类用于在不同Activity间传递数据，
        如果你有传递很多不同数据的需要，
        请尝试将数据变为字符串列表的方式进行传递，
        这个Bundle不能传递类对象，也不能传递字典，
        是因为安卓Bundle类的局限性
        """
        self.bundle = Bundle()

    def auto_append_by_dict(self, python_dict: dict):
        """
        通过字典自动添加
        注意！该字典键对应的值必须为基本类型！如果为列表类型数据，请保证里面所有元素的类型全等！另，不要传入字典！
        :param python_dict:字典对象
        :return:self
        """
        for key, value in python_dict.items():
            if isinstance(value, int):
                self.bundle.putInt(key, value)
            elif isinstance(value, str):
                self.bundle.putString(key, value)
            elif isinstance(value, float):
                self.bundle.putDouble(key, value)
            elif isinstance(value, list):
                if all(isinstance(x, int) for x in value):
                    self.bundle.putIntArray(key, value)

                elif all(isinstance(x, float) for x in value):
                    self.bundle.putDoubleArray(key, value)

                elif all(isinstance(x, str) for x in value):
                    self.bundle.putStringArray(key, value)
        return self

    def putInt(self, key, value):
        """
        添加整数键值对
        :param key: 键
        :param value: 值
        :return: self
        """
        self.bundle.putInt(key, value)
        return self

    def putString(self, key, value):
        """
        添加字符串键值对
        :param key: 键
        :param value: 值
        :return: self
        """
        self.bundle.putString(key, value)
        return self

    def putFloat(self, key, value):
        """
        添加小数键值对
        :param key: 键
        :param value: 值
        :return: self
        """
        self.bundle.putDouble(key, value)
        return self

    def putIntList(self, key, value):
        """
        添加整数列表键值对
        :param key: 键
        :param value: 值
        :return: self
        """
        self.bundle.putIntArray(key, value)
        return self

    def putStrList(self, key, value):
        """
        添加字符串列表键值对
        :param key: 键
        :param value: 值
        :return: self
        """
        self.bundle.putStringArray(key, value)
        return self

    def putFloatList(self, key, value):
        """
        添加小数列表键值对
        :param key: 键
        :param value: 值
        :return: self
        """
        self.bundle.putDoubleArray(key, value)
        return self
