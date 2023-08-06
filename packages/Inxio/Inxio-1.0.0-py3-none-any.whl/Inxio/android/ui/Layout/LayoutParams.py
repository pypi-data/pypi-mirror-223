class LayoutParams:
    def __init__(self, layout):
        self.params = []
        if str(layout) == "GridLayout":
            self.params = [
                "android:layout_column",
                "android:layout_columnSpan",
                "android:layout_columnWeight",
                "android:layout_gravity",
                "android:layout_row",
                "android:layout_rowSpan",
                "android:layout_rowWeight"
            ]
        elif str(layout) == "FrameLayout":
            self.params = []

        elif str(layout) == "LinearLayout":
            self.params = ["android:layout_gravity", "android:layout_weight"]

        elif str(layout) == "RelativeLayout":
            self.params = ["android:layout_above",
                           "android:layout_alignBottom",
                           "android:alignLeft",
                           "android:alignParentBottom",
                           "android:layout_alignParentLeft",
                           "android:layout_alignParentRight",
                           "android:layout_alignParentTop",
                           "android:layout_alignRight",
                           "android:layout_alignTop",
                           "android:layout_below",
                           "android:layout_centerHorizontal",
                           "android:layout_centerInParent",
                           "android:layout_centerVertical",
                           "android:layout_toLeftOf",
                           "android:layout_toRightOf"]

        elif str(layout) == "TableLayout":
            self.params = ["android:layout_gravity", "android:layout_weight"]

    def get_params(self):
        return self.params
