from android.app import AlertDialog
import java
from Inxio.android.core_components.View_Listeners import VDialogClickListener


class Builder:
    def __init__(self, control_activity):
        java_activity = control_activity.java_activity
        self.builder = AlertDialog.Builder(java_activity)

    def set_message(self, text: str):
        """
        为消息对话框设置文字
        :param text: str
        :return: None
        """
        self.builder.setMessage(text)
        return self

    def set_title(self, title: str):
        """
        设置标题
        :param title:str
        :return: None
        """
        self.builder.setTitle(title)
        return self

    def set_positive_button(self, text: str,
                            listener: VDialogClickListener):
        """
        设置对话框的点击按钮
        :param text: 按钮名
        :param listener:
        :return: None
        """
        self.builder.setPositiveButton(text, listener)
        return self

    def showMessage(self):
        """
        显示消息框,进入消息循环
        :return: None
        """
        self.builder.show()
