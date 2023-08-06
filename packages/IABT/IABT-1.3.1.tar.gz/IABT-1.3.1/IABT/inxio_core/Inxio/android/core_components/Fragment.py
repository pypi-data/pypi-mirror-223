from android.app import Fragment
import java
from Inxio.global_var import PROJECT_DOMAIN


class VFragment:
    def __init__(self, fragment_name):
        self.fragment = java.jclass(PROJECT_DOMAIN + f".{fragment_name}")
