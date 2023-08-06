from Inxio.android.ui.Layout.LinearLayout import LinearLayout
from Inxio.android.ui.Layout.LayoutParams import LayoutParams


class TableLayout(LinearLayout):
    def __init__(self):
        super().__init__()
        self.append_attributes([
            "android:collapseColumns",
            "android:shrinkColumns",
            "android:stretchColumns"
        ])

        self.set_tag_name("TableLayout")

        self.element_params = LayoutParams(self).get_params()

    def append_element(self, element_tag):
        self.append_son_tag(element_tag)


if __name__ == "__main__":
    gl = TableLayout()
    gl.collapseColumns = "tp://schemas.android"
    print(gl.sting_text)
