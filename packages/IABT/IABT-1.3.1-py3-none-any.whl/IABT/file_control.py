import os
import shutil


def copy_to(old_file_path, new_file_path):
    try:
        with open(old_file_path, "r", encoding="utf-8") as f:
            text = f.read()
            with open(new_file_path, "w", encoding="utf-8") as f2:
                f2.write(text)
        return True
    except Exception as e:
        print(e)
        return False


def copy_to_2(old_file_path, new_file_path):
    try:
        with open(old_file_path, "rb") as f:
            text = f.read()
            with open(new_file_path, "wb") as f2:
                f2.write(text)
        return True
    except Exception as e:
        print(e)
        return False


def get_file_paths(path) -> list:
    """
    获取文件列表
    :param path:路径
    :return: list
    """
    file_names = []
    root_path = None
    for i in os.walk(path):
        root_path = i[0]
        for ii in i[2]:
            file_names.append(ii)
    pattern_old = ["\\", "/"][int("/" in path)]
    if root_path[-1] != pattern_old:
        root_path += pattern_old
    return [root_path + i for i in file_names]


def copy_all_to(old_path, new_path):
    file_names = []
    root_path = None
    for i in os.walk(old_path):
        root_path = i[0]
        for ii in i[2]:
            file_names.append(ii)

    pattern_old = ["\\", "/"][int("/" in old_path)]
    pattern_new = ["\\", "/"][int("/" in new_path)]
    if root_path[-1] != pattern_old:
        root_path += pattern_old
    if new_path[-1] != pattern_new:
        new_path += pattern_new

    for i in file_names:
        copy_to(root_path + i, new_path + i)


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


def copy_folder(old_path, new_path):
    if not os.path.exists(new_path):
        shutil.copytree(old_path, new_path)
    else:
        shutil.rmtree(new_path)
        shutil.copytree(old_path, new_path)


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
    """
    new_path必须存在！不支持复制空文件夹
    """
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
            print(f"[*]{new_path}{i[0]}", f"{old_path}{i[0]}{i[1]}", f"{new_path}{i[0]}{p2}{i[1]}")
            os.mkdir(f"{new_path}{i[0]}")
            shutil.copy(f"{old_path}{i[0]}{p}{i[1]}", f"{new_path}{i[0]}{p2}{i[1]}")


if __name__ == '__main__':
    # copy_all_to("C:\\Users\\Administrator\\PycharmProjects\\VABT\\data\\",
    #             "C:\\Users\\Administrator\\Desktop\\CV\\InxioCode\\AndroidRequire\\InxioActivities")
    #
    # template_write(
    #     "C:\\Users\\Administrator\\Desktop\\CV\\InxioCode\\AndroidRequire\\InxioActivities\\EventActivity.java",
    #     site="Inxio.cemeye")
    # print(
    #     get_file_paths("C:\\Users\\Administrator\\Desktop\\CV\\InxioCode\\AndroidRequire\\InxioActivities\\")
    # )
    # shutil.copytree(r"C:\Users\Administrator\AndroidStudioProjects\PythonAPP\app\src\main\java\com\cemeye",
    #                 r"C:\Users\Administrator\Desktop\CV\PythonAPP\AndroidRequire\try")
    # only_copy(
    #     r"C:\Users\Administrator\Desktop\copy_test\a",
    #     r"C:\Users\Administrator\Desktop\copy_test\b"
    # )
    print(get_file_paths(r"C:\Users\Administrator\Desktop\CV\PythonAPP"))


    class A:
        def __init__(self):
            ...

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...
