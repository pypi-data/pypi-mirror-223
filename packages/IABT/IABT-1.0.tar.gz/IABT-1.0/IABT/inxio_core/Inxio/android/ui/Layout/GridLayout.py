from Inxio.android.core_components.View import ViewGroup
from Inxio.android.ui.Layout.LayoutParams import LayoutParams


class GridLayout(ViewGroup):
    def __init__(self):
        super().__init__()
        self.append_attributes([
            "xmlns:android",
            "xmlns:tools",
            "android:columnCount",
            "android:orientation",
            "android:rowCount",
            "android:useDefaultMargins",
            "android:alignmentMode",
            "android:rowOrderPreserved",
            "android:columnOrderPreserved",
        ])

        self.set_attribute_value("xmlns:android", "http://schemas.android.com/apk/res/android")
        self.set_attribute_value("xmlns:tools", "http://schemas.android.com/tools")

        self.set_tag_name("GridLayout")

        self.element_params = LayoutParams(self).get_params()

    def append_element(self, element_tag):
        self.append_son_tag(element_tag)


if __name__ == "__main__":
    gl = GridLayout()
    gl.columnCount = "tp://schemas.android"
    print(gl.sting_text)
