init -990 python:
    store.mas_submod_utils.Submod(
        author="P",
        name="房间模板V4核心",
        description="房间模板V4的前置子模组.",
        version='1.0.1',
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
    store.LocationManager.start_init()


init -9 python in LocationManager:
    from store import LCC_DataIsNotaLocationData
    from store import LocationData
    debugmode = False
    locations = []
    def debug(msg):
        if not debugmode:
            return
        from store.mas_submod_utils import submod_log
        return submod_log.debug("[LCC] {}".format(msg))
    def start_init():
        for loc in locations:
            loc.init()
    def AddLocation(data):
        if type(data) is not LocationData:
            raise LCC_DataIsNotaLocationData(type(data))
        debug("新location:{}".format(data))
        locations.append(data)
    def set_info(location, setting):
        for loc in locations:
            if loc.sid == location:
                return loc.update_setting(setting)
    def set_config(location, setting):
        for loc in locations:
            if loc.sid == location:
                return loc.update_config(setting)
    def get_location_by_Id(id):
        for loc in locations:
            if loc.sid == id:
                return loc
init -10 python:
    class LocationData(object):
        debugmode=True
        """docstring for LocationData"""
        times = ['day', 'night', 'sunset']
        weather = ['def', 'rain', 'overcast', 'snow']
        
        
        def __new__(cls, sid, sname, imgmaps, config={}, setting={}):
            return super(LocationData, cls).__new__(cls, sid, sname, imgmaps, config={}, setting={})
        def __init__(self, sid, sname, imgmaps, config={}, setting={}):
            self.sid = sid
            self.sname = sname
            self.simgmaps = {}
            self.__template_config = {
            # 是否启用entry_pp
            'entry_pp_enable': False,
            # 是否启用exit_pp
            'exit_pp_enable': False,
            # 进入房间时的聊天内容 格式为(1eua, "要说的话")
            'entry_talk': None,
            # 回到默认房间时的聊天内容
            'exit_talk': None,
            # 更换桌面，文件应该位于mod_assets/monika/t，命名格式为 table-<desk_acs的值>.png，需要启用entry_pp和exit_pp
            'desk_acs': None,
            # 更换椅子，文件应该位于mod_assets/monika/t，命名格式为 chair-<chair_acs的值>.png，需要启用entry_pp和exit_pp
            'chair_acs': None,
            # imgmaps 文件路径前缀
            'location_assets_prefix': ''
            }
            self.__setting = {
            # 禁用天气变换
            'disable_progressive': False,
            # 禁用天气动画
            'hide_masks': False,
            # 隐藏日历
            'hide_calendar': True,
            # 解锁状态
            'unlocked': True,
            # 进入房间时会执行一次entry_pp，需要打开config中对应的enable
            'entry_pp': None,
            # 离开房间后会执行一次exit_pp
            'exit_pp': None,
            # 额外属性
            'ex_props': None,
            # MASDecoManager 应该是特定节日的装饰管理器
            'deco_man': None
            }
            for i in self.times:
                self.simgmaps[i] = {}
                for w in self.weather:
                    self.simgmaps[i][w] = None
                try:
                    self.simgmaps[i].update(imgmaps[i])
                except KeyError as e:
                    pass
            self.debug("ID: {}\nIMG:\n{}".format(self.sid, self.simgmaps))
            self.update_config(config)
            self.update_setting(setting)

        def init(self):
            try:
                self.verify()
                self.init_img()
                self.registed()
            except Exception:
                raise LCC_DuplicateBackgroundID(self.sid)

        def debug(self, msg):
            if not self.debugmode:
                return
            from store.mas_submod_utils import submod_log
            return submod_log.debug("[LCC] {}".format(msg))

        def get_setting(self, keys):
            return self.__setting[keys]
        def get_lcc_config(self, keys):
            return self.__template_config[keys]
        def verify(self):
            # 白天和晚上的图不允许为空
            if self.simgmaps['day']['def'] is None:
                raise LCC_SettingCannotBeNone('day-def')
            if self.simgmaps['night']['def'] is None:
                raise LCC_SettingCannotBeNone('night-def')
            for t in self.times:
                for w in self.weather:
                    if self.simgmaps[t][w] is None:
                        continue
                    self._verify_img(self.simgmaps[t][w])
            if self.get_lcc_config('desk_acs') is not None:
                self._verify_img("mod_assets/monika/t/table-{}.png".format(self.get_lcc_config('desk_acs')))
            if self.get_lcc_config('chair_acs') is not None:
                self._verify_img("mod_assets/monika/t/chair-{}.png".format(self.get_lcc_config('chair_acs')))
        def _verify_img(self, filename):
            if not renpy.loadable(self.get_lcc_config('location_assets_prefix') + filename):
                raise LCC_FileNotLoadable(self.get_lcc_config('location_assets_prefix') + filename)
        def init_img(self):
            self.debug("初始化{}的图片资源".format(self.sid))
            for t in self.times:
                for w in self.weather:
                    if self.simgmaps[t][w] is not None:
                        renpy.display.image.images[(self.get_imgname(t,w),)] = store.Image(
                            self.get_lcc_config('location_assets_prefix') + self.simgmaps[t][w]
                        )
                        self.debug("{} : {}".format(
                            [(self.get_imgname(t,w),)],
                            self.get_lcc_config('location_assets_prefix') + self.simgmaps[t][w]
                        ))
                    else:
                        if t == 'sunset':
                            renpy.display.image.images[(self.get_imgname(t,w),)] = store.Image(
                                self.get_lcc_config('location_assets_prefix') + self.simgmaps['day']['def']
                            )
                            self.debug("{} : {}".format(
                                [(self.get_imgname(t,w),)],
                                self.get_lcc_config('location_assets_prefix') + self.simgmaps['day']['def']
                            ))
                        else:
                            renpy.display.image.images[(self.get_imgname(t,w),)] = store.Image(
                                self.get_lcc_config('location_assets_prefix') + self.simgmaps[t]['def']
                            )
                            self.debug("{} : {}".format(
                                [(self.get_imgname(t,w),)],
                                self.get_lcc_config('location_assets_prefix') + self.simgmaps[t]['def']
                            ))

        def get_imgname(self, times ,keys):
            return "{}_{}_{}".format(
                self.sid,
                times,
                keys
            )
        
        def update_setting(self, set1):
            self.__setting.update(set1)
            self.debug(self.__setting)
            return 
        def update_config(self, set1):
            self.__template_config.update(set1)
            self.debug(self.__template_config)
            return

        def registed(self):
            self.verify()
            self.debug("注册房间:{}".format(self.sid))
            self.registed_data = MASFilterableBackground(
                background_id=self.sid,
                prompt=self.sname,
                image_map=MASFilterWeatherMap(
                    day=MASWeatherMap({
                        store.mas_weather.PRECIP_TYPE_DEF: self.get_imgname("day", "def"),
                        store.mas_weather.PRECIP_TYPE_RAIN: self.get_imgname("day", "rain"),
                        store.mas_weather.PRECIP_TYPE_OVERCAST: self.get_imgname("day", "overcast"),
                        store.mas_weather.PRECIP_TYPE_SNOW: self.get_imgname("day", "snow"),
                    }),
                    night=MASWeatherMap({
                        store.mas_weather.PRECIP_TYPE_DEF: self.get_imgname("night", "def"),
                        store.mas_weather.PRECIP_TYPE_RAIN: self.get_imgname("night", "rain"),
                        store.mas_weather.PRECIP_TYPE_OVERCAST: self.get_imgname("night", "overcast"),
                        store.mas_weather.PRECIP_TYPE_SNOW: self.get_imgname("night", "snow"),
                    }),
                    sunset=MASWeatherMap({
                        store.mas_weather.PRECIP_TYPE_DEF: self.get_imgname("sunset", "def"),
                        store.mas_weather.PRECIP_TYPE_RAIN: self.get_imgname("sunset", "rain"),
                        store.mas_weather.PRECIP_TYPE_OVERCAST: self.get_imgname("sunset", "overcast"),
                        store.mas_weather.PRECIP_TYPE_SNOW: self.get_imgname("sunset", "snow"),
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
                entry_pp=self.entrypp if self.get_lcc_config('entry_pp_enable') else None,
                exit_pp=self.exitpp if self.get_lcc_config('exit_pp_enable') else None,
                ex_props=self.get_setting("ex_props"),
                deco_man=self.get_setting("deco_man")
            )
            
        def entrypp(self, *args ,**kwargs):
            self.debug("entry_pp")
            if self.debugmode:
                for v in args:
                    self.debug('Optional argument (args): {}'.format(v))
                for k, v in kwargs.items():
                    self.debug('Optional argument {} (kwargs): {}'.format(k, v))
            if self.get_setting('entry_pp') is not None:
                a = self.get_setting('entry_pp')
                self.debug("运行自定义pp")
                if not callable(a):
                    raise LCC_FunctionNotCallable(a)
                a()
            self.debug("调整桌面")
            if self.get_lcc_config('desk_acs') is not None:
                store.monika_chr.tablechair.table = self.get_lcc_config('desk_acs')
            if self.get_lcc_config('chair_acs') is not None:
                store.monika_chr.tablechair.table = self.get_lcc_config('chair_acs')
            try:
                kwargs['startup']
            except KeyError:
                kwargs['startup'] = False
            if self.get_lcc_config('entry_talk') and not kwargs['startup']:
                store.persistent.LCC_talking = self.get_lcc_config('entry_talk')
                store.pushEvent('LCC_entry_talk')
        def exitpp(self,*args, **kwargs):
            self.debug("exit_pp")
            if self.debugmode:
                for v in args:
                    self.debug('Optional argument (args): {}'.format(v))
                for k, v in kwargs.items():
                    self.debug('Optional argument {} (kwargs): {}'.format(k, v))
            if self.get_setting('exit_pp') is not None:
                a = self.get_setting('exit_pp')
                self.debug("运行自定义pp")
                if not callable(a):
                    raise LCC_FunctionNotCallable(a)
                a()
            self.debug("调整桌面")
            store.monika_chr.tablechair.table = "def"
            store.monika_chr.tablechair.chair = "def"
            try:
                kwargs['startup']
            except KeyError:
                kwargs['startup'] = False
            if self.get_lcc_config('exit_talk') and not kwargs['startup'] and args == store.mas_background_def:
                store.persistent.LCC_talking = self.get_lcc_config('exit_talk')
                store.pushEvent('LCC_exit_talk')


label LCC_entry_talk:
    python:
        _exp, _talk = renpy.random.choice(store.persistent.LCC_talking)
        renpy.show("monika " + _exp)
        renpy.say(m, _talk)
    return
label LCC_exit_talk:
    python:
        _exp, _talk = renpy.random.choice(store.persistent.LCC_talking)
        renpy.show("monika " + _exp)
        renpy.say(m, _talk)
    return
