from android.app import PendingIntent


def GetJava(func):
    return func


class VPendingIntent:
    """
    FLAG_CANCEL_CURRENT:如果当前系统中已经存在一个相同的PendingIntent对象，那么就将先将已有的PendingIntent取消，然后重新生成一个PendingIntent对象。

    FLAG_NO_CREATE:如果当前系统中不存在相同的PendingIntent对象，系统将不会创建该PendingIntent对象而是直接返回null。

    FLAG_ONE_SHOT:该PendingIntent只作用一次。在该PendingIntent对象通过send()方法触发过后，PendingIntent将自动调用cancel()进行销毁，那么如果你再调用send()方法的话，系统将会返回一个SendIntentException。

    FLAG_UPDATE_CURRENT:如果系统中有一个和你描述的PendingIntent对等的PendingInent，那么系统将使用该PendingIntent对象，但是会使用新的Intent来更新之前PendingIntent中的Intent对象数据，例如更新Intent中的Extras。
    """
    FLAG_ONE_SHOT = 1 << 30
    FLAG_NO_CREATE = 1 << 29
    FLAG_CANCEL_CURRENT = 1 << 28
    FLAG_UPDATE_CURRENT = 1 << 27
    FLAG_IMMUTABLE = 1 << 26
    FLAG_MUTABLE = 1 << 25

    def __init__(self):
        self.android_pending_intent = PendingIntent()
        self.intent_class = PendingIntent

    @GetJava
    def get_android_pending_intent(self):
        """
        如果你是一个Android + Java高手的话，请用此方法获取你熟悉的Android Pending Intent对象
        注意，此方法返回的是一个标准的Java对象，如果需要传入其中参数，请务必在参数外套上标准类型强制
        转换方法。例如，如果需传入一个字符串类型的参数text，你需要在外部套上str()再传入，即传入str(text).
        获取安卓PendingIntent
        :return: Java-PendingInten
        """
        return self.android_pending_intent

    def get_activity(self, activity, requestCode, intent, flags):
        """
        获取Activity
        :param activity:上下文对象
        :param requestCode:请求码
        :param intent:VIntent对象
        :param flags:标志位
        :return:PendingIntent
        """
        return self.intent_class.getActivity(activity.java_activity, requestCode,
                                             intent.android_intent, flags)
