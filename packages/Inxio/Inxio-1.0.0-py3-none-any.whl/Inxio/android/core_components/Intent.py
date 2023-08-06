from android.content import Intent
import java
from Inxio.global_var import PROJECT_DOMAIN


class VIntent:
    def __init__(self, old_activity, new_activity_name):
        """
        Inxio实现Android中的Intent
        :param old_activity: 旧的Activity对象
        :param new_activity_name: 新的Activity名，注意，是绝对标识！
        """
        OCL = java.jclass(PROJECT_DOMAIN + f".{new_activity_name}")
        self.android_intent = Intent(old_activity.java_activity, OCL)

    def setExtraData(self, data_key, data_value):
        self.android_intent.putExtra(data_key, data_value)

    def setExtraDataBundle(self, vbundle):
        self.android_intent.putExtras(vbundle.bundle)
