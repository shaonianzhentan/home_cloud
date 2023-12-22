import re
from homeassistant.core import async_get_hass
from . import XiaoduDeviceBase
from .light import XiaoduLight

# switch
from .switch import XiaoduSwitch
from .socket import XiaoduSocket
# Cover
from homeassistant.components.cover import CoverDeviceClass
from .curt_simp import XiaoduCurtSimp
from .curtain import XiaoduCurtCurtain
from .clothes_rack import XiaoduClothesRack
from .window_opener import XiaoduWindowOpener
# Media Player
from .tv_set import XiaoduTVSet

from .air_condition import XiaoduAirCondition


class XiaoduDevice(XiaoduDeviceBase):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)

    def get_device(self):
        ''' 获取设备 '''
        domain = self.domain
        if domain == 'switch' or domain == 'input_boolean':
            if self.device_class == 'plug':
              return XiaoduSocket(self.entity_id)
            else:
              return XiaoduSwitch(self.entity_id)
        elif domain == 'light':
            return XiaoduLight(self.entity_id)
        elif domain == 'cover':
            device_class = self.device_class
            if device_class == CoverDeviceClass.CURTAIN:
                return XiaoduCurtCurtain(self.entity_id)
            elif '晾衣架' in self.friendly_name:
                return XiaoduClothesRack(self.entity_id)
            elif '窗纱' in self.friendly_name or '纱帘' in self.friendly_name:
                return XiaoduCurtSimp(self.entity_id)
            return XiaoduWindowOpener(self.entity_id)
        elif domain == 'media_player':
            device_class = self.device_class
            if device_class == 'tv':
                return XiaoduTVSet(self.entity_id)
        elif domain == 'climate':
            return XiaoduAirCondition(self.entity_id)

class XiaoduParams():

    def __init__(self, payload) -> None:
        # 高度
        if 'deltValue' in payload:
            deltValue = payload.get('deltValue')
            if isinstance(deltValue, dict):
                deltValue = deltValue['value']
            self._deltValue = deltValue
            
        if 'deltaValue' in payload:
            deltaValue = payload.get('deltaValue')
            if isinstance(deltaValue, dict):
                deltaValue = deltaValue['value']
            self._deltaValue = deltaValue
        # 颜色
        if 'color' in payload:
            self._color = payload['color']
        # 色温
        if 'colorTemperatureInKelvin' in payload:
            self._colorTemperatureInKelvin = payload['colorTemperatureInKelvin']
        # 单位秒
        if 'timestamp' in payload:
            self._timestamp = payload['timestamp']
        # 定时
        if 'timeInterval' in payload:
            self._timeInterval = payload['timeInterval']
        # 亮度
        if 'brightness' in payload:
            self._brightness = payload['brightness']['value']
        # 增量百分比
        if 'deltaPercentage' in payload:
            self._deltaPercentage = payload['deltaPercentage']['value']
        # 模式
        if 'mode' in payload:
            self._mode = payload['mode']['value']
        # 风速
        if 'fanSpeed' in payload:
            self._fanSpeed = payload['fanSpeed']['value']
        # 风速
        if 'speed' in payload:
            self._speed = payload['speed']
        # 温度
        if 'targetTemperature' in payload:
            self._targetTemperature = payload['targetTemperature']['value']

    _deltValue = None
    @property
    def deltValue(self):
        ''' 高度 '''
        return self._deltValue

    _deltaValue = None
    @property
    def deltaValue(self):
        ''' 变数 '''
        return self._deltaValue

    _color = None
    @property
    def color(self):
        ''' 颜色 '''
        return self._color

    _colorTemperatureInKelvin = None
    @property
    def colorTemperatureInKelvin(self):
        ''' 色温 '''
        return self._colorTemperatureInKelvin

    _timestamp = None
    @property
    def timestamp(self):
        ''' 单位秒 '''
        return self._timestamp

    _timeInterval = None
    @property
    def timeInterval(self):
        ''' 定时 '''
        return self._timeInterval

    _brightness = None
    @property
    def brightness(self):
        ''' 亮度 '''
        return self._brightness

    _deltaPercentage = None
    @property
    def deltaPercentage(self):
        ''' 百分比 '''
        return self._deltaPercentage

    _mode = None
    @property
    def mode(self):
        ''' 模式 '''
        return self._mode

    _fanSpeed = None
    @property
    def fanSpeed(self):
        ''' 风速 '''
        return self._fanSpeed

    _targetTemperature = None
    @property
    def targetTemperature(self):
        ''' 温度 '''
        return self._targetTemperature
    
    _speed = None
    @property
    def speed(self):
        ''' 速度 '''
        return self._speed

class XiaoduCloud():

    def __init__(self, body) -> None:
        self.hass = async_get_hass()
        self.header = body['header']
        self.payload = body['payload']

    def validate(self, accessToken):
        ''' 授权验证 '''
        if self.payload['accessToken'] != accessToken:
            return self.response('InvalidAccessTokenError', self.payload)

    def filter_entity(self, state):
        ''' 实体过滤 '''
        if state.state == 'unavailable':
            return False

        friendly_name = state.attributes.get('friendly_name')
        if not friendly_name:
            return False
        if re.match(r'^[\u4e00-\u9fff]+$', friendly_name) is None:
            return False
        # 过滤不支持的实体

        return True

    def discovery(self):
        ''' 发现设备 '''
        devices = []
        states = self.hass.states.async_all()
        entities = filter(self.filter_entity, states)
        for entity in entities:
            xiaodu = XiaoduDevice(entity.entity_id)
            device = xiaodu.get_device()
            if not device:
                continue
            devices.append(device.device_info())

        return self.response('DiscoverAppliancesResponse', {'discoveredAppliances': devices})

    def control(self):
        ''' 控制 '''
        attributes = None
        name = self.header['name']
        appliance = self.payload['appliance']
        additionalApplianceDetails = appliance.get(
            'additionalApplianceDetails', {})
        entity_id = appliance['applianceId']
        state = self.hass.states.get(entity_id)
        if state is not None:
            params = XiaoduParams(self.payload)

            xiaodu = XiaoduDevice(entity_id)
            device = xiaodu.get_device()

            if name == 'TurnOnRequest':
                attributes = device.TurnOn()
            elif name == 'TurnOnPercentRequest':
                attributes = device.TurnOnPercent(params.deltValue)
            elif name == 'TurnOffRequest':
                attributes = device.TurnOff()
            elif name == 'TimingTurnOnRequest':
                attributes = device.TimingTurnOn(params.timestamp)
            elif name == 'TimingTurnOffRequest':
                attributes = device.TimingTurnOff(params.timestamp)
            elif name == 'PauseRequest':
                attributes = device.Pause()
            elif name == 'ContinueRequest':
                # 继续
                attributes = device.Continue()
            elif name == 'StartUpRequest':
                # 启动
                attributes = device.StartUp()
            # 可控灯光设备
            elif name == 'SetBrightnessPercentageRequest':
                attributes = device.SetBrightnessPercentage(params.brightness)
            elif name == 'IncrementBrightnessPercentageRequest':
                # 增加亮度
                attributes = device.IncrementBrightnessPercentage(
                    params.brightness)
            elif name == 'DecrementBrightnessPercentageRequest':
                # 减少亮度
                attributes = device.DecrementBrightnessPercentage(
                    params.brightness)
            elif name == 'SetColorRequest':
                attributes = device.SetColor(params.color)
            elif name == 'IncrementColorTemperatureRequest':
                attributes = device.IncrementColorTemperature(params.deltaPercentage)
            elif name == 'DecrementColorTemperatureRequest':
                attributes = device.DecrementColorTemperature(params.deltaPercentage)
            elif name == 'SetColorTemperatureRequest':
                attributes = device.SetColorTemperature(
                    params.colorTemperatureInKelvin)
            # 可控温度设备
            elif name == 'IncrementTemperatureRequest':
                attributes = device.IncrementTemperature(params.deltaValue)
            elif name == 'DecrementTemperatureRequest':
                attributes = device.DecrementTemperature(params.deltaValue)
            elif name == 'SetTemperatureRequest':
                attributes = device.SetTemperature(params.targetTemperature)
            # 设备模式设置
            elif name == 'SetModeRequest':
                attributes = device.SetMode(params.mode)
            elif name == 'UnsetModeRequest':
                attributes = device.UnsetMode(params.mode)
            elif name == 'TimingSetModeRequest':
                attributes = device.TimingSetMode(params.timestamp, params.mode)
            # 可控风速设备
            elif name == 'IncrementFanSpeedRequest':
                attributes = device.IncrementFanSpeed(params.deltaValue)
            elif name == 'DecrementFanSpeedRequest':
                attributes = device.DecrementFanSpeed(params.deltaValue)
            elif name == 'SetFanSpeedRequest':
                attributes = device.SetFanSpeed(params.fanSpeed)
            # 可控音量设备
            elif name == 'IncrementVolumeRequest':
                attributes = device.IncrementVolume(params.deltaValue)
            elif name == 'DecrementVolumeRequest':
                attributes = device.DecrementVolume(params.deltaValue)
            elif name == 'SetVolumeRequest':
                attributes = device.SetVolume(params.deltaValue)
            elif name == 'SetVolumeMuteRequest':
                attributes = device.SetVolume(params.deltaValue)
            # 电视频道设置
            elif name == 'IncrementTVChannelRequest':
                attributes = device.IncrementTVChannel()
            elif name == 'DecrementTVChannelRequest':
                attributes = device.DecrementTVChannel()
            elif name == 'SetTVChannelRequest':
                attributes = device.SetTVChannel(params.deltaValue)
            elif name == 'ReturnTVChannelRequest':
                attributes = device.ReturnTVChannel()
            # 可控高度设备
            elif name == 'IncrementHeightRequest':
                attributes = device.IncrementHeight(params.deltaValue)
            elif name == 'DecrementHeightRequest':
                attributes = device.DecrementHeight(params.deltaValue)
            # 可控速度设备
            elif name == 'IncrementSpeedRequest':
                attributes = device.IncrementSpeed(params.deltaValue)
            elif name == 'DecrementSpeedRequest':
                attributes = device.DecrementSpeed(params.deltaValue)
            elif name == 'SetSpeedRequest':
                attributes = device.SetSpeed(params.speed)
            # 可锁定设备
            elif name == 'SetLockStateRequest':
                pass
            # 打印设备
            elif name == 'SubmitPrintRequest':
                pass
            # 可控吸力设备
            elif name == 'SetSuctionRequest':
                pass
            # 可控水量设备
            elif name == 'SetWaterLevelRequest':
                pass
            # 可控电量设备
            elif name == 'ChargeRequest':
                pass
            elif name == 'DischargeRequest':
                pass
            # 可控方向设备
            elif name == 'SetDirectionRequest':
                pass
            elif name == 'SetCleaningLocationRequest':
                pass
            elif name == 'SetComplexActionsRequest':
                pass
            # 可控定时设备
            elif name == 'SetTimerRequest':
                pass
                # 定时
            elif name == 'TimingCancelRequest':
                pass
                # 取消定时
            # 可复位设备
            elif name == 'ResetRequset':
                pass
            # 可控楼层设备
            elif name == 'SetFloorRequest':
                pass
            elif name == 'IncrementFloorRequest':
                pass
            elif name == 'DecrementFloorRequest':
                pass
            # 可控湿度类设备
            elif name == 'SetHumidityRequest':
                pass

        if attributes is not None:
            return self.response(name.replace('Request', 'Confirmation'), {
                'attributes': attributes
            })

        return self.response('UnsupportedOperationError', {})

    def query(self):
        ''' 查询 '''
        name = self.header['name']
        appliance = self.payload['appliance']
        additionalApplianceDetails = appliance.get(
            'additionalApplianceDetails', {})
        # 实体ID
        entity_id = appliance['applianceId']
        state = self.hass.states.get(entity_id)
        if state is None:
            return {
                'attributes': [
                    {
                        "name": "connectivity",
                        "value": "UNREACHABLE",
                        "scale": "",
                        "timestampOfSample": self.timestampOfSample,
                        "uncertaintyInMilliseconds": 10,
                        "legalValue": "(UNREACHABLE, REACHABLE)"
                    }
                ]
            }

        payload = None
        xiaodu = XiaoduDevice(entity_id)
        device = xiaodu.get_device()

        if name == 'ReportStateRequest':
            # 上报属性
            payload = {
                'attributes': device.get_attribute()
            }
        # 查询设备温度
        elif name == 'GetTemperatureReadingRequest':
            payload = device.GetTemperatureReading()
        elif name == 'GetTargetTemperatureRequest':
            payload = device.GetTargetTemperature()
        # 查询空气质量
        elif name == 'GetHumidityRequest':
            payload = device.GetHumidity()
        elif name == 'GetTargetHumidityRequest':
            payload = device.GetTargetHumidity()
        elif name == 'GetAirQualityIndexRequest':
            pass
        elif name == 'GetAirPM25Request':
            pass
        elif name == 'GetAirPM10Request':
            pass
        elif name == 'GetCO2QuantityRequest':
            pass
        # 查询设备运行参数
        elif name == 'GetRunningTimeRequest':
            pass
        elif name == 'GetTimeLeftRequest':
            pass
        elif name == 'GetRunningStatusRequest':
            pass
        elif name == 'GetStateRequest':
            pass
        elif name == 'GetLocationRequest':
            payload = {
                'attributes': [
                    device.get_attribute_location()
                ]
            }
        # 查询电量
        elif name == 'GetElectricityCapacityRequest':
            pass
        # 查询水质
        elif name == 'GetWaterQualityRequest':
            pass
        # 查询风速
        elif name == 'GetFanSpeedRequest':
            pass
        # 查询速度
        elif name == 'GetSpeedRequest':
            pass
        # 查询运动信息
        elif name == 'GetMotionInfoRequest':
            pass
        # 查询开关状态
        elif name == 'GetTurnOnStateRequest':
            payload = {
                'attributes': [
                    device.get_attribute_turnOnState()
                ]
            }

        if payload is not None:
            return self.response(name.replace('Request', 'Response'), payload)

        return self.response('UnsupportedOperationError', {})

    def response(self, name, payload):
        self.header['name'] = name
        return {'header': self.header, 'payload': payload}
