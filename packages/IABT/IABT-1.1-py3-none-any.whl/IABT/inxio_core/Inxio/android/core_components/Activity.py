"""
Inxio运行时程序
提示：
    在Inxio程序书写中，如果发现某个方法是以__External_开头，请不要去调用；这种函数是给外部java的代码去调用的
    这类函数上面都会有@PythonUnAllowed装饰器！

"""
from Inxio.android.core_components.SensorManager import VSensorManager
from Inxio.android.core_components.LocationManager import VLocationManager
from Inxio.android.core_components.NotificationManager import VNotificationManager


def PythonUnAllowed(func):
    """
    ─=≡Σ(((つ•̀ω•́)つ
    一个完全没有用的装饰器，唯一的作用就是提示你被
    这个装饰器装饰的函数不能再Python中调用！
    :param func: emm
    :return: emm
    """
    return func


def Rewritable(func):
    """
    ─=≡Σ(((つ•̀ω•́)つ
    一个完全没有用的装饰器，唯一的作用就是提示你被
    这个装饰器装饰的函数可以重写或者需要被重写！自由发挥吧!
    :param func: emm
    :return: emm
    """
    return func


class R:
    def __init__(self):
        """
        在Android开发中，编译器会自动生成R.class文件，里面存在各种资源
        你可以用这个文件快速获得资源
        我就不详细解释了
        """
        self.resources_list = ["id", "layout", "style", "anim", "animator", "array", "attr", "bool",
                               "color", "dimen",
                               "drawable", "font", "menu", "mipmap", "string"]
        self.id = None
        self.layout = None
        self.style = None
        self.anim = None
        self.animator = None
        self.array = None
        self.attr = None
        self.bool = None
        self.color = None
        self.dimen = None
        self.drawable = None
        self.font = None
        self.menu = None
        self.mipmap = None
        self.string = None

    def if_inited(self) -> bool:
        """
        R类是否被初始化完毕？
        :return: bool
        """
        check_list = []
        for i in self.resources_list:
            check_list.append(eval(f"bool(self.{i})"))

        if all(check_list):
            return True
        elif not all(check_list):
            return False

    def get_resources_types(self) -> list:
        """
        获取全部的资源类型
        :return: list
        """
        return self.resources_list


class _ActivityType:
    FORMAL_TYPE = "FormalActivity.java"
    EVENT_TYPE = "EventActivity.java"
    PERMISSION_TYPE = "PermissionActivity.java"


class _BasedInxioActivity:
    """
    次中央控制器
    附着在每一个Activity的生命进程中，接管了Activity的方法

1. onCreate()：当Activity被创建时调用，通常在此方法中进行布局的初始化和数据的加载。

2. onStart()：当Activity可见但未获得焦点时调用。

3. onResume()：当Activity获得焦点并开始活动时调用。

4. onPause()：当Activity失去焦点但仍可见时调用，通常在此方法中保存数据和释放资源。

5. onStop()：当Activity不再可见时调用，通常在此方法中释放资源。

6. onDestroy()：当Activity被销毁时调用，通常在此方法中释放所有资源。

7. onRestart()：当Activity从停止状态重新启动时调用。

10. onActivityResult()：当Activity启动的子Activity返回结果时调用，用于处理返回的结果。

11. onBackPressed()：当用户按下返回键时调用，通常在此方法中处理返回键的逻辑。

14. onConfigurationChanged()：当设备配置发生改变时调用，例如旋转屏幕或改变语言设置。
    """

    def __init__(self, activity_IDname, APP):
        """
        安卓Activity控制器
        """
        self.sensor_manager = VSensorManager(None)
        self.location_manager = VLocationManager(None)
        self.notification_manager = VNotificationManager(None)

        self.Intent = None
        self.APP = APP
        self.ID = activity_IDname
        self.java_activity = None
        self.R = R()

        self.if_call_super = {
            "onRestart": True,
            "onResume": True,
            "onPause": True,
            "onDestroy": True,
            "onStart": True,
            "onStop": True,
            "onActivityResult": True,
            "onBackPressed": True,
            "onConfigurationChanged": True
        }

        self.activity_type = _ActivityType.FORMAL_TYPE

    @Rewritable
    def onCreate(self, savedInstanceState):
        """
        Activity创建时执行的函数
        如果你的创建函数需要用到savedInstanceState，你可以直接通过这个变量访问
        :param savedInstanceState: 固定参数（不必填！由外部java环境自动赋值）
        :return: None
        """
        ...

    @Rewritable
    def onRestart(self):
        ...

    @Rewritable
    def onResume(self):
        ...

    @Rewritable
    def onPause(self):
        ...

    @Rewritable
    def onDestroy(self):
        ...

    @Rewritable
    def onStart(self):
        ...

    @Rewritable
    def onStop(self):
        ...

    @Rewritable
    def onActivityResult(self, requestCode, resultCode, data):
        """
        重写此函数，获取setResult的结果状态码和额外数据
        :param requestCode:需要的状态码
        :param resultCode: 返回的状态码，用于判断是否是同一个状态码
        :param data: Bundle对象，可以调用get方法
        :return: None
        """
        ...

    @Rewritable
    def onBackPressed(self):
        ...

    @Rewritable
    def onConfigurationChanged(self, newConfig):
        ...

    @PythonUnAllowed
    def External_assignment_Activity(self, java_activity):
        """
        [!]暴露给外部Java的函数，请勿在Python程序中掉用
        在Java中为控制器的Activity赋值
        :param java_activity: Android Activity Class
        :return: None
        """
        self.java_activity = java_activity

    @PythonUnAllowed
    def External_assignment_R(self, java_R, sourse_type):
        """
        在Java中为控制器的R赋值
        :param sourse_type: 资源类型
        :param java_R: Android Activity Class
        :return: None
        """
        array = java_R.entrySet().toArray()
        source = {i.getKey(): i.getValue() for i in array}
        source_type = str(sourse_type).split("$")[1]
        exec(f"self.R.{source_type} = {source}")

    @PythonUnAllowed
    def External_assignment_intent(self, java_intent):
        """
        外部赋值，赋值内容为Intent，可能保存了之前的数据
        :param java_intent: 外部Intent对象
        :return: None
        """
        self.Intent = java_intent

    @PythonUnAllowed
    def External_assignment_sensor_manager(self, sensor_manager):
        """
        外部赋值，赋值传感器
        :param sensor_manager:SensorManager对象
        :return: None
        """
        self.sensor_manager = VSensorManager(sensor_manager)

    @PythonUnAllowed
    def External_assignment_location_manager(self, location_manager):
        """
        外部赋值，赋值传感器
        :param location_manager:LocationManager对象
        :return: None
        """
        self.location_manager = VLocationManager(location_manager)

    @PythonUnAllowed
    def External_assignment_notification_manager(self, notification_manager):
        """
        外部赋值，赋值传感器
        :param notification_manager: NotificationManager对象
        :return: None
        """
        self.notification_manager = VNotificationManager(notification_manager)

    def findViewById(self, id_name):
        """
        通过ID来查找对象
        :param id_name: 对象的ID字符串
        :return:None
        """
        try:
            id = self.R.id[id_name]
            view = self.java_activity.findViewById(id)
            return view

        except KeyError:
            raise Exception(f"未找到id[{id_name}]的对象")

    def finish(self):
        """
        直接结束当前Activity的生命进程
        :return:None
        """
        self.java_activity.finish()

    def setContentView(self, layout_name):
        self.java_activity.setContentView(self.R.layout[layout_name])

    def getBeforeData(self, key):
        """
        获取可能存在的前置数据
        :param key: 键
        :return: None|data
        """
        if self.Intent:
            return self.Intent.getExtras().get(key)
        else:
            return None

    def set_not_call_super(self, target_func_name):
        """
        设置不调用某个Activity活动的父类方法
        注意！请不要随意改动该情况，在某些情况（例如您想实现按两次返回键才退出，就禁用onBackPressed）下，你可以禁用某些函数的父类调用
        可选值：onRestart|onResume|onPause|onDestroy|onStart|onStop|onActivityResult|onBackPressed|onConfigurationChanged

        :param target_func_name: 目标函数名
        :return: None
        """
        self.if_call_super[target_func_name] = False

    def set_result(self, result_code: int, bundle=None):
        """
        设置结果状态码
        :param bundle: 可能存在的额外数据包
        :param result_code: 结果状态码
        :return: None
        """
        intent = self.java_activity.getIntent()
        if bundle:
            intent.putExtras(bundle.bundle)
        self.java_activity.setResult(result_code, intent)

    def get_fragment_manager(self):
        """
        获取【碎片页面】管理器
        :return: .
        """
        return self.java_activity.getFragmentManager()

    @staticmethod
    def begin_fragment_transaction(manager):
        """
        开启一个[fragment]事务
        :return: fragment_transaction
        """
        fm = manager
        return fm.beginTransaction()

    def get_resources(self):
        return self.java_activity.getResources()

    def replace(self, transaction, fragment_old_id, fragment):
        """
        根据参数替换旧的碎片页面为新的碎片页面
        :param transaction: begin_fragment_transaction获取到的事务对象
        :param fragment_old_id: 旧碎片的ID
        :param fragment: 新碎片对象
        :return: None
        """
        transaction.replace(self.findViewById(fragment_old_id), fragment.fragment)

    def get_sensor_manager(self) -> VSensorManager:
        """
        返回传感器管理器
        :return: VSensorManager
        """
        return self.sensor_manager

    def get_location_manager(self) -> VLocationManager:
        """
        返回位置管理器
        :return: VLocationManager
        """
        return self.location_manager

    def get_notification_manager(self) -> VNotificationManager:
        """
        获取通知管理器
        :return: VNotificationManager
        """
        return self.notification_manager


class FormalActivity(_BasedInxioActivity):
    def __init__(self, activity_IDname, APP):
        """
        次中央控制器
        附着在每一个Activity的生命进程中，接管了Activity的方法

        1. onCreate()：当Activity被创建时调用，通常在此方法中进行布局的初始化和数据的加载。

        2. onStart()：当Activity可见但未获得焦点时调用。

        3. onResume()：当Activity获得焦点并开始活动时调用。

        4. onPause()：当Activity失去焦点但仍可见时调用，通常在此方法中保存数据和释放资源。

        5. onStop()：当Activity不再可见时调用，通常在此方法中释放资源。

        6. onDestroy()：当Activity被销毁时调用，通常在此方法中释放所有资源。

        7. onRestart()：当Activity从停止状态重新启动时调用。

        10. onActivityResult()：当Activity启动的子Activity返回结果时调用，用于处理返回的结果。

        11. onBackPressed()：当用户按下返回键时调用，通常在此方法中处理返回键的逻辑。

        14. onConfigurationChanged()：当设备配置发生改变时调用，例如旋转屏幕或改变语言设置。
        """

        super().__init__(activity_IDname, APP)


class EventActivity(_BasedInxioActivity):
    def __init__(self, activity_IDname, APP):
        """
        在FormalActivity的基础上新增六个可重写函数：

        1. onKeyDown   按下按键时的操作
        2. onKeyUp     抬起按键
        3. onKeyLongPress    长按
        4. onKeyShortcut  轻点
        5. onTouchEvent 触摸事件
        6. onTrackballEvent  滑动球

        :param activity_IDname: Activity的唯一标识名称字符串
        :param APP: AndroidAPP对象
        """
        super().__init__(activity_IDname, APP)
        self.activity_type = _ActivityType.EVENT_TYPE

    def onKeyDown(self, key_code, event) -> bool:
        ...

    def onKeyUp(self, key_code, event) -> bool:
        ...

    def onKeyLongPress(self, key_code, event) -> bool:
        ...

    def onKeyShortcut(self, key_code, event) -> bool:
        ...

    def onTouchEvent(self, event) -> bool:
        ...

    def onTrackballEvent(self, event) -> bool:
        ...


class PermissionActivity(EventActivity):
    """
    基于EventActivity，在有事件回调的基础上，新增四大可重写函数

    1. onPermissionsGranted 当权限成功被授予时
    2. onPermissionsDenied 当权限被授予失败时（即用户拒绝了你的请求）
    3. onRationaleAccepted 当提示对话框被点击了确定按钮时调用的方法
    4. onRationaleDenied 当提示对话框被点击了取消按钮时调用的方法
    """

    def __init__(self, activity_IDname, APP):
        super().__init__(activity_IDname, APP)
        self.activity_type = _ActivityType.PERMISSION_TYPE

    def onPermissionsGranted(self, requestCode, permissions):
        """
        当权限成功被授予时
        请注意！只有当你的Activity声明为PermissionRequiredActivity后才能重写此方法！
        :param requestCode:授予成功的请求码
        :param permissions: 返回的权限列表
        :return: None
        """
        ...

    def onPermissionsDenied(self, requestCode, permissions):
        """
        当权限被授予失败时（即用户拒绝了你的请求）
        请注意！只有当你的Activity声明为PermissionActivity后才能重写此方法！
        :param requestCode:授予失败的请求码
        :param permissions: 返回的权限列表
        :return: None
        """
        ...

    def onRationaleAccepted(self, requestCode):
        """
        当提示对话框被点击了确定按钮时调用的方法
        :param requestCode: 请求码
        :return: None
        """

        ...

    def onRationaleDenied(self, requestCode):
        """
        当提示对话框被点击了取消按钮时调用的方法
        :param requestCode: 请求码
        :return: None
        """
        ...
