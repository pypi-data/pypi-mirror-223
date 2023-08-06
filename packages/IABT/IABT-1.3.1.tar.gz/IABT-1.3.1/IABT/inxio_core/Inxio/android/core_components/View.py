from Inxio.android.core_components.XMLGenerator import XMLTag, SingleXMLTag


class View(XMLTag):
    def __init__(self):
        super().__init__()
        self.append_attributes([
            "android:background",
            "android:clickable",
            "android:elevation",
            "android:id",
            "android:longClickable",
            "android:minHeight",
            "android:minWidth",
            "android:onClick",
            "android:padding",
            "android:paddingBottom",
            "android:paddingEnd",
            "android:paddingLeft",
            "android:paddingRight",
            "android:paddingStart",
            "android:paddingTop",
            "android:visibility",
        ])

    def set_id(self, id_str):
        self.set_attribute_value("android:id", id_str)


class SView(SingleXMLTag):
    def __init__(self):
        super().__init__()
        self.append_attributes([
            "android:background",
            "android:clickable",
            "android:elevation",
            "android:id",
            "android:longClickable",
            "android:minHeight",
            "android:minWidth",
            "android:onClick",
            "android:padding",
            "android:paddingBottom",
            "android:paddingEnd",
            "android:paddingLeft",
            "android:paddingRight",
            "android:paddingStart",
            "android:paddingTop",
            "android:visibility",
        ])

    def set_id(self, id_str):
        self.id = "@+id/" + id_str


class ViewGroup(View):
    def __init__(self):
        super().__init__()
        self.append_attributes([
            "android:layout_marginBottom",
            "android:layout_marginEnd",
            "android:layout_marginLeft",
            "android:layout_marginRight",
            "android:layout_marginStart",
            "android:layout_marginTop",
        ])

    def set_id(self, id_str):
        self.set_attribute_value("android:id", id_str)
