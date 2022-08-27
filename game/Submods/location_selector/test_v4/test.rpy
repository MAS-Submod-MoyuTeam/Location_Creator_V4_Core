# 定义图片
#image mod_assets/location/test_V4/maiteasu_lr_gamedus_day.png = "mod_assets/location/test_V4/maiteasu_lr_gamedus_day.png"

# 初始化阶段不应更改
init -1 python:
    Location_Manager.AddLocation(
        LocationData(
            # 房间id，这个id不能重复
            sid = "test_v4_template",
            # 房间显示名称
            sname = "房间模板v4测试",
            # 房间图片列表
            imgmaps = {
                # 白天
                "day":{
                    # 晴朗
                    "def": "mod_assets/location/test_V4/maiteasu_lr_gamedus_day.png"
                },
                # 晚上
                "night":{
                    "def": "mod_assets/location/test_V4/maiteasu_lr_gamedus_day.png",
                },
            }
        )
    )
    ## 如果你有更改默认设置的需求，请取消以下注释
    #Location_Manager.set_info(
    #    # 要设置的房间id，同你一开始写的
    #    location = "test_v4_template",
    #    # 设置项，以下为默认设置
    #    setting={
    #        # 禁用天气变换
    #        # 原文：weather or not we want to disable progressive weather
    #        #    (Default: None, if hide masks is true and this is not provided, we assume True, otherwise False)
    #        'disable_progressive': None,
    #        # 禁用天气动画
    #        # 原文：weather or not we want to show the windows
    #        'hide_masks': False,
    #        # 隐藏日历
    #        'hide_calendar': True,
    #        # 解锁状态
    #        'unlocked': True,
    #        # 当进入这个房间时，会自动执行entry_pp对应的函数
    #        'entry_pp': None,
    #        # 当离开这个房间时，会自动执行exit_pp对应的函数
    #        'exit_pp': None,
    #        # 背景的额外属性
    #        'ex_props': None,
    #        # MASDecoManager 应该是特定节日的装饰管理器
    #        'deco_man': None
    #    }
    #)

    ## 如果你有更改模板设置的需求，请取消以下注释
    Location_Manager.set_config(
        # 要设置的房间id，同你一开始写的
        location = "test_v4_template",
        # 设置项，以下为默认设置
        setting={
            # 是否启用entry_pp
            'entry_pp_enable': True,
            # 是否启用exit_pp
            'exit_pp_enable': True,
            # 进入房间时的聊天内容 格式为[(1eua, "要说的话"), (2eua, "say something")]，必须先启用entry_pp
            'entry_talk': [("1eua", "好耶！"), ("2eua", "退出对话")],
            # 回到默认房间时的聊天内容，必须先启用exit_pp
            'exit_talk': [("1eua", "好耶！"), ("2eua", "退出对话")],
            # 更换桌面
            'desk_acs': None,
            # simgmaps 文件路径前缀
            'location_assets_prefix': ''
        }
    )