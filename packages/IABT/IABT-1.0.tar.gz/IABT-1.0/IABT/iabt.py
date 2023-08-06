# -*- coding: utf-8 -*-

import sys
from generate_path import create_paths, create_path, create_files, create_file
from build import *

not_color = False

all_right = True

try:
    from colorama import Fore, Back, init

    init(autoreset=True)
except ModuleNotFoundError:
    import os

    os.system("pip install colorama")
    try:
        import colorama
    except ModuleNotFoundError:
        not_color = True
args = sys.argv[1:]

settings = {"ASP_path": "",
            "project_name": "",
            "project_path": "",
            "site": "com.inxio.example",
            "python_path": str(sys.executable).replace("\\", "/"),
            "build": False,
            "init": False,
            "create_project": False,
            "build_project_path": ""
            }


def show_help():
    print(Fore.YELLOW + "─────────────────────────────────────────────────────────────────────")
    print(Fore.LIGHTBLUE_EX + Back.WHITE + """
                                                     
██╗     █████╗     ██████╗     ████████╗       
██║    ██╔══██╗    ██╔══██╗    ╚══██╔══╝       
██║    ███████║    ██████╔╝       ██║          
██║    ██╔══██║    ██╔══██╗       ██║          
██║    ██║  ██║    ██████╔╝       ██║       ██╗
╚═╝    ╚═╝  ╚═╝    ╚═════╝        ╚═╝       ╚═╝
                                               """)
    print(Fore.LIGHTRED_EX + "        （Inxio Android Build Tools）")
    print(Fore.LIGHTGREEN_EX + """
v.0.0.2
author:cemeye

本代码用于创建、构建你的Inxio项目,以下是代码帮助.""")
    print(Fore.LIGHTWHITE_EX +
          f"""                            
  [*]参数列表:
  -l|--link     :     链接到目标AndroidStudio项目，后面请接参数[AndroidStudio项目路径]
  -n|--name     :     输入项目名称
  -c|--create   :     输入创建的Inxio项目路径
  -h|--help     :     显示帮助
  -i|--init     :     初始化项目（在正常状态下，创建的项目文件都是空白文件，初始化则可以写入文件）
  -s|--site     :     设置域名，默认为com.inxio.example
  -p|--python   :     设置打包目标python.exe源文件{settings["python_path"]}
  
  -build        :     打包项目（此模式下创建项目的-l与-n无效）
  [#]如果您要创建项目，推荐配置:  vabt -c [创建项目路径] -n [项目名称] -i -l [绑定的AndroidStudio项目路径] -s [项目域名]
  如果需要自定义Python.exe，请输入-p参数;
  
  [#]如果您要打包Inxio项目至APK文件，推荐配置：vabt -build [打包的Inxio项目路径]
          """
          )
    print(
        Fore.LIGHTRED_EX + "注意！您需要预先设置环境变量JAVA_HOME，具体方式请自行查找，大体步骤：此电脑->属性->高级系统设置->系统变量")
    print(Fore.YELLOW + "─────────────────────────────────────────────────────────────────────")
    input()


def formal_show_help():
    print(f"""
─────────────────────────────────────────────────────────────────────

██╗     █████╗     ██████╗     ████████╗       
██║    ██╔══██╗    ██╔══██╗    ╚══██╔══╝       
██║    ███████║    ██████╔╝       ██║          
██║    ██╔══██║    ██╔══██╗       ██║          
██║    ██║  ██║    ██████╔╝       ██║       ██╗
╚═╝    ╚═╝  ╚═╝    ╚═════╝        ╚═╝       ╚═╝
                                               
        （Inxio Android Build Tools）
v.0.0.2
author:cemeye

本代码用于创建、构建你的Inxio项目,以下是代码帮助.
  [*]参数列表:
  -l|--link     :     链接到目标AndroidStudio项目，后面请接参数[AndroidStudio项目路径]
  -n|--name     :     输入项目名称
  -c|--create   :     输入创建的Inxio项目路径
  -h|--help     :     显示帮助
  -i|--init     :     初始化项目（在正常状态下，创建的项目文件都是空白文件，初始化则可以写入文件）
  -s|--site     :     设置域名，默认为com.inxio.example
  -p|--python   :     设置打包目标python.exe源文件，默认为{settings["python_path"]}

  - build:     打包项目（此模式下创建项目的-l与-n无效）
  
    [#]如果您要创建项目，推荐配置:  vabt -c [创建项目路径] -n [项目名称] -i -l [绑定的AndroidStudio项目路径] -s [项目域名]，
    如果需要自定义Python.exe，请输入-p参数;

    [#]如果您要打包Inxio项目至APK文件，推荐配置：vabt -build [打包的Inxio项目路径]

    注意！您需要预先设置环境变量JAVA_HOME，具体方式请自行查找，大体步骤：此电脑->属性->高级系统设置->系统变量
─────────────────────────────────────────────────────────────────────
          """)


def create_project(path, project_name):
    root_path = path
    pattern = ["\\", "/"][int("/" in root_path)]
    if root_path[-1] != pattern:
        root_path += pattern
    root_path += project_name
    create_path(root_path)

    path_list = ["src",
                 "resources",
                 "AndroidRequire",
                 "AndroidRequire" + pattern + "ProjectRoot",
                 "AndroidRequire" + pattern + "CompiledLayout",
                 "AndroidRequire" + pattern + "CompiledActivity",
                 "assets",
                 "resources" + pattern + "layout",
                 "resources" + pattern + "drawable",
                 "resources" + pattern + "mipmap",
                 "output"
                 ]

    file_list = [
        [f'{pattern}', "settings.json"],
        [f"{pattern}src{pattern}", "main.py"],
        [f"{pattern}resources{pattern}", "InxioManifest.vsp"]
    ]

    new_path_list = [root_path + pattern + ii for ii in path_list]
    new_file_list = [[root_path + pattern + j[0], j[1]] for j in file_list]

    create_paths(new_path_list)
    create_files(new_file_list)


def init():
    global all_right

    # 写入json文件
    project_path = settings["project_path"]
    project_name = settings["project_name"]
    pattern = ["\\", "/"][int("/" in project_path)]
    json_path = project_path + pattern + settings["project_name"] + pattern + "settings.json"
    pydict = {"project_name": project_name,
              "project_path": project_path,
              "ASP_path": settings["ASP_path"],
              "output_path": project_path + pattern + project_name + pattern + "output",
              "python_path": settings["python_path"],
              "site": settings["site"],
              "include": []}
    write_json(json_path, pydict)
    print(">>>[*]写入JSON文件设置.")

    if project_path[-1] != pattern:
        project_path += pattern

    # 复制，写入文件
    path = r"\\".join(__file__.split(["\\", "/"][int("/" in __file__)])[0:-1]) + r"\\"
    data_path = path + "data\\"
    pf_path = path + "pretreatment_files\\"
    activity_path = project_path + pattern + settings[
        "project_name"] + pattern + "AndroidRequire" + pattern + "ProjectRoot"
    copy_all_to(data_path, activity_path)
    print(">>>[*]复制DATA文件夹，写入文件，")
    vsp_path = path + "InxioManifest.vsp"
    copy_to(vsp_path, f"{project_path}{project_name}{pattern}resources{pattern}InxioManifest.vsp")
    print(">>>[*]复制InxioManifest节点")
    copy_to_2(pf_path + "python.jpg",
              f"{project_path}{project_name}{pattern}resources{pattern}mipmap{pattern}python.jpg")
    print(">>>[*]复制python.jpg图标")

    # 写入模版变量
    for file_path in get_file_paths(activity_path):
        if file_path.split(".")[-1] == "java":
            template_write(file_path, site=settings["site"])
    print(">>>[*]设置模版变量.")

    # 进行 AS-VG 链接
    asp = settings["ASP_path"]
    pattern = ["\\", "/"][int("/" in asp)]
    if asp[-1] != pattern:
        asp += pattern
    print(">>>[*]进行 AS-VG对接")

    # 删除默认生成的MainActivity.java文件
    site = settings["site"].split(".")
    target_path = f"{asp}app{pattern}src{pattern}main{pattern}java{pattern}{site[0]}{pattern}{site[1]}{pattern}{site[2]}{pattern}MainActivity.java"
    try:
        os.remove(target_path)
        print(">>>[*]项目预清洗")
    except Exception as e:
        print(e)
        print(">>>[!]预清洗失败")

    # 项目gradle赋值
    ans_p = copy_to(data_path + "project_build.gradle", asp + "build.gradle")
    print(">>>[*]进行项目gradle赋值 结果:", ans_p)

    # APP gradle赋值
    ans_a = copy_to(data_path + "app_build.gradle", asp + "app" + pattern + "build.gradle")
    if "\\" in settings["python_path"]:
        settings["python_path"] = settings["python_path"].replace("\\", "/")
    pattern = ["\\", "/"][int("/" in settings["project_path"])]
    if settings["project_path"][-1] != pattern:
        settings["project_path"] += pattern
    template_write(asp + "app" + pattern + "build.gradle", site=settings["site"],
                   build_python_path=settings["python_path"],
                   output_path=pydict["output_path"].replace("\\", "/"))
    print(">>>[*]进行APP gradle赋值 结果:", ans_a)

    # 复制接口文件
    print(">>>[*]创建Inxio安卓接口文件、桥接文件")
    p = pattern
    site_list = settings["site"].split(".")
    a1 = copy_to(f"{project_path}{p}{project_name}{p}AndroidRequire{p}ProjectRoot{p}" + "VDialogInterface.java",
                 f"{asp}{p}app{p}src{p}main{p}java{p}com{p}{site_list[1]}{p}{site_list[2]}{p}VDialogInterface.java")
    a2 = copy_to(f"{project_path}{p}{project_name}{p}AndroidRequire{p}ProjectRoot{p}" + "VLocationListener.java",
                 f"{asp}{p}app{p}src{p}main{p}java{p}com{p}{site_list[1]}{p}{site_list[2]}{p}VLocationListener.java")
    a3 = copy_to(f"{project_path}{p}{project_name}{p}AndroidRequire{p}ProjectRoot{p}" + "VOnClickListener.java",
                 f"{asp}{p}app{p}src{p}main{p}java{p}com{p}{site_list[1]}{p}{site_list[2]}{p}VOnClickListener.java")
    a4 = copy_to(f"{project_path}{p}{project_name}{p}AndroidRequire{p}ProjectRoot{p}" + "VSensorEventListener.java",
                 f"{asp}{p}app{p}src{p}main{p}java{p}com{p}{site_list[1]}{p}{site_list[2]}{p}VSensorEventListener.java")

    if all([a1, a2, a3, a4]):
        print(">>>[*]创建桥接文件成功,分别为")
        for i in ["VDialogInterface", "VLocationListener", "VOnClickListener", "VSensorEventListener"]:
            print(i + ".java")
    else:
        all_right = False
        print(">>>[!]创建桥接文件失败！")

    # 创建打包build.bat
    command = f"""cd {settings["ASP_path"]}
.\\gradlew assembleRelease"""
    create_file(settings["project_path"] + settings["project_name"], "build.bat", command)
    print(">>>[*]创建打包build.bat")

    # 复制Inxio核心文件
    inxio_path = r"\\".join(__file__.split(["\\", "/"][int("/" in __file__)])[0:-1]) + r"\\Inxio_core\\Inxio"
    p = ["\\", "/"][int("/" in settings["project_path"])]
    copy_folder(inxio_path, settings["project_path"] + settings["project_name"] + f"{p}AndroidRequire{p}Inxio")

    template_write(settings["project_path"] + settings["project_name"] + f"{p}AndroidRequire{p}Inxio{p}global_var.py",
                   site=settings["site"])

    print(">>>[*]复制Inxio核心文件.")

    if all_right:
        ans = input("[~]是否进行预打包，用于测试是否桥接成功、配置正确(默认为Y)[Y/n]:")
        if ans in ["", "Y", "y", "yes"]:
            os.system('chcp 65001')
            pattern = ["\\", "/"][int("/" in settings["project_path"])]
            os.system(settings["project_path"] + settings["project_name"] + pattern + "build.bat")
        else:
            os.system('chcp 65001')
            print("[$]创建项目完成.DONE.")


def process():
    if settings["create_project"]:
        if settings["project_path"] != "" and settings["project_name"] != "":
            create_project(settings["project_path"], settings["project_name"])
        else:
            print("[!]请至少输入[-c]与[-n]两项参数！")
    if settings["init"]:
        if settings["project_path"] and settings["ASP_path"]:
            init()
        else:
            print("[!]请输入要初始化的项目路径[-c|--create]及链接项目路径[-l|--link]")


if __name__ == "__main__":
    try:
        for index, i in enumerate(args):
            # 以下这些与创建项目、初始化项目有关，与打包项目无关
            if (i == "-l" or i == "--link") and args[index + 1][0] != "-":
                settings["ASP_path"] = args[index + 1]
                print("[*]设置AndroidStudio项目路径.")

            elif (i == "-n" or i == "--name") and args[index + 1][0] != "-":
                settings["project_name"] = args[index + 1]
                settings["create_project"] = True
                print("[*]设置项目名称.")

            elif (i == "-c" or i == "--create") and args[index + 1][0] != "-":
                settings["project_path"] = args[index + 1]
                print("[*]设置项目路径.")

            elif i == "-h" or i == "--help":
                if not_color:
                    formal_show_help()
                else:
                    show_help()

            elif (i == "-s" or i == "--site") and args[index + 1][0] != "-":
                settings["site"] = args[index + 1]
                print("[*]设置项目域名.")

            elif i == "-i" or i == "--init":
                settings["init"] = True
                print("[*]设置项目初始化...")

            elif (i == "-p" or i == "--python") and args[index + 1][0] != "-":
                settings["python_path"] = args[index + 1]
                print("[*]设置项目打包Python环境源地址.")
            # ------------------------------------------------------------
            # 以下这些仅与打包APK有关

            elif i == "-build" and args[index + 1][0] != "-":
                settings["build"] = True
                settings["build_project_path"] = args[index + 1]
                print("[*]开始打包项目")
                build(settings["build_project_path"])

            # ------------------------------------------------------------
            # 以下是杂项

            elif i[0] != "-":
                ...
            else:
                print(f"[!]不知道的参数项[{str(i)}],请输入正确的参数！")
        process()
    except IndexError as e:
        print("[!]请输入正确的参数")
