from Inxio.android.core_components.View import ViewGroup
from Inxio.android.ui.Layout.LayoutParams import LayoutParams


class LinearLayout(ViewGroup):
    def __init__(self):
        super().__init__()
        self.append_attributes([
            "xmlns:android",
            "xmlns:tools",
            "android:orientation",
            "android:gravity",
            "android:layout_width",
            "android:layout_height",
            "android:id",
            "android:background",
        ])
        self.android = "http://schemas.android.com/apk/res/android"
        self.tools = "http://schemas.android.com/tools"

        self.set_tag_name("LinearLayout")

        self.element_params = LayoutParams(self).get_params()

    def append_element(self, element_tag):
        self.append_son_tag(element_tag)


if __name__ == "__main__":
    gl = LinearLayout()
    print(gl.sting_text)
