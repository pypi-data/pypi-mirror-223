from file_control import *
from json_control import *
from translate.translator import generate_xml
from file_control import get_file_paths
from vsp.VSPparser import VSP
from translate.vsp2xml import generate_vm


def copy_data_to(project_path, asp_path, site):
    """
    将类似assets、resources文件夹中的东西拷贝到目标项目文件夹
    :param site: 域名
    :param project_path:此项目路径
    :param asp_path:AndroidStudio项目路径
    :return:None
    """
    sl = site.split(".")
    p = ["\\", "/"][int("/" in project_path)]
    if project_path[-1] != p:
        project_path += p
    p2 = ["\\", "/"][int("/" in asp_path)]
    if asp_path[-1] != p2:
        asp_path += p2
    # ------------1.拷贝assets文件夹 --------------
    assets_path = project_path + "assets"
    asp_assets_path = f"{asp_path}app{p2}src{p2}main{p2}assets{p2}"
    copy_folder(assets_path, asp_assets_path)

    # ------------2.拷贝编译后的Layout文件 --------------
    complied_path = f"{project_path}AndroidRequire{p}CompiledLayout{p}"
    asp_layout_path = f"{asp_path}app{p2}src{p2}main{p2}res{p2}layout{p2}"
    copy_folder(complied_path, asp_layout_path)

    # ------------3.拷贝Python代码与Inxio运行库 --------------
    python_src_path = f"{project_path}src{p}"
    asp_src_path = f"{asp_path}app{p2}src{p2}main{p2}python{p}"
    only_copy(python_src_path, asp_src_path, update=True)

    inxio_path = f"{project_path}AndroidRequire{p}Inxio"
    only_copy(inxio_path, asp_src_path + "Inxio")

    # ------------4.拷贝图片资源--------------
    drawable_path = project_path + f"resources{p}drawable{p}"
    tar_drawable_path = f"{asp_path}app{p2}src{p2}main{p2}res{p2}drawable{p}"
    only_copy(drawable_path, tar_drawable_path, )

    # -----------5.拷贝打包好的Activity-----------
    complied_path = f"{project_path}AndroidRequire{p}CompiledActivity{p}"
    asp_src_path = f"{asp_path}app{p2}src{p2}main{p2}java{p2}{sl[0]}{p2}{sl[1]}{p2}{sl[2]}"
    only_copy(complied_path, asp_src_path)

    # -----------6.拷贝mipmap资源-----------
    mipmap_path = project_path + f"resources{p}mipmap{p}"
    tar_mipmap_path = f"{asp_path}app{p2}src{p2}main{p2}res{p2}mipmap-hdpi{p}"
    only_copy(mipmap_path, tar_mipmap_path)


def renew_settings(settings):
    """
    更新ASP项目设置
    :param settings: 项目设置
    :return: None
    """

    project_path = settings["project_path"]

    # 复制，写入文件
    path = r"\\".join(__file__.split(["\\", "/"][int("/" in __file__)])[0:-1]) + r"\\"
    data_path = path + "data\\"

    # 进行 AS-VG 链接
    asp = settings["ASP_path"]
    pattern = ["\\", "/"][int("/" in asp)]
    if asp[-1] != pattern:
        asp += pattern
    print(">>>[*]进行 AS-VG对接")

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
                   output_path=settings["output_path"].replace("\\", "/"))
    print(">>>[*]进行APP gradle赋值 结果:", ans_a)

    # 复制接口文件
    print(">>>[*]创建Inxio安卓接口文件、桥接文件")
    p = pattern
    site_list = settings["site"].split(".")
    a1 = copy_to(f"{project_path}AndroidRequire{p}ProjectRoot{p}" + "VDialogInterface.java",
                 f"{asp}app{p}src{p}main{p}java{p}com{p}{site_list[1]}{p}{site_list[2]}{p}VDialogInterface.java")
    a2 = copy_to(f"{project_path}AndroidRequire{p}ProjectRoot{p}" + "VLocationListener.java",
                 f"{asp}app{p}src{p}main{p}java{p}com{p}{site_list[1]}{p}{site_list[2]}{p}VLocationListener.java")
    a3 = copy_to(f"{project_path}AndroidRequire{p}ProjectRoot{p}" + "VOnClickListener.java",
                 f"{asp}app{p}src{p}main{p}java{p}com{p}{site_list[1]}{p}{site_list[2]}{p}VOnClickListener.java")
    a4 = copy_to(f"{project_path}AndroidRequire{p}ProjectRoot{p}" + "VSensorEventListener.java",
                 f"{asp}app{p}src{p}main{p}java{p}com{p}{site_list[1]}{p}{site_list[2]}{p}VSensorEventListener.java")

    if all([a1, a2, a3, a4]):
        print(">>>[*]更新桥接文件成功,分别为")
        for i in ["VDialogInterface", "VLocationListener", "VOnClickListener", "VSensorEventListener"]:
            print(i + ".java")
    else:
        print(">>>[!]创建桥接文件失败！")


def complain_vsp(project_path):
    """
    编译VSP文件至XML
    :param project_path:项目路径
    :return: None
    """

    def get_file_name(path_str) -> str:
        return path_str.split(["\\", "/"][int("/" in path_str)])[-1]

    def get_file_suffix(path_str):
        return get_file_name(path_str).split(".")[-1]

    def get_file_name_without_s(path_str):
        return get_file_name(path_str).split(".")[0]

    p = ["\\", "/"][int("/" in project_path)]
    if project_path[-1] != p:
        project_path += p

    folder_path = f"{project_path}resources{p}layout{p}"
    compile_path = f"{project_path}AndroidRequire{p}CompiledLayout{p}"

    file_lists = [i for i in get_file_paths(folder_path)]
    for i in file_lists:
        if get_file_suffix(i) == "vsp":
            generate_xml(i, get_file_name_without_s(i) + ".xml", compile_path)
        elif get_file_suffix(i) == "xml":
            copy_to(i, compile_path + get_file_name(i))


def complain_activity(project_path):
    pattern = ["\\", "/"][int("/" in project_path)]
    if project_path[-1] != pattern:
        project_path += pattern

    vm_path = f"{project_path}resources{pattern}InxioManifest.vsp"
    system_vars = VSP(path=vm_path).get_system_vars()  # activity,permission
    activity_list = [i + ".py" for i in system_vars["ACTIVITIES"]]
    activities_check = {i: False for i in activity_list}

    activity_py_list = []

    for file in get_file_paths(f"{project_path}src{pattern}"):
        file_name = file.split(["\\", "/"][int("/" in file)])[-1]
        if file_name in activity_list:
            activities_check[file_name] = True
            activity_py_list.append(file)
    if all(activities_check.values()):
        print(">>>[*]Activity检查通过，确认Activity数目正确无问题。Activity列表如下：")
        for i in activity_list:
            print(f">>>[#]{i}.py ... √")
    else:
        print(f">>>[#]{activities_check}")
        print(">>>[!]Activity检查不通过，请确认Activity数目正确无问题！有问题的Activity列表如下：")
        for key, value in activities_check.items():
            if not value:
                print(f">>>[!]{key}. ... ×")
        print("[!]请确认无误，书写正确，完全实现列表中的Activity后重试.")

    data_path = f"{project_path}AndroidRequire{pattern}ProjectRoot{pattern}"
    compile_path = f"{project_path}AndroidRequire{pattern}CompiledActivity{pattern}"

    for file_path in activity_py_list:
        print(f">>>[○]进行Activity编译，进度：{file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            file_text = f.read()
            file_name = file_path.split(["\\", "/"][int("/" in file_path)])[-1].split(".")[0]
            if "__TYPE_FORMAL__" in file_text:
                copy_to(data_path + "FormalActivity.java", compile_path + f"{file_name}.java")
                print(">>>[●]类型判断:__TYPE_FORMAL__")
            elif "__TYPE_EVENT__" in file_text:
                copy_to(data_path + "EventActivity.java", compile_path + f"{file_name}.java")
                print(">>>[●]类型判断:__TYPE_EVENT__")
            elif "__TYPE_PERMISSION__" in file_text:
                copy_to(data_path + "PermissionActivity.java", compile_path + f"{file_name}.java")
                print(">>>[●]类型判断:__TYPE_PERMISSION__")
            else:
                print(
                    f"[!!]错误！识别不到Activity[{file_path}]的Activity类型！请在文件中添加：__TYPE__ = __TYPE_FORMAL__|__TYPE_EVENT__"
                    f"|__TYPE_PERMISSION__")
            print(">>>[*]进行模版变量填充.")
            template_write(compile_path + f"{file_name}.java", name=file_name)
            print(">>>[☑]编译Activity完成.")


def complain_inxio_manifest(settings):
    project_path = settings["project_path"]
    asp = settings["ASP_path"]
    pattern = ["\\", "/"][int("/" in project_path)]
    p = ["\\", "/"][int("/" in asp)]
    if project_path[-1] != pattern:
        project_path += pattern

    if asp[-1] != p:
        asp += p
    print(">>>[*]准备开始编译inxioManifest节点.Done")

    vm_path = f"{project_path}resources{pattern}InxioManifest.vsp"
    system_vars = VSP(path=vm_path).get_system_vars()  # activity,permission
    activities = system_vars["ACTIVITIES"]
    permissions = system_vars["PERMISSIONS"]
    icon = system_vars["icon"]
    app_name = system_vars["app_name"]
    main_activity_name = system_vars["main_activity"]
    print(f">>>[*]获取信息{activities}, {permissions}, {icon}, {app_name}")
    for i in activities:
        print(f">>>[○]{i}")
    for i in permissions:
        print(f">>>[○]{i}")

    xml_str = generate_vm(settings["project_name"], activities, permissions, main_activity_name, icon_path=icon,
                          app_name=app_name)
    print(">>>[*]生成完毕.")
    with open(f"{asp}app{p}src{p}main{p}AndroidManifest.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(">>>[*]写入文件完毕，路径:" + f"{asp}app{p}src{p}main{p}AndroidManifest.xml")


def package_apk(settings):
    """
    执行打包APK文件命令
    :param settings:设置dict
    :return: None
    """
    os.system('chcp 65001')
    pattern = ["\\", "/"][int("/" in settings["project_path"])]
    pjp = settings["project_path"]
    if pjp[-1] != pattern:
        pjp += pattern
    os.system(f"{pjp}build.bat")


def build(project_path):
    # 基础变量获取、赋值 √√
    pattern = ["\\", "/"][int("/" in project_path)]
    if project_path[-1] != pattern:
        project_path += pattern

    settings = read_json(project_path + "settings.json")
    settings["project_path"] = project_path
    print("[*]", settings)

    # 重新更新设置 √
    renew_settings(settings=settings)
    print("[*]重新更新设置————√")

    # 编译vsp文件至xml文件 √√
    complain_vsp(project_path)
    print("[*]编译vsp文件至xml文件————√")

    # 编译Activity ×
    complain_activity(project_path)
    print("[*]编译Activity————√")

    # 编译InxioManifest.vsp
    complain_inxio_manifest(settings)
    print("[*]编译InxioManifest.vsp————√")

    # 复制文件至AndroidStudio项目中
    copy_data_to(project_path, settings["ASP_path"], settings["site"])
    print("[*]复制文件至AndroidStudio项目中 √")

    # 打包APK
    package_apk(settings)
    print("[*]打包APK √")

    input("按Enter键继续...")
