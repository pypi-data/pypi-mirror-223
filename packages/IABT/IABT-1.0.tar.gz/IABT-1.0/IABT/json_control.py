from __future__ import annotations
import json


def read_json(json_path) -> dict | bool:
    """
    读取json,返回字典或错误
    :param json_path:路径
    :return: bool|dict
    """
    try:
        with open(json_path, "r") as f:
            text = f.read()
            json_dict = json.loads(text)
            return json_dict
    except FileNotFoundError:
        return False

    except json.JSONDecodeError:
        return False


def write_json(json_path, python_dict):
    """
    写入json文件
    :param json_path:路径
    :param python_dict: 字典对象
    :return: bool状态
    """
    try:

        with open(json_path, "w") as f:
            json.dump(python_dict, f)
            return True
    except FileNotFoundError:
        return False


def rewrite_json(json_path, key, new_value):
    """
    覆写json文件
    :param json_path: json路径
    :param key: 新键
    :param new_value:新值
    :return: bool状态
    """
    read_dict = read_json(json_path)
    try:
        if read_dict:
            read_dict[key] = new_value
            write_json(json_path, read_dict)
            return True
        else:
            return False
    except KeyError:
        return False

