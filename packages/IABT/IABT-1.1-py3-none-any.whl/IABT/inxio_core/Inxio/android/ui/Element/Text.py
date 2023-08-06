from Inxio.android.core_components.View import SView
import copy


class TextView(SView):
    def __init__(self, layout):
        super().__init__()
        self.set_tag_name("TextView")
        self.append_attributes(
            [
                "android:autoLink",
                "android:drawableBottom",
                "android:drawableLeft",
                "android:drawableStart",
                "android:drawableRight",
                "android:drawableEnd",
                "android:drawableTop",
                "android:gravity",
                "android:hint",
                "android:inputType",
                "android:singleLine",
                "android:text",
                "android:textColor",
                "android:textSize",
                "android:width",
                "android:height",
                "android:layout_width",
                "android:layout_height"
            ]
        )
        self.append_attributes(copy.copy(layout.element_params))


class EditText(TextView):
    def __init__(self, layout):
        self.set_tag_name("EditText")
        super().__init__(layout=layout)
