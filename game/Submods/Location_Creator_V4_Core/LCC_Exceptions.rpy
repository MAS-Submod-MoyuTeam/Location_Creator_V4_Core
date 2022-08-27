init -900 python:
    class LCC_NoData(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] {} 数据不存在".format(self.arg1)

    class LCC_FileNotLoadable(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 图片 '{}' 无法加载".format(self.arg1)

    class LCC_SettingCannotBeNone(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 设置项 '{}' 不可为 None".format(self.arg1)
    class LCC_DuplicateBackgroundID(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 重复的房间ID '{}'".format(self.arg1)

    class LCC_FunctionNotCallable(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] '{}' 不是可调用对象".format(self.arg1)

    class LCC_DataIsNotaLocationData(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] '{}' 类型不为LocationData".format(self.arg1)