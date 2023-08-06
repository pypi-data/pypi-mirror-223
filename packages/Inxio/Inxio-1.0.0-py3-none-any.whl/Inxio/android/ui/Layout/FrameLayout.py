from Inxio.android.core_components.XMLGenerator import XMLTag
from Inxio.android.ui.Layout.LayoutParams import LayoutParams


class FrameLayout(XMLTag):
    def __init__(self):
        super().__init__()
        self.append_attributes([
            "xmlns:android",
            "android:foreground",
            "android:foregroundGravity",
        ])

        self.set_attribute_value("xmlns:android", "http://schemas.android.com/apk/res/android")

        self.set_tag_name("FrameLayout")

        self.element_params = LayoutParams(self).get_params()

    def append_element(self, element_tag):
        self.append_son_tag(element_tag)


if __name__ == "__main__":
    gl = FrameLayout()
    print(gl.sting_text)
