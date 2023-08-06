"""
生成XML文档
"""


class XMLTag:
    def __init__(self):
        self.tag_name = ""
        self.attrs = {}
        self.father = None
        self.sons = []
        self.text = ""

    def set_tag_name(self, name_str):
        """
        设置标签名
        :param name_str:标签名字符串
        :return: None
        """
        self.tag_name = name_str
        return self

    def add_attr(self, attr_name, value, addr=None):
        """
        添加一个属性值，可以带前缀
        :param attr_name: 属性名
        :param value: 属性值
        :param addr: 前缀（可选）
        :return: self
        """
        self.attrs[attr_name] = [addr, value]
        return self

    def add_attrs(self, attr_dict):
        """
        批量添加属性
        :param attr_dict:属性字典，{name:[attr_value,addr],name:[],name:[]...}
        :return: self
        """
        for key, value in attr_dict.items():
            self.add_attr(key, value[0], addr=value[1])
        return self

    def set_attr(self, attr_name, value):
        self.attrs[attr_name] = value
        return self

    def set_father(self, tag):
        """
        设置父节点
        :param tag:XMLTag对象
        :return: None
        """
        self.father = tag
        return self

    def add_son(self, son_tag):
        """
        添加子孙节点
        :param son_tag:
        :return:
        """
        son_tag.set_father(self)
        self.sons.append(son_tag)
        return self

    def _render_attrs(self):
        """
        渲染属性
        :return:
        """
        attrs = ""
        for attr_name, value in self.attrs.items():
            if value[0] is None:
                if type(value[1]) is str:
                    attrs += f"{attr_name}=\"{value[1]}\" "
                else:
                    attrs += f"{attr_name}={value[1]} "
            else:
                if type(value[1]) is str:
                    attrs += f"{value[0]}:{attr_name}=\"{value[1]}\" "
                else:
                    attrs += f"{value[0]}:{attr_name}={value[1]} "
        return attrs

    def get_string(self):
        """
        获得字符串
        :return:
        """
        son_texts = [i.get_string() for i in self.sons]
        son_text = ""
        for i in son_texts:
            son_text += i
        text = f"<{self.tag_name} {self._render_attrs()}>{son_text}</{self.tag_name}>"
        return text

    def generate_string(self):
        """
        最终生成和处理
        :return:
        """
        text = self.get_string()
        return text


class DataTag(XMLTag):
    """
    数据标签，有A，B，两种样式
    """
    TAG_TYPE_A = 0
    TAG_TYPE_B = 1

    def __init__(self, tag_type):
        super().__init__()
        # TAG_TYPE_A:带文字，开始标签和闭合标签的格式  TAG_TYPE_B:不带闭合标签，单独一个标签，内含属性
        self.tag_type = tag_type
        self.text = ""

    def add_son(self, son_tag):
        """
        重写方法，不允许数据标签添加子孙
        :param son_tag:
        :return:
        """
        raise Exception("Can not add son to a data-tag!")

    def set_text(self, text):
        """
        设置数据标签的文字内容
        :param text:
        :return:
        """
        self.text = text
        return self

    def get_string(self):
        """
        重写后的数据标签渲染文字的功能
        :return:
        """
        if self.tag_type == DataTag.TAG_TYPE_A:
            text = f"<{self.tag_name} {self._render_attrs()}>{self.text}</{self.tag_name}>"
            return text
        elif self.tag_type == DataTag.TAG_TYPE_B:
            text = f"<{self.tag_name} {self._render_attrs()}/>"
            return text


if __name__ == "__main__":
    x = XMLTag() \
        .set_tag_name("LinearLayout") \
        .add_attr("android", "http://schemas.android.com/apk/res/android") \
        .add_attr("id", "@+id/mylayout2")

    y = XMLTag().set_tag_name("TextView") \
        .add_attr("id", "@+id/textView3")

    z = DataTag(DataTag.TAG_TYPE_A).set_tag_name("DATA").add_attr("data", "emm").set_text("测试A类型的数据标签@")

    x.add_son(y)
    x.add_son(z)

    x.generate_string()
