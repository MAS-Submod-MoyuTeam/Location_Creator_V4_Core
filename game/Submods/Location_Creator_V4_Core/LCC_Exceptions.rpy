init -900 python:
    class LCC_NoData(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 没有 {} 的相关信息".format(arg1)

    class LCC_FileNotLoadable(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 图片 '{}' 无法加载".format(arg1)

    class LCC_SettingCannotBeNone(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 属性 '{}' 不允许为None".format(arg1)