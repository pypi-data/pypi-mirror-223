"""
author：@cemeye
finish_time：2023/5
version:1.3
mail:你猜

你好！这里是cemeye！没错，又是我，这次来看看这个模块的作用！

这个模块，完全没有用到任何第三方库，只通过Python内置函数和方法
创建了一种名为VSP的标记语言！这是一种类似于kv语言的标记语言（如果你用过kivy的话）
没用过也没关系

这个语言的特色：
    1.更加清晰的逻辑结构
    2.方便地进行增删查改和生成
    3.可以导入已经存在的VSP文件，也可以通过程序动态生成再保存在文件中
    4.支持内嵌python代码，不过不是直接在文件中写python代码哦

这个模块最初是我为了写一个Python-Android模块Inxio时想用来动态翻译为XML的，不过我觉得这个模块
很好用，于是就把它单独分离和重构了！

内部原理大量应用了exec 与 eval这两个函数，主要功能就是解析字符串等等

祝你喜欢！

"""
from __future__ import annotations

__author__ = "cemeye"
__finish_time__ = "2023/5"
__version__ = "1.3.0"

import re
import traceback
import random


class VSPException(Exception):
    def __init__(self, msg):
        self.msg = msg
        traceback.print_exc()
        super().__init__(msg)

    def __str__(self):
        return f"@<{self.__class__.__name__}>[" + self.msg + "]"


class VSPRunCodeError(VSPException):
    """
    在运行VSP中的代码报错时
    """


class VSPUnknownCommandError(VSPException):
    """
    VSP命令未发现时报错
    """
    ...


class VSPModuleNotFoundError(VSPException):
    """
    VSP 在导入模块时错误
    """
    ...


class VSPIncludeMouldError(VSPException):
    """
    VSP 在包含模块时可能会报错
    """
    ...


class VSPPretreatmentEndFlagNotFoundError(VSPException):
    """
    VSP @PED 终止符未发现时会报错
    """
    ...


class VSPTabAttributeNotDefineError(VSPException):
    """
    属性未定义时报错
    """
    ...


class VSPSonNotFoundError(VSPException):
    """
    未发现直系子节点时报的错
    """


class VSPDeepSonNotFoundError(VSPException):
    """
    深度遍历删除子节点时未发现报的错误
    """


class VSPTagNotDefinedError(VSPException):
    """
    当标签未定义时报的错
    """


class VSPTemplateVarNotFoundError(VSPException):
    """
    当模板变量未在对应文件定义时
    """


# 错误定义完毕，下面是对应代码


def random_name(length=8) -> str:
    result = ""
    for i in range(length):
        result += \
            ["a", "b", "c",
             "d", "e", "f",
             "g", "h", "i",
             "j", "k", "l",
             "m", "n", "o",
             "p", "q", "r",
             "s", "t", "u",
             "v", "w", "x",
             "y", "z"][random.randint(0, 25)]
    return result


class VSPGenerateControl:
    """
    生成器,根据获取的Tab进行生产文字
    """

    def __init__(self, VSP_tab=None):
        self.final_result = []
        if not VSP_tab:
            self.tab = VSPTab().set_name("VSPROOT").set_ID("@vsp_root")
        else:
            self.tab = VSP_tab

    def add_son(self, tag_name, tag_id) -> None:
        """
        添加一个直系后代
        :param tag_id:
        :param tag_name:
        :return:
        """
        self.tab.set_son(VSPTab().set_ID(tag_id).set_name(tag_name))

    def deep_add_son(self, target_tag_ID, tag_name, tag_id) -> None:
        """
        深度遍历，添加子孙节点
        :param target_tag_ID: 目标父节点
        :param tag_id: 标签ID
        :param tag_name: 标签名
        :return: None
        """
        self.get_target_by_ID(target_tag_ID).set_son(VSPTab().set_name(tag_name).set_ID(tag_id))

    def add_attribute(self, ID, attr_name, value) -> None:
        """
        浅层遍历，为直系节点设置属性
        :param ID: 目标ID
        :param attr_name:属性名
        :param value: 属性值
        :return: None
        """
        for i in self.tab.son:
            if i.ID == ID:
                i.set_attribute(attribute_name=attr_name, value=value)
                return
        raise VSPSonNotFoundError("未找到目标节点ID 为\"{ID}\"的目标！")

    def deep_add_some_attributes(self, ID, attr_value_dict) -> None:
        """
        深度批量添加属性
        :param ID: None
        :param attr_value_dict:属性-值 字典
        :return: None
        """
        try:
            target = self.get_target_by_ID(ID)
            for i in attr_value_dict.keys():
                target.set_attribute(attribute_name=i, value=attr_value_dict[i])
        except AttributeError:
            raise VSPSonNotFoundError("未找到目标节点ID 为\"{ID}\"的目标！")

    def deep_add_attribute(self, ID, attr_name, value) -> None:
        """
        深度遍历，查找所有子节点，为目标添加属性
        :param ID: ID
        :param attr_name:属性名
        :param value: 属性值
        :return: None
        """
        try:
            self.get_target_by_ID(ID).set_attribute(attribute_name=attr_name, value=value)
        except AttributeError:
            raise VSPSonNotFoundError("未找到目标节点ID 为\"{ID}\"的目标！")

    def get_target_by_ID(self, ID) -> VSPTab:
        """
        通过ID获取一个VSP标签
        """
        return self.tab.get_target_by_ID(ID)

    def _recursive_struct(self, list_, index_=0) -> None:
        """
        递归生成结构体
        :param list_: None
        :param index_:
        :return:
        """
        for i in list_:
            if type(i) is str:
                self.final_result.append(index_ * "=" + "|" + i)
            else:
                self._recursive_struct(i, index_=index_ + 1)

    def generate_vsp_file(self, target_path, list_=None) -> None:
        """
        根据路径进行生成vsp文件
        :param list_: ..
        :param target_path:目标路径
        :return: None
        """
        if not list_:
            list_ = self.tab.get_recursive_struct()
        self._recursive_struct(list_)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("@PretreatmentEnd\n")
            for i in self.final_result:
                tabs = i.split("|", 1)[0].replace("=", "  ")
                result = tabs + i.split("|", 1)[1]
                f.write(tabs + result + "\n")


class VSPTab:
    def __init__(self):
        """
        定义的，VSP标签
        """
        self.name = "_init_"
        self.ID = "_init_"
        self.father_id = "_init_"
        self.attributes = {}
        self.son = []

    def __str__(self) -> str:
        """
        魔术方法，用于返回字符串式的结果
        :return: str
        """
        return f"*{self.name}[{self.ID}]:"

    def duplicate_removal(self) -> None:
        """
        去重，因为VSP在编译环节会通过动态添加父节点和子节点的方式，可能会有重复，
        所以需要有序去重进行修正
        :return: None
        """
        # 有序排序的以来key
        index = self.son.index
        # 去重
        self.son = list(set(self.son))
        # 有序排序
        self.son.sort(key=index)
        # 递归对于子节点去重
        for i in self.son:
            i.duplicate_removal()

    def set_ID(self, ID) -> VSPTab:
        """
        为Tab设置标签ID
        :param ID: str
        :return: self
        """
        self.ID = ID
        return self

    def set_father(self, fatherID) -> VSPTab:
        """
        为Tag设置父节点的ID
        :param fatherID: str
        :return: self
        """
        self.father_id = fatherID
        return self

    def delete_son(self, ID) -> None:
        """
        只删除直系节点
        :return: None
        """
        for i in self.son:
            if i.ID == ID:
                self.son.remove(i)
                return
        raise VSPSonNotFoundError(
            f"未发现直系子节点ID\"{ID}\"！如果有需要，请使用deep_delete_son方法于全部子孙节点范围内删除！")

    def deep_delete_son(self, ID) -> None:
        """
        深度遍历，删除某个节点
        :param ID:目标节点的ID
        :return: None
        """
        try:
            target = self.get_target_by_ID(self.get_target_by_ID(ID).father_id).son
            for i in target:
                if i.ID == ID:
                    self.get_target_by_ID(self.get_target_by_ID(ID).father_id).delete_son(ID)
                    return
        except AttributeError:
            raise VSPDeepSonNotFoundError(
                f"深度节点遍历错误！在全部子孙范围内未发现目标节点ID\"{ID}\"")

    def set_name(self, name) -> VSPTab:
        """
        设置名称
        :param name:
        :return:
        """
        self.name = name
        return self

    def set_attributes(self, attributes_names) -> VSPTab:
        """
        设置属性列表
        :param attributes_names:list
        :return:self
        """
        self.attributes_names = attributes_names
        self.attributes = {i: None for i in self.attributes_names}
        return self

    def set_attribute(self, attribute_name, value) -> None:
        """
        设置目标属性值
        :param attribute_name:
        :param value:
        :return:
        """
        try:
            self.attributes[attribute_name] = value

        except KeyError:
            # 报错可能:标签中属性未定义
            raise VSPTabAttributeNotDefineError(
                f"标签{self.name}中存在未定义的属性{attribute_name}!")

    def get_sons_IDs(self) -> list:
        """
        获取直系子节点的全部ID
        :return: list[str,str.....]
        """
        names = []
        for i in self.son:
            names.append(i.ID)
        return names

    def set_son(self, son) -> None:
        """
        为标签设置子节点
        :param son: VSPTab Class
        :return: None
        """
        self.son.append(son)

    def get_target_by_ID(self, ID) -> VSPTab:
        """
        通过ID递归寻找对应Tab
        :param ID: str
        :return: None
        """
        for i in self.son:
            if i.ID == ID:
                return i
        for i in self.son:
            return i.get_target_by_ID(ID)

    def get_sons(self) -> list:
        """
        获取全部直系子节点的描述
        :return: [str,str,str......]
        """
        sons = [str(i) for i in self.son]
        return sons

    def recursive_rendering_sons(self, index=0, with_attr=False) -> None:
        """
        递归渲染子孙节点之间的关系
        通过树状结构的制表符呈现
        :param index: 固定结构
        :param with_attr: 是否一同将属性渲染出来?
        :return: None
        """

        if with_attr:
            # 渲染属性
            index = index
            if self.attributes:
                print("╠" + (index - 1) * "════|" + "属性:" + str(self.attributes))

        # 不渲染属性
        index = index
        for i in self.son:
            print("┣" + index * "━━━━|" + str(i))
            i.recursive_rendering_sons(index=index + 1, with_attr=with_attr)

    def get_recursive_struct(self, index=0) -> list:
        """
        递归渲染子孙节点之间的关系
        通过树状结构的制表符呈现
        :param index: 固定结构
        :return: None
        """
        all_list = []
        # 渲染属性
        index = index
        for i in self.attributes.keys():
            all_list.append("-" + i + " = " + str(self.attributes[i]))
        for i in self.son:
            all_list.append(str(i))
            all_list.append(i.get_recursive_struct(index=index + 1))
        return all_list

    def process_attr_code(self, system_vars, template_vars) -> None:
        """
        解析在变量赋值时的值
        :param template_vars:
        :param system_vars: 系统变量字典
        :return: None
        """
        for attr_name in self.attributes.keys():
            # 当为系统变量赋值时
            target_attr_value = self.attributes[attr_name].strip()
            if target_attr_value[0] == "$":
                for system_key in system_vars.keys():
                    if system_key in target_attr_value:
                        target_attr_value = target_attr_value.replace("$" + system_key,
                                                                      f"system_vars[\"{system_key}\"]")
                        try:
                            target_attr_value = eval(target_attr_value)
                        except Exception:
                            raise VSPRunCodeError(f"在运行属性解析时出错！出错位置:{attr_name}")
                        self.set_attribute(attribute_name=attr_name, value=target_attr_value)
            # 当为python表达式时
            elif target_attr_value.strip().split(".")[0] == "~vsp":
                try:
                    self.set_attribute(attribute_name=attr_name,
                                       value=eval(str(target_attr_value.strip().split(".")[1])))
                except Exception:
                    raise VSPRunCodeError(f"在运行属性解析时出错！出错位置:{attr_name}")
            else:
                try:
                    self.set_attribute(attribute_name=attr_name, value=eval(str(target_attr_value)))
                except Exception as e:
                    if_template_var = []
                    for key in template_vars.keys():
                        if "{{" + key + "}}" in target_attr_value:
                            if_template_var.append(key)

                    if if_template_var:
                        value = target_attr_value.strip()
                        for spica_var_not_repeat in if_template_var:
                            exec(
                                f"var_{spica_var_not_repeat} = template_vars[\"{spica_var_not_repeat}\"]")
                            value = value.replace("{{" + spica_var_not_repeat + "}}",
                                                  f"var_{spica_var_not_repeat}")
                        self.set_attribute(attribute_name=attr_name, value=eval(value))
                    else:
                        raise VSPRunCodeError(
                            f"在运行属性解析时出错！赋值不合法！出错位置:{attr_name}\n错误原因:{str(e)}")

        for i in self.son:
            i.process_attr_code(system_vars, template_vars)

    def get_name(self):
        return self.name

    def get_ID(self):
        return self.ID

    def get_father_ID(self):
        return self.father_id

    def get_attributes(self):
        return self.attributes


class FormatCodeParser:
    """
    VSP编码解析器
    """

    def __init__(self, lines, vsf):
        """
        需要传参
        :param lines:VSPFile Class的 code_lines属性
        """
        self.vsf_system_var = vsf.system_var
        self.template_vars = vsf.template_vars
        self.root_tab = None
        self.lines = lines
        # 预处理，添加首行
        self._pretreatment_lines()

        self.line_dict = {}

        self._process_tabs(self.lines)

        self.all_runtime_codes = []
        self.generate_tabs()

        # 处理运行时的VSP代码，属性中的值
        self.process_code_in_var()

        self.process_runcodes_system_var()

    def _pretreatment_lines(self) -> None:
        """
        预处理，添加首行
        :return:
        """
        new_list = ["*VSPROOT[@vsp_root]:"]
        for i in self.lines:
            i = "    " + i
            new_list.append(i)

        self.lines = new_list

    def _process_tabs(self, lines) -> None:
        """
        初步处理标签
        :param lines:行状文字,列表
        :return:None
        """
        new_lines = []
        # 初步替换制表符或四个空格为₪,方便之后的处理
        for i in lines:
            new_line = i.replace("    ", "₪")
            new_lines.append(new_line)
        max_str = max([i.count('₪') for i in new_lines])
        line_dict = {str(i): [] for i in range(max_str + 1)}

        # 通过₪符号,确定父子关系,进行二次赋值字符串
        his_p = {}
        parent = [1, ""]
        for index, ele in enumerate(new_lines):
            len_str = ele.count("₪")
            if len_str > parent[0]:
                parent[0] = len_str
                parent[1] = new_lines[index - 1].replace("₪", "")

                his_p[str(len_str)] = new_lines[index - 1].replace("₪", "")
            elif len_str < parent[0]:
                try:
                    parent[0] = len_str
                    parent[1] = his_p[str(len_str)]
                except KeyError:
                    ...
            line_dict[str(len_str)].append(ele.replace("₪", "") + "►►" + parent[1])

        self.line_dict = line_dict

    @staticmethod
    def _process_attr(attr_str) -> tuple:
        """
        处理属性节点,返回名称和对应值
        :param attr_str: str
        :return:
        """
        attrs = attr_str.strip().split("►►")[0].split("=")
        name = attrs[0].strip()
        value = attrs[1].strip()
        return name, value

    @staticmethod
    def get_father(star_tag_str) -> str:
        """
        获取父节点
        :param star_tag_str:str
        :return:None
        """
        try:
            father = star_tag_str.strip().split("►►")[1].split("[", 1)[1][0:-2]
            return father
        except IndexError:
            return "@Root"

    @staticmethod
    def process_tag(tag_str) -> tuple:
        """
        处理标签,返回类型,标签名,标签ID
        :param tag_str: str
        :return:None
        """
        tag_name = tag_str.strip().split("[", 1)[0][1:]
        tag_type = tag_str.strip().split("[", 1)[0][0]
        if tag_type == "*":
            tag_ID = tag_str.strip().split("►►")[0].split("[", 1)[1][0:-2]
        else:
            tag_ID = tag_str.strip().split("►►")[1].split("[", 1)[1][0:-2]
        return tag_type, tag_name, tag_ID

    def generate_tabs(self) -> None:
        """
        生成标签
        :return: None
        """
        all_tags = []
        for key in self.line_dict.keys():
            line = self.line_dict[key]
            for tag in line:
                # 当标签为*时的处理
                if tag[0] == "*":
                    tag_father_id = self.get_father(tag)
                    tag_type, tag_name, tag_ID = self.process_tag(tag)
                    tag_new = VSPTab().set_ID(tag_ID).set_name(tag_name).set_father(tag_father_id)

                    all_tags.append(tag_new)
                    for i in all_tags:
                        if i.ID == tag_father_id:
                            i.set_son(tag_new)
                            break

                    for i in all_tags:
                        for ii in all_tags:
                            if ii.ID == i.father_id:
                                ii.set_son(i)
                            elif ii.get_target_by_ID(i.father_id):
                                ii.get_target_by_ID(i.father_id).set_son(i)
                # 当标签为-时的处理
                elif tag[0] == "-":
                    tag_father_id = self.get_father(tag)
                    for i in all_tags:
                        name, value = self._process_attr(tag)
                        if i.ID == tag_father_id:
                            i.set_attribute(name, value)
                            break
                        elif i.get_target_by_ID(tag_father_id):
                            i.get_target_by_ID(tag_father_id).set_attribute(name, value)
                elif tag[0] == "~":
                    father = self.get_father(tag)
                    self.all_runtime_codes.append([tag.split("►►")[0].split("->")[1], father])

        # 进行批量去重,并且对根节点进行赋值
        for i in all_tags:
            i.duplicate_removal()
            if i.father_id == "@Root":
                self.root_tab = i

    def get_root_tag(self) -> VSPTab:
        """
        获取根节点
        :return:self.root_Tab
        """
        return self.root_tab

    def process_runcodes_system_var(self) -> None:
        """
        解析目标系统变量赋值
        :return: None
        """
        for index, line_code in enumerate(self.all_runtime_codes):
            for var_name in self.vsf_system_var.keys():
                if f"${var_name}" in line_code[0]:
                    if type(self.vsf_system_var[var_name]) is str:
                        self.all_runtime_codes[index] = [
                            line_code[0].replace(f"${var_name}",
                                                 "\"" + self.vsf_system_var[var_name] + "\""),
                            line_code[1]]
                    else:
                        self.all_runtime_codes[index] = [
                            line_code[0].replace(f"${var_name}",
                                                 str(self.vsf_system_var[var_name])),
                            line_code[1]]

    def process_code_in_var(self) -> None:
        """
        有一些属性是由VSP系统变量赋值，或者Python表达式，需要解析并且更改赋值
        :return: None
        """
        self.root_tab.process_attr_code(system_vars=self.vsf_system_var,
                                        template_vars=self.template_vars)


class InxioSpicaFile:
    """
    VSP File 类，调用前面的FormatCodeParser，
    通过构建VSP Tab来进行解析
    """

    def __init__(self, path, template_var=None):
        self.path = path
        self.file_lines = []
        self.code_lines = []
        self.system_var = {}

        self.template_vars = {}

        self.include_pyfiles_paths = {}
        for line in open(self.path, 'r', encoding="utf-8"):  # 打开文件
            rs = self._process_formal(line.rstrip('\n'))
            # 预处理，为空白ID随机赋值
            if rs:
                for i in re.findall("""\*.*?\[_]""", rs):
                    rs = rs.replace(i, i.split("[_")[0] + "[" + random_name() + "]", 1)
                self.file_lines.append(rs)
        # 预处理划分
        self._divide_pretreatment(self.file_lines)

        # 处理特殊转义字符
        self._first_marks()

        # 处理模板变量
        self._process_template_vars(template_var_dict=template_var)

        # 处理系统变量
        self._process_system_var(template_var_dict=template_var)
        # 处理引入库
        self._process_include_py()

        # 处理系统变量中运行的代码
        self._process_runcode_var()

        # 运行单行代码
        self._run_line_code()

    def _process_template_vars(self, template_var_dict) -> None:
        """
        处理模板变量（即用{{}}包含的值）
        :return: None
        """
        if template_var_dict:
            self.template_vars = template_var_dict

    def _divide_pretreatment(self, lines) -> None:
        """
        划分代码区和预处理区
        :param lines:
        :return:
        """
        try:
            index = lines.index("@PED")
            self.code_lines = self.file_lines[index + 1:]
            self.file_lines = self.file_lines[0:index]

        except ValueError:
            raise VSPPretreatmentEndFlagNotFoundError(
                "未发现VSP终止符\"@PED\",请在代码中添加！")

    def _run_line_code(self) -> None:
        """
        运行单行代码
        :return: None
        """
        for i in self.file_lines:
            if i.strip()[0] == "~":
                command = i.strip().split(".", 1)[1]
                try:
                    exec(command)
                except SyntaxError:
                    try:
                        target_lib = self.include_pyfiles_paths[command.split(".", 1)[0]]
                        command_new = command.split(".", 1)[1]
                        exec(f"""target_lib.{command_new}""")
                    except KeyError:
                        error_lib_name = command.split(".", 1)[0]
                        raise VSPModuleNotFoundError(f"并没有找到名为[{error_lib_name}]的模块！")
                except NameError:
                    target_lib = self.include_pyfiles_paths[command.split(".", 1)[0]]
                    command_new = command.split(".", 1)[1]
                    exec(f"""target_lib.{command_new}""")

    def _first_marks(self) -> None:
        """
        替换特殊符号
        反斜杠+单，双引号替换为ф
        反斜杠+n，替换为∏
        :return: None
        """
        new_list = []
        for i in self.file_lines:
            i = i.replace("\\\"", "ф")
            i = i.replace("\\\'", "ф")
            i = i.replace("\\\n", "∏")
            new_list.append(i)
        self.file_lines = new_list

    @staticmethod
    def _process_formal(line) -> None | str:
        """
        预处理数据，删掉注释和空行
        :return: line
        """
        if line:
            try:
                if not line.strip()[0] == "#":
                    return line
            except Exception:
                ...
        return None

    def _process_system_var(self, template_var_dict=None) -> None:
        """
        处理系统变量
        :return: None
        """
        for i in self.file_lines:
            if i.strip()[0] == "$":
                result = i.replace("$", "").strip().split("=", 1)
                try:
                    if "~vsp" not in result[1].strip():
                        self.system_var[result[0].strip()] = eval(result[1].strip())
                    else:
                        self.system_var[result[0].strip()] = result[1].strip()
                except NameError:
                    if_template_var = []
                    for key in template_var_dict.keys():
                        if "{{" + key + "}}" in result[1].strip():
                            if_template_var.append(key)

                    if if_template_var:
                        value = result[1].strip()
                        for spica_var_not_repeat in if_template_var:
                            exec(
                                f"var_{spica_var_not_repeat} = template_var_dict[\"{spica_var_not_repeat}\"]")
                            value = value.replace("{{" + spica_var_not_repeat + "}}",
                                                  f"var_{spica_var_not_repeat}")
                        self.system_var[result[0].strip()] = eval(value)

    def _process_include_py(self) -> None:
        """
        解析包含进来的py文件
        :return: None
        """
        for i in self.file_lines:
            if i.strip()[0] == "@":
                if "include" in i:
                    lib_name = i.split("=")[1].strip()[1:-1]
                    if "," not in lib_name:
                        try:
                            lib = __import__(f"{lib_name}")
                            self.include_pyfiles_paths[lib_name] = lib
                        except ValueError:
                            ...
                        except ModuleNotFoundError:
                            raise VSPIncludeMouldError(f"导入Python文件失败！错误文件：{lib_name}")
                    else:
                        libs = lib_name.split(",")
                        for a_lib in libs:
                            try:
                                lib = __import__(f"{a_lib}")
                                self.include_pyfiles_paths[a_lib] = lib
                            except ValueError:
                                ...
                            except ModuleNotFoundError:
                                raise VSPIncludeMouldError(f"导入Python文件失败！错误文件：{a_lib}")
                else:
                    raise VSPUnknownCommandError(
                        f"未知vsp命令{i}!您正在使用'@'操作符来引入文件，但是语法似乎并不正确")

    def _process_runcode_var(self) -> None:
        """
        处理运行代码
        :return: None
        """

        for key in self.system_var.keys():
            if str(self.system_var[key])[0:5] == "~vsp.":
                command = self.system_var[key].split(".", 1)[1]
                try:
                    self.system_var[key] = eval(command)
                except SyntaxError:
                    try:
                        target_lib = self.include_pyfiles_paths[command.split(".", 1)[0]]
                        command_new = command.split(".", 1)[1]
                        self.system_var[key] = eval(f"""target_lib.{command_new}""")
                    except KeyError:
                        error_lib_name = command.split(".", 1)[0]
                        raise VSPModuleNotFoundError(f"并没有找到名为[{error_lib_name}]的模块！")
                except NameError:
                    target_lib = self.include_pyfiles_paths[command.split(".", 1)[0]]
                    command_new = command.split(".", 1)[1]
                    self.system_var[key] = eval(f"""target_lib.{command_new}""")


class VSPLoader:
    """
    VSP现存文件导入器
    作用：如果你已经写好了一个VSP文件，你可以用这个类进行读取和更改
    PS：这里面很多函数都是对于VSPTab的再度封装
    """

    def __init__(self, path, template_var=None):
        self.vspf = InxioSpicaFile(path, template_var=template_var)
        self.fcp = FormatCodeParser(self.vspf.code_lines, self.vspf)
        self.root_tag = self.fcp.get_root_tag()

    def delete_son(self, ID) -> None:
        """
        只删除直系节点
        :return: None
        """
        self.root_tag.delete_son(ID=ID)

    def deep_delete_son(self, ID) -> None:
        """
        深度遍历，删除某个节点
        :param ID:目标节点的ID
        :return: None
        """
        self.root_tag.deep_delete_son(ID=ID)

    def set_attribute(self, attribute_name, value) -> None:
        """
        设置目标属性值
        :param attribute_name:
        :param value:
        :return:
        """
        self.root_tag.set_attribute(attribute_name=attribute_name, value=value)

    def get_sons_IDs(self) -> list:
        """
        获取直系子节点的全部ID
        :return: list[str,str.....]
        """
        return self.root_tag.get_sons_IDs()

    def set_son(self, son) -> None:
        """
        为标签设置子节点
        :param son: VSPTab Class
        :return: None
        """
        self.root_tag.set_son(son)

    def get_target_by_ID(self, ID) -> VSPTab:
        """
        通过ID递归寻找对应Tab
        :param ID: str
        :return: None
        """
        return self.root_tag.get_target_by_ID(ID=ID)

    def get_sons(self) -> list:
        """
        获取全部直系子节点的描述
        :return: [str,str,str......]
        """
        return self.root_tag.get_sons()

    def recursive_rendering_sons(self, index=0, with_attr=False) -> None:
        """
        递归渲染子孙节点之间的关系
        通过树状结构的制表符呈现
        :param index: 固定结构
        :param with_attr: 是否一同将属性渲染出来?
        :return: None
        """
        self.root_tag.recursive_rendering_sons(index=index, with_attr=with_attr)

    def get_recursive_struct(self, index=0) -> list:
        """
        递归渲染子孙节点之间的关系
        通过树状结构的制表符呈现
        :param index: 固定结构
        :return: None
        """
        return self.root_tag.get_recursive_struct(index=index)


class VSP:
    """
    为了方便大家使用，我特意将上面不同类型的类进行了封装
    这个是真正的整合类，支持全部功能
    """

    def __init__(self, path="", template_var=None):
        # 导入器
        if path:
            self.loader = VSPLoader(path=path, template_var=template_var)
            self.fcp = self.loader.fcp
            self.runtime_codes = self.fcp.all_runtime_codes
        else:
            self.loader = None
            # 生成器
        self.maker = VSPGenerateControl()

    def get_system_vars(self) -> None | dict:
        """
        返回系统变量大全
        :return: None
        """
        if self.loader:
            return self.loader.vspf.system_var
        else:
            return None

    def recursive_rendering_sons(self, with_attr=True) -> None:
        """
        根节点渲染
        :param with_attr:是否渲染属性
        :return: None
        """
        if self.loader:
            if self.loader.vspf.system_var:
                print("┏系统变量列表")
                for i in self.loader.vspf.system_var.keys():
                    print(f"┗━━[{i}]━━━|{self.loader.vspf.system_var[i]}|")
            self.loader.root_tag.recursive_rendering_sons(with_attr=with_attr)
        else:
            self.maker.tab.recursive_rendering_sons(with_attr=with_attr)

    def get_tab(self, if_no_root=False) -> VSPTab:
        """
        获取根标签
        :param if_no_root:是否禁用获取root标签?
        :return:VSPTab
        """
        if self.loader:
            if if_no_root:
                return self.loader.root_tag.son
            else:
                return self.loader.root_tag
        else:
            return self.maker.tab


class ClassTemplate:
    def __init__(self, _class_, ID_target_arg='ID', append_class_func=None):
        """
        此类为类模板定义，通过添加至ClassTemplateParser类，再将ClassTemplateParser
        类绑定到VSP类中，即可实现最终的实时解析和生成效果

        :param _class_: 某个类的__class__本体

        :param append_class_func: 当类被添加至此类（即标签中套标签）时所执行的函数的函数体

        :param ID_target_arg: VSP解析语法中，标签后必须有ID参数；所以这个参数目的在于将标签的ID赋值到传进来的_class_本体的哪个属性中，默认为'ID'

        注：
            ①append_class_func所代表的函数体必须有参数appended_class即 def x(appended_class):...
            ②注意，标签类不要有构造参数，参数会在解析过程中动态赋值
        """
        self.bind_tag_name = _class_.__name__
        self.ID_target_arg = ID_target_arg
        self.class_body = _class_
        if append_class_func:
            self.append_class_func = append_class_func.__name__
        else:
            self.append_class_func = None


class ClassTemplateParser:
    """
    类模板解析器，可以快速地将VSP标签映射到对应的类上
    """

    def __init__(self):
        self.runtime_codes = []
        self.class_template = {}
        self.runtime_classes = []

    def append_template(self, new_plate: ClassTemplate) -> None:
        """
        添加一个新的模板
        :param new_plate: ClassTemplate
        :return: None
        """
        self.class_template[new_plate.bind_tag_name] = new_plate

    def append_templates(self, templates: list) -> None:
        """
        批量添加模板
        :param templates:模板列表
        :return: None
        """
        for i in templates:
            self.append_template(i)

    def get_class_by_ID(self, ID) -> None | VSPTab:
        """
        通过ID获取类
        :param ID: str
        :return: class
        """
        for i in self.runtime_classes:
            if i.ID == ID:
                return i
        return None

    def process_runcode_system_var(self) -> None:
        """
        执行运行时代码
        :return: None
        """
        for item in self.runtime_codes:
            code, ID = item[0], item[1]
            target_class = self.get_class_by_ID(ID)
            try:
                exec(f"target_class.{code}")
            except Exception:
                raise VSPRunCodeError(f"在执行运行时代码时出错！位置：{code}")

    def Vparser(self, VSP_obj: VSP, fatherID=None, VSP_tab=None) -> None:
        """
        对于某个VSPTab进行解析
        :param fatherID:
        :param VSP_tab:
        :param VSP_obj: 填什么我不多说了吧？
        :return: Your Class
        """
        self.runtime_codes = VSP_obj.runtime_codes
        if not VSP_tab:
            VSP_tab = VSP_obj.get_tab()
        name, ID = VSP_tab.name, VSP_tab.ID
        if name in self.class_template.keys():
            class_target_template = self.class_template[name]

            class_target = class_target_template.class_body.__new__(
                class_target_template.class_body)

            # 通过python虚拟环境进行目标元类生成
            exec(f"class_target.{class_target_template.ID_target_arg} = \"{VSP_tab.ID}\"")

            # 虚拟生成目标属性，为其属性赋值
            for attr_name, value in VSP_tab.attributes.items():
                attr_name = attr_name[1:]
                if type(value) is str:
                    value = "\"" + value + "\""
                exec(f"class_target.{attr_name} = {value}")

            self.runtime_classes.append(class_target)
            if fatherID:
                father = self.get_class_by_ID(fatherID)
                target_func_name = self.class_template[father.__class__.__name__].append_class_func
                if target_func_name:
                    exec(f"father.{target_func_name}(class_target)")

            # 对子孙进行解析
            for i in VSP_tab.son:
                self.Vparser(VSP_obj, ID, VSP_tab=i)

        # 对根节点进行解析
        elif name == "VSPROOT":
            for i in VSP_tab.son:
                self.Vparser(VSP_obj, VSP_tab=i)
        else:
            raise VSPTagNotDefinedError(f"未定义的标签{name}")

    def get_render_classes(self) -> list:
        """
        获取渲染完的列表
        :return: None
        """
        return self.runtime_classes

    def get_first_class(self) -> object:
        """
        获取第一个类，一般都是根类
        :return: root_class
        """
        return self.runtime_classes[0]

    def parser(self, VSP_obj: VSP) -> None:
        """
        升级版parser!
        :param VSP_obj: VSP对象实例化
        :return:
        """
        self.Vparser(VSP_obj)
        self.process_runcode_system_var()

# END
