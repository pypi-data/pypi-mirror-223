import java
from Inxio.global_var import PROJECT_DOMAIN


def PythonUnAllowed(func):
    """
    ─=≡Σ(((つ•̀ω•́)つ
    一个完全没有用的装饰器，唯一的作用就是提示你被
    这个装饰器装饰的函数不能再Python中调用！
    :param func: emm
    :return: emm
    """
    return func


class VCriteria:
    """
    常量信息:
    NO_REQUIREMENT = 对电量无要求
    POWER_LOW = 低耗电
    POWER_MEDIUM = 中耗电
    POWER_HIGH = 高耗电

    ACCURACY_FINE = 超高精度
    ACCURACY_COARSE = 近似精度
    ACCURACY_LOW = 低精度
    ACCURACY_MEDIUM = 中精度
    ACCURACY_HIGH = 高精度
    """
    NO_REQUIREMENT = 0
    POWER_LOW = 1
    POWER_MEDIUM = 2
    POWER_HIGH = 3

    ACCURACY_FINE = 1
    ACCURACY_COARSE = 2
    ACCURACY_LOW = 1
    ACCURACY_MEDIUM = 2
    ACCURACY_HIGH = 3

    def __init__(self):
        ...


class VLocationManager:
    GPS_PROVIDER = "gps"
    PASSIVE_PROVIDER = "passive"
    FUSED_PROVIDER = "fused"
    NETWORK_PROVIDER = "network"

    KEY_PROXIMITY_ENTERING = "entering"
    KEY_STATUS_CHANGED = "status"
    KEY_PROVIDER_ENABLED = "providerEnabled"
    KEY_LOCATION_CHANGED = "location"
    KEY_LOCATIONS = "locations"
    KEY_FLUSH_COMPLETE = "flushComplete"

    def __init__(self, java_location_manager):
        self.manager = java_location_manager

    def get_java_manager(self):
        """
        获取JavaSensorManager
        :return: JavaSensorManager
        """
        return self.manager

    def get_all_providers(self):
        """
        获取全部可用位置源的字符串列表
        :return: [str,str,str......]
        """
        return list(self.manager.getAllProviders().toArray())

    def getLastKnownLocation(self, provider):
        """
        获取最新的定位，通过provider
        :param provider: VLocationManager.GPS_PROVIDER等
        :return:
        """
        return VLocation(self.manager.getLastKnownLocation(provider))

    def requestLocationUpdates(self, provider,
                               update_interval,
                               space_interval,
                               vlocation_listener):
        """
        传递新的位置对象给vlocation_listener并做出相应的处理
        :param provider:提供者，可用    VLocationManager.**_PROVIDER
        :param update_interval:更新时间间隔（毫秒）
        :param space_interval:空间距离位置间隔（米）
        :param vlocation_listener:VLocationListener
        :return:
        """
        self.manager.requestLocationUpdates(provider, update_interval, space_interval,
                                            vlocation_listener)


OCL = java.jclass(PROJECT_DOMAIN + ".VLocationListener")


class VLocationListener(java.dynamic_proxy(OCL)):
    def __init__(self):
        super().__init__()
        self.on_status_changed_func = None
        self.on_provider_enabled_func = None
        self.on_provider_disabled_func = None
        self.on_location_changed_func = None

    @PythonUnAllowed
    def onLocationChanged(self, location):
        if self.on_location_changed_func:
            self.on_location_changed_func(VLocation(location))

    @PythonUnAllowed
    def onProviderDisabled(self, provider):
        if self.on_provider_disabled_func:
            self.on_provider_disabled_func(provider)

    @PythonUnAllowed
    def onProviderEnabled(self, provider):
        if self.on_provider_enabled_func:
            self.on_provider_enabled_func(provider)

    @PythonUnAllowed
    def onStatusChanged(self, provider, status, extras):
        if self.on_status_changed_func:
            self.on_status_changed_func(provider, status, extras)

    def setLocationChanged(self, func):
        self.on_location_changed_func = func
        return self

    def setProviderDisabled(self, func):
        self.on_provider_disabled_func = func
        return self

    def setProviderEnabled(self, func):
        self.on_provider_enabled_func = func
        return self

    def setStatusChanged(self, func):
        self.on_status_changed_func = func
        return self


class VLocation:
    def __init__(self, java_location):
        self.location = java_location

    def get_longitude(self):
        """
        获取经度
        :return:
        """
        if self.location:
            return str(self.location.getLongitude())

    def get_latitude(self):
        """
        获取纬度
        :return:
        """
        if self.location:
            return str(self.location.getLatitude())

    def get_accuracy(self):
        """
        获取精确度
        :return:
        """
        if self.location:
            return str(self.location.getAccuracy())

    def get_altitude(self):
        """
        获取高度
        :return:
        """
        if self.location:
            return str(self.location.getAltitude())

    def get_bearing(self):
        """
        获取方向
        :return:
        """
        if self.location:
            return str(self.location.getBearing())

    def get_speed(self):
        """
        获取速度
        :return:
        """
        if self.location:
            return str(self.location.getSpeed())
