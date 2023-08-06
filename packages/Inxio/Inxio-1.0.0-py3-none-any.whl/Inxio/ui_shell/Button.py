"""
用于UI加壳
"""
from Inxio.android.core_components.View_Listeners import VOnClickListener


class Button:
    def __init__(self, java_button_view):
        self.j_view = java_button_view

        self.click_func = None

    def bind_onclick(self, func):
        self.click_func = func
        self.j_view.setOnClickListener(VOnClickListener().register_onClick(
            lambda view: self.click_func(view)
        ))

    def set_text(self, text):
        self.j_view.setText(text)
