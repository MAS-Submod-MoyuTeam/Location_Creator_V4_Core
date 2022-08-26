init -900 python:
    class LCC_NoData(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 没有 {arg1} 的相关信息"

    class LCC_FileNotLoadable(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 图片 '{arg1}' 无法加载"

    class LCC_SettingCannotBeNone(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 属性 '{arg1}' 不允许为None"