from android.hardware import SensorEventListener
import java
from Inxio.global_var import PROJECT_DOMAIN


def PythonUnAllowed(func):
    """
    ─=≡Σ(((つ•̀ω•́)つ
    一个完全没有用的装饰器，唯一的作用就是提示你被
    这个装饰器装饰的函数不能再Python中调用！
    :param func: emm
    :return: emm
    """
    return func


class SensorType:
    """
        纯粹得不能在纯粹得数据类，用于存放传感器类型
        TYPE_PRESSURE = 压力传感器
        TYPE_ACCELEROMETER = 加速度传感器
        TYPE_GRAVITY = 重力传感器
        TYPE_LINEAR_ACCELERATION = 线性加速度传感器
        TYPE_GYROSCOPE = 陀螺仪传感器
        TYPE_LIGHT = 光纤传感器
        TYPE_MAGNETIC_FIELD = 磁场传感器
        TYPE_ORIENTATION = 方向传感器
        TYPE_PROXIMITY = 距离传感器
        TYPE_AMBIENT_TEMPERATURE = 温度传感器
        TYPE_RELATIVE_HUMIDITY = 相对湿度传感器
        TYPE_ROTATION_VECTOR = 旋转矢量传感器|
        -----------------------------------------------------------
        TYPE_TEMPERATURE = 被弃用的温度传感器，请使用TYPE_AMBIENT_TEMPERATURE！
        ___________________________________________________________
        !>>下列这些可能不常用，但还是列出来吧

        TYPE_MAGNETIC_FIELD_UNCALIBRATED = 未校准磁场传感器
        TYPE_GAME_ROTATION_VECTOR = 未校准旋转矢量传感器
        TYPE_GYROSCOPE_UNCALIBRATED = 未校准陀螺仪传感器
        TYPE_SIGNIFICANT_MOTION = 重要运动触发传感器
        TYPE_STEP_DETECTOR = 步进检测器传感器
        TYPE_STEP_COUNTER = 步进计数器传感器
        TYPE_GEOMAGNETIC_ROTATION_VECTOR = 地磁旋转矢量
        TYPE_HEART_RATE = 心率监测器
        TYPE_TILT_DETECTOR = 唤醒倾斜探测器传感器
        TYPE_WAKE_GESTURE = 唤醒手势传感器
        TYPE_GLANCE_GESTURE = 唤醒手势传感器

    """
    TYPE_ACCELEROMETER = 1
    TYPE_MAGNETIC_FIELD = 2
    TYPE_ORIENTATION = 3
    TYPE_GYROSCOPE = 4
    TYPE_LIGHT = 5
    TYPE_PRESSURE = 6

    TYPE_TEMPERATURE = 7  # 似乎被弃用

    TYPE_PROXIMITY = 8
    TYPE_GRAVITY = 9
    TYPE_LINEAR_ACCELERATION = 10
    TYPE_ROTATION_VECTOR = 11
    TYPE_RELATIVE_HUMIDITY = 12
    TYPE_AMBIENT_TEMPERATURE = 13

    TYPE_MAGNETIC_FIELD_UNCALIBRATED = 14
    TYPE_GAME_ROTATION_VECTOR = 15
    TYPE_GYROSCOPE_UNCALIBRATED = 16
    TYPE_SIGNIFICANT_MOTION = 17
    TYPE_STEP_DETECTOR = 18
    TYPE_STEP_COUNTER = 19
    TYPE_GEOMAGNETIC_ROTATION_VECTOR = 20
    TYPE_HEART_RATE = 21
    TYPE_TILT_DETECTOR = 22
    TYPE_WAKE_GESTURE = 23
    TYPE_GLANCE_GESTURE = 24

    def __init__(self):
        pass


class VSensor:
    def __init__(self, java_sensor):
        self.sensor = java_sensor

    def getMaximumRange(self):
        """
        最大取值范围
        :return:sth
        """
        return self.sensor.getMaximumRange()

    def getName(self):
        """
        设备名称
        :return:sth
        """
        return self.sensor.getName()

    def getPower(self):
        """
        功率
        :return:sth
        """
        return self.sensor.getPower()

    def getResolution(self):
        """
        精度
        :return:sth
        """
        return self.sensor.getResolution()

    def getType(self):
        """
        传感器类型
        :return:sth
        """
        return self.sensor.getType()

    def getVentor(self):
        """
        设备供应商
        :return:sth
        """
        return self.sensor.getVentor()

    def getVersion(self):
        """
        设备版本号
        :return:sth
        """
        return self.sensor.getVersion()


class VSensorManager:
    # 定义常用常量
    SENSOR_DELAY_FASTEST = 0
    SENSOR_DELAY_GAME = 1
    SENSOR_DELAY_NORMAL = 3
    SENSOR_DELAY_UI = 2

    def __init__(self, java_sensor_manager):
        self.manager = java_sensor_manager

    def get_java_manager(self):
        """
        获取JavaSensorManager
        :return: JavaSensorManager
        """
        return self.manager

    def get_default_sensor(self, sensor_type) -> VSensor:
        """
        获得一个传感器对象
        :param sensor_type:传感器类型，例如 SensorType.TYPE_PRESSURE
        :return: VSensor
        """
        return VSensor(self.manager.getDefaultSensor(sensor_type))

    def registerListener(self, listener, vsensor, sensor_delay_type):
        """
        注册监听器
        :param listener:SensorEventListener-> self
        :param vsensor: VSensor
        :param sensor_delay_type: VSensorManager.SENSOR_DELAY_FASTEST等
        :return: None
        """
        self.manager.registerListener(listener, vsensor.sensor, sensor_delay_type)

    def unregisterListener(self, listener):
        """
        取消注册传感器
        :param listener: SensorEventListener -> self
        :return: None
        """
        self.manager.unregisterListener(listener)


OCL = java.jclass(PROJECT_DOMAIN + ".VSensorEventListener")


class VSensorEventListener(java.dynamic_proxy(OCL)):
    def __init__(self):
        super().__init__()
        self.on_sensor_changed_func = None
        self.on_accuracy_changed_func = None

    @PythonUnAllowed
    def onSensorChanged(self, event):
        if self.on_sensor_changed_func:
            self.on_sensor_changed_func(event)

    @PythonUnAllowed
    def onAccuracyChanged(self, sensor, accuracy):
        if self.on_accuracy_changed_func:
            self.on_accuracy_changed_func(sensor, accuracy)

    def setSensorChanged(self, func):
        self.on_sensor_changed_func = func
        return self

    def setAccuracyChanged(self, func):
        self.on_accuracy_changed_func = func
        return self
