"""
1. onCreate()：当Activity被创建时调用，通常在此方法中进行布局的初始化和数据的加载。

2. onStart()：当Activity可见但未获得焦点时调用。

3. onResume()：当Activity获得焦点并开始活动时调用。

4. onPause()：当Activity失去焦点但仍可见时调用，通常在此方法中保存数据和释放资源。

5. onStop()：当Activity不再可见时调用，通常在此方法中释放资源。

6. onDestroy()：当Activity被销毁时调用，通常在此方法中释放所有资源。

7. onRestart()：当Activity从停止状态重新启动时调用。

8. onSaveInstanceState()：当Activity被暂停或销毁前调用，用于保存Activity的状态信息。

9. onRestoreInstanceState()：当Activity被重新创建时调用，用于恢复Activity的状态信息。

10. onActivityResult()：当Activity启动的子Activity返回结果时调用，用于处理返回的结果。

11. onBackPressed()：当用户按下返回键时调用，通常在此方法中处理返回键的逻辑。

12. onBackPressed()：当Activity创建选项菜单时调用，用于创建菜单项。

13. onOptionsItemSelected()：当用户选择菜单项时调用，用于处理菜单项的点击事件。

14. onConfigurationChanged()：当设备配置发生改变时调用，例如旋转屏幕或改变语言设置。

15. onRequestPermissionsResult()：当应用请求权限时调用，用于处理权限请求的结果。

以上是常用的一些方法，还有其他一些方法可以参考Android官方文档。
"""

from Inxio.android.errors.exe_error import *


def PythonUnAllowed(func):
    return func


class ExecutionType:
    onCreate = 15
    onStart = 1
    onResume = 2
    onPause = 3
    onStop = 4
    onDestroy = 5
    onRestart = 6
    onSaveInstanceState = 7
    onRestoreInstanceState = 8
    onActivityResult = 9
    onBackPressed = 10
    onCreateOptionsMenu = 11
    onOptionsItemSelected = 12
    onConfigurationChanged = 13
    onRequestPermissionsResult = 14


class ExecutionBlock:
    def __init__(self):
        self.execution_type = None
        self.activity_name = None
        self.activity_belong = None

    def check_type(self):
        """
        合法性审查，用于检查有没有设置运行类型
        :return:
        """
        if not self.execution_type:
            raise ExeBlockETUnknown("未设置运行块类型！")
        elif not self.activity_name:
            raise ExeBlockActivityNameUnknown("未设置ActivityName")

    def get_execution_type(self):
        """
        获取当前运行块的执行类型
        :return: int
        """
        return self.execution_type

    def get_activity_name(self):
        """
        获取执行在哪个activity?
        :return: str
        """
        return self.activity_name

    def setActivityName(self, name):
        """
        设置当前执行块执行位置
        :param name: str
        :return: None
        """
        self.activity_name = name

    def setExecutionType(self, Type):
        """
        设置执行类型
        :param Type: 数据类ExecutionType.?
        :return: None
        """
        self.execution_type = Type

    @PythonUnAllowed
    def AssignedActivity(self, AndroidActivity):
        """
        外部调用
        为内部的Activity赋值，得到的Java Class 继承自 android.Activity
        :param AndroidActivity: Java Class Expends Activity
        :return: None
        """
        self.activity_belong = AndroidActivity

    def findViewById(self, id_name):
        if self.activity_belong:
            return self.activity_belong.findViewById(id_name=id_name)
        else:
            raise FatalError_ExeBlock_Activity_Not_Found("""    
    致命错误
    在获取控件时未能成功获取属于的Activity
    可能是由于Inxio解释器在编译运行时未能成功为改运行块赋值Activity
    错误原因：
        [可能原因]:此运行块的ActivityName复制错误，请检查.setActivityName()是否正确应用""")

    @PythonUnAllowed
    def RUN(self):
        """
        暴露给Java的接口,用于运行此区块
        :return: None
        """
        # 合法性审查
        self.check_type()
        self.run()

    def run(self):
        """
        需要重写的方法，可以执行自己的函数或调用
        :return:
        """
        ...


if __name__ == "__main__":
    a = ExecutionBlock()
    a.setExecutionType(ExecutionType.onCreate)
    a.setActivityName("MAIN")
    a.RUN()
