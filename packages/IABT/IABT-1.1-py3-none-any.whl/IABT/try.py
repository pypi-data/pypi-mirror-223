from translate.xml_generate import *


class InxioManifest:
    def __init__(self):
        self.root_tag = XMLTag().set_tag_name("manifest")
        self.main_attr_dict = {"android": ["http://schemas.android.com/apk/res/android", "xmlns"],
                               "tools": ["http://schemas.android.com/tools", "xmlns"]}
        self.app_attr_dict = {"allowBackup": ["true", "android"],
                              "dataExtractionRules": ["@xml/data_extraction_rules", "android"],
                              "fullBackupContent": ["@xml/backup_rules", "android"],
                              "icon": ["@mipmap/python", "android"],
                              "label": ["Application", "android"],
                              "supportsRtl": ["true", "android"],
                              "theme": ["@style/Theme.PythonAPP", "android"],
                              "targetApi": ["31", "tools"],
                              }

        self.app_tag = XMLTag().set_tag_name("application").add_attrs(self.app_attr_dict)

    def init(self, project_name, app_name="Application", app_icon="@mipmap/python"):
        self.app_attr_dict["label"] = ["Application", "android"]
        self.app_attr_dict["icon"] = ["@mipmap/python", "android"]
        self.app_attr_dict["theme"] = [f"@style/Theme.{project_name}", "android"]

        self.root_tag.add_attrs(self.main_attr_dict)

        return self

    def append_activity(self, activity_IDname):
        self.app_tag.add_son(
            XMLTag().set_tag_name("activity").add_attr("name", "." + activity_IDname, addr="android")
        )
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


def generate_vm(project_name, activities_list, icon_path="@mipmap/python", app_name="Application"):
    v = InxioManifest().init(project_name, app_name=app_name, app_icon=icon_path).append_activities(
        activities_list
    ).finish()
    return v.get_str()


if __name__ == '__main__':
    # v = InxioManifest().init("PythonAPP").append_activities(
    #     ["Formal", "Event", "Permission"]
    # ).finish()
    #
    # print(v.get_str())
    ...
