"""
将VSP源代码转化为XML代码，即第一次编译
"""
from IABT.translate.xml_generate import XMLTag, DataTag
from IABT.vsp.VSPparser import VSPTab


def _(x):
    return x[1:]


class LayoutTranslator:
    def __init__(self, vsp_root_tag):
        self.vsp_tag = vsp_root_tag
        self.xml_tag = XMLTag()

    def level_traversal(self) -> str:
        """
        层序遍历生成函数
        :return: sth
        """

        def traversal(vsp_tag: VSPTab, root=False, now_father_xml=None):
            if not root:
                self.xml_tag = XMLTag().set_tag_name(vsp_tag.get_name())
                self.xml_tag.add_attr("android", "http://schemas.android.com/apk/res/android", addr="xmlns")
                self.xml_tag.add_attr("tools", "http://schemas.android.com/tools", addr="xmlns")
                self.xml_tag.add_attr("id", "@+id/" + vsp_tag.get_ID(), addr="android")
                for key, value in vsp_tag.get_attributes().items():
                    self.xml_tag.add_attr(_(key), value, addr="android")
                for i in vsp_tag.son:
                    traversal(i, True, now_father_xml=self.xml_tag)

            else:
                new_xml = XMLTag().set_tag_name(vsp_tag.get_name())
                new_xml.add_attr("id", "@+id/" + vsp_tag.get_ID(), addr="android")
                for key, value in vsp_tag.get_attributes().items():
                    new_xml.add_attr(_(key), value, addr="android")
                for i in vsp_tag.son:
                    traversal(i, True, now_father_xml=new_xml)
                now_father_xml.add_son(new_xml)

        traversal(self.vsp_tag, now_father_xml=self.xml_tag)
        return self.xml_tag.generate_string()


class InxioManifest:
    def __init__(self, project_name, main_activity_name, app_name, app_icon):
        self.intent_tag = None

        self.main_activity_name = main_activity_name

        self.set_main()

        self.root_tag = XMLTag().set_tag_name("manifest")
        self.main_attr_dict = {"android": ["http://schemas.android.com/apk/res/android", "xmlns"],
                               "tools": ["http://schemas.android.com/tools", "xmlns"]}
        self.app_attr_dict = {"allowBackup": ["true", "android"],
                              "dataExtractionRules": ["@xml/data_extraction_rules", "android"],
                              "fullBackupContent": ["@xml/backup_rules", "android"],
                              "icon": [f"{app_icon}", "android"],
                              "label": [f"{app_name}", "android"],
                              "supportsRtl": ["true", "android"],
                              "theme": [f"@style/Theme.{project_name}", "android"],
                              "targetApi": ["31", "tools"],
                              }

        self.app_tag = XMLTag().set_tag_name("application").add_attrs(self.app_attr_dict)

    def init(self):
        self.root_tag.add_attrs(self.main_attr_dict)
        return self

    def append_activity(self, activity_IDname):
        if activity_IDname != self.main_activity_name:
            self.app_tag.add_son(
                XMLTag().set_tag_name("activity").add_attr("name", "." + activity_IDname, addr="android").add_attr(
                    "exported", "true", addr="android")
            )
        else:
            self.app_tag.add_son(
                XMLTag().set_tag_name("activity").add_attr("name", "." + activity_IDname, addr="android").add_son(
                    self.intent_tag).add_attr(
                    "exported", "true", addr="android")
            )
        return self

    def append_permission(self, permission_name):
        self.root_tag.add_son(
            XMLTag().set_tag_name("uses-permission").add_attr("name", permission_name, addr="android"))
        return self

    def append_permissions(self, permission_list):
        for i in permission_list:
            self.append_permission(i)
        return self

    def finish(self):
        self.root_tag.add_son(self.app_tag)
        return self

    def append_activities(self, activity_list):
        for i in activity_list:
            self.append_activity(i)
        return self

    def get_str(self):
        return self.root_tag.generate_string()

    def set_main(self):
        self.intent_tag = XMLTag().set_tag_name("intent-filter")
        self.intent_tag.add_son(
            DataTag(DataTag.TAG_TYPE_B).set_tag_name("action").add_attr("name", "android.intent.action.MAIN",
                                                                        addr="android"))
        self.intent_tag.add_son(
            DataTag(DataTag.TAG_TYPE_B).set_tag_name("category").add_attr("name", "android.intent.category.LAUNCHER",
                                                                          addr="android"))


def generate_vm(project_name, activities_list, permission_list, main_activity, icon_path="@mipmap/python",
                app_name="Application"):
    v = InxioManifest(project_name, main_activity, app_name, icon_path).init().append_activities(
        activities_list).append_permissions(permission_list).finish()
    return v.get_str()


if __name__ == "__main__":
    ...
