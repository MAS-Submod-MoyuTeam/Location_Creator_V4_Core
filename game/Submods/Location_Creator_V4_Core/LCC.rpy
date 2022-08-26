init -990 python:
    store.mas_submod_utils.Submod(
        author="P",
        name="房间模板V4核心",
        description="房间模板V4的前置子模组.",
        version='1.0.0',
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="房间模板V4核心",
            user_name="MAS-Submod-MoyuTeam",
            repository_name="Location_Creator_V4_Core",
            update_dir="",
            attachment_id=None
        )
init python:
    Location_Manager.start_init()


init -1 python:
    class LocationManager(object):
        def __init__(self):
            self.locations=[]
        def start_init(self):
            for loc in self.locations:
                loc.registed()
        def append(self, datas):
            self.locations.append(datas)
        def set_info(self, location, setting):
            for loc in self.locations:
                if loc.sid == location:
                    loc.update_setting(setting)
    Location_Manager = LocationManager()
    class LCC_NoData(Exception):
        def __init__(self, arg1):
            self.arg1 = arg1
        def __str__(self):
            return "[LCC] 没有 {arg1} 的相关信息"
    class LocationData(object):
        """docstring for LocationData"""
        setting = {
            'disable_progressive': False,
            'hide_masks': False,
            'hide_calendar': True,
            'unlocked': True,
            'entry_pp': None,
            'exit_pp': None,
            'ex_props': None,
            'deco_man': None
        }
        def __init__(self, sid, sname, simgmaps):
            super(LocationData, self).__init__()
            self.sid = sid
            self.sname = sname
            self.simgmaps = simgmaps

        def get_setting(self, keys):
            return self.setting[keys]

        def get_imgdata(self, times ,keys):
            return self.simgmaps[times][keys]
        
        def update_setting(set1):
            return setting.update(set1)

        def registed(self):
            self.registed_data = MASFilterableBackground(
                background_id=self.sid,
                prompt=self.sname,
                image_map=MASFilterWeatherMap(
                    day=MASWeatherMap({
                        store.mas_weather.PRECIP_TYPE_DEF: self.get_imgdata("day", "def"),
                        store.mas_weather.PRECIP_TYPE_RAIN: self.get_imgdata("day", "rain"),
                        store.mas_weather.PRECIP_TYPE_OVERCAST: self.get_imgdata("day", "overcast"),
                        store.mas_weather.PRECIP_TYPE_SNOW: self.get_imgdata("day", "snow"),
                    }),
                    night=MASWeatherMap({
                        store.mas_weather.PRECIP_TYPE_DEF: self.get_imgdata("night", "def"),
                        store.mas_weather.PRECIP_TYPE_RAIN: self.get_imgdata("night", "rain"),
                        store.mas_weather.PRECIP_TYPE_OVERCAST: self.get_imgdata("night", "overcast"),
                        store.mas_weather.PRECIP_TYPE_SNOW: self.get_imgdata("night", "snow"),
                    }),
                    sunset=MASWeatherMap({
                        store.mas_weather.PRECIP_TYPE_DEF: self.get_imgdata("sunset", "def"),
                        store.mas_weather.PRECIP_TYPE_RAIN: self.get_imgdata("sunset", "rain"),
                        store.mas_weather.PRECIP_TYPE_OVERCAST: self.get_imgdata("sunset", "overcast"),
                        store.mas_weather.PRECIP_TYPE_SNOW: self.get_imgdata("sunset", "snow"),
                    }),
                ),
                filter_man=MASBackgroundFilterManager(
                    MASBackgroundFilterChunk(
                        False,
                        None,
                        MASBackgroundFilterSlice.cachecreate(
                            store.mas_sprites.FLT_NIGHT,
                            60
                        )
                    ),
                    MASBackgroundFilterChunk(
                        True,
                        None,
                        MASBackgroundFilterSlice.cachecreate(
                            store.mas_sprites.FLT_SUNSET,
                            60,
                            30*60,
                            10,
                        ),
                        MASBackgroundFilterSlice.cachecreate(
                            store.mas_sprites.FLT_DAY,
                            60
                        ),
                        MASBackgroundFilterSlice.cachecreate(
                            store.mas_sprites.FLT_SUNSET,
                            60,
                            30*60,
                            10,
                        ),
                    ),
                    MASBackgroundFilterChunk(
                        False,
                        None,
                        MASBackgroundFilterSlice.cachecreate(
                            store.mas_sprites.FLT_NIGHT,
                            60
                        )
                    )
                ),
                hide_calendar=self.get_setting("hide_calendar"),
                hide_masks=self.get_setting("hide_masks"),
                disable_progressive=self.get_setting("disable_progressive"),
                unlocked=self.get_setting("unlocked"),
                entry_pp=self.get_setting("entry_pp"),
                exit_pp=self.get_setting("exit_pp"),
                ex_props=self.get_setting("ex_props"),
                deco_man=self.get_setting("deco_man")
            )