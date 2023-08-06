from translate.vsp2xml import LayoutTranslator
from vsp.VSPparser import VSP
import os
import random


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


def write_file(file_name, path, text, encoding="utf-8"):
    pattern = ["/", "\\"][int("\\" in file_name)]

    if not path[-1] == pattern:
        path += pattern

    if not os.path.exists(path):
        os.mkdir(path)

    with open(path + file_name, "w", encoding=f"{encoding}") as f:
        f.write(text)


def load_string(vsp_str, name=None, encoding="utf-8"):
    if not name:
        file_name = random_name(length=10) + ".vsp"
    else:
        file_name = name + ".vsp"
    write_file(file_name, "./", vsp_str, encoding=encoding)
    vsp_class = VSP(path=f"./{file_name}").get_tab().son[0]
    os.remove("./" + file_name)
    return vsp_class


def generate_xml_by_string(vsp_str, xml_name, path, encoding="utf-8"):
    """
    通过字符串强行转换为XML文件（主要用于布局的转化）
    :param encoding: 文件编码，不采用utf-8可能会乱码
    :param vsp_str: VSP字符串
    :param xml_name: XML的名字
    :param path: 目标路径
    :return: None
    """
    vsp_tag = load_string(vsp_str)
    lt = LayoutTranslator(vsp_root_tag=vsp_tag)
    lt.level_traversal()
    text = lt.xml_tag.generate_string()
    write_file(xml_name, path, text, encoding=encoding)


def generate_xml(vsp_path, xml_name, path, encoding="utf-8"):
    """
    通过vsp文件转化为XML文件（主要用于布局的转化）
    :param encoding: 文件编码，不采用utf-8可能会乱码
    :param vsp_path: vsp文件路径（请确保您填入了正确的文件路径）
    :param xml_name: XML生成文件的名称
    :param path: 目标路径
    :return:
    """
    if ".xml" not in xml_name:
        xml_name += ".xml"

    vsp_tag = VSP(path=vsp_path).get_tab().son[0]
    lt = LayoutTranslator(vsp_root_tag=vsp_tag)
    lt.level_traversal()
    text = lt.xml_tag.generate_string()
    write_file(xml_name, path, text, encoding=encoding)


if __name__ == "__main__":
    # 回归测试
    generate_xml("../vsp/hellolay.vsp", "../hello_lay.xml", "./")
