class SingleTagAppendSonError(Exception):
    """
    对单标签节点添加子节点时会报的错误
    """


class AttributeNotExistError(Exception):
    """
    当属性不存在时会报此错误
    """


class SingleTagSetTextError(Exception):
    """
    为单标签设置内容时报错
    """


class GenerateUnknownTagError(Exception):
    """
    调用生成标签字符串方法时，标签未设置标签名时引发此错误
    """


class TagNotDataTagError(Exception):
    """
    当标签不是数据标签时对其内容进行赋值会引发的错误
    """


class XMLTag:
    def __init__(self):
        self.attributes = {}
        self.attribute_keys = []
        self.parent_tag = None
        self.son_tags = []
        self.tag_text = ""
        self.tag_name = None
        self.if_data_tag = False

    def __str__(self):
        return self.tag_name

    def append_attribute(self, attribute_name):
        """
        添加一个属性
        :param attribute_name:属性名称
        :return: None
        """
        self.attribute_keys.append(attribute_name)
        self.attributes[attribute_name] = None
        if ":" in attribute_name:
            setattr(self, attribute_name.split(":")[1], None)
        else:
            setattr(self, attribute_name, None)

    def append_attributes(self, attribute_names):
        """
        批量添加属性
        :param attribute_names: 属性名称列表
        :return: None
        """
        for i in attribute_names:
            self.append_attribute(i)

    def set_tag_name(self, name):
        """
        设置标签名
        :param name:标签名字符串
        :return: None
        """
        self.tag_name = name

    def set_parent(self, parent_arg):
        """
        设置父节点
        :param parent_arg: 父节点对象:XMLTag
        :return: None
        """
        self.parent_tag = parent_arg

    def set_text(self, text):
        """
        设置标签内容
        :param text: 内容字符串
        :return: None
        """
        if self.if_data_tag:
            self.tag_text = text
        else:
            raise TagNotDataTagError(f"[!]标签{str(self)}并不是数据标签，请先调用set_data_type_true()")

    def set_data_type_true(self):
        """
        设置成为数据标签(没有子标签，相反，里面是文字类型的内容的)
        :return: None
        """
        self.if_data_tag = True

    def append_son_tag(self, son_tag):
        """
        添加一个子节点
        :param son_tag:子节点对象:XMLTag
        :return: None
        """
        self.son_tags.append(son_tag)
        son_tag.set_parent(self)

    @property
    def sting_text(self):
        return self.generate_string_xml_tag()

    def set_attribute_value(self, attribute_name, value):
        if attribute_name in self.attribute_keys:
            if type(value) == str:
                value = "\"" + value + "\""
            elif type(value) == bool:
                if value:
                    value = "true"
                else:
                    value = "false"
            self.attributes[attribute_name] = value
        else:
            raise AttributeNotExistError(f"[!]标签属性{attribute_name}不存在！请检查拼写......")

    def get_attributes(self):
        return self.attribute_keys

    def print_attributes(self):
        print(self.attribute_keys)

    def generate_string_xml_tag(self):
        if not self.tag_name:
            raise GenerateUnknownTagError("[!]未知标签！可能是未设置标签名导致！")
        else:
            tag_text_start = f"<{self.tag_name} "
            # 生成参数
            for i in self.attribute_keys:
                if hasattr(self, i.split(":")[1]):
                    attr_name = i.split(":")[1]
                    result = eval(f"self.{attr_name}")
                    if result:
                        print(type(self), i, result)
                        if type(result) == str:
                            result = "\"" + result + "\""
                        tag_text_start += f"{i}=" + result + " "
                elif self.attributes[i]:
                    tag_text_start += f"{i}=" + self.attributes[i] + " "
            # 闭合起始标签
            tag_text_start += ">"
            # 判断数据标签，添加内容
            if self.if_data_tag:
                tag_text_start += self.tag_text
            tag_text_end = f"</{self.tag_name}>"
            for i in self.son_tags:
                tag_text_start += i.generate_string_xml_tag()

            tag_text_start += tag_text_end
            return tag_text_start


class SingleXMLTag(XMLTag):
    def __init__(self):
        super().__init__()
        self.parent_tag = None
        self.son_tags = None

    def append_son_tag(self, son_tag):
        raise SingleTagAppendSonError("[!]禁止向单节点标签添加新的子节点!")

    def set_text(self, text):
        raise SingleTagSetTextError("[!]禁止向单标签设置内容!")

    def generate_string_xml_tag(self):
        if not self.tag_name:
            raise GenerateUnknownTagError("[!]未知标签！可能是未设置标签名导致！")
        else:
            tag_text_start = f"<{self.tag_name} "
            # 生成参数
            for i in self.attribute_keys:
                if hasattr(self, i.split(":")[1]):
                    attr_name = i.split(":")[1]
                    result = eval(f"self.{attr_name}")
                    if result:
                        if type(result) == str:
                            result = "\"" + result + "\""
                        tag_text_start += f"{i}=" + result + " "
                elif self.attributes[i]:
                    tag_text_start += f"{i}=" + self.attributes[i] + " "
            # 判断数据标签，添加内容
            if self.if_data_tag:
                tag_text_start += self.tag_text
            tag_text_end = f"/>"

            tag_text_start += tag_text_end
            return tag_text_start


if __name__ == "__main__":
    a = XMLTag()
    a.set_tag_name("resources")
    a.append_attribute("xmlns:tools")
    a.set_attribute_value("xmlns:tools", "http://schemas.android.com/tools")

    b = XMLTag()
    b.set_tag_name("item")
    b.append_attribute("target")
    b.set_attribute_value("target", "zrd")

    c = SingleXMLTag()
    c.set_tag_name("item")
    c.append_attribute("target")
    c.set_attribute_value("target", "zrd")

    b.append_son_tag(c)
    a.append_son_tag(b)

    print(a.generate_string_xml_tag())
    a.print_attributes()
