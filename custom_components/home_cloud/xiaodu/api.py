import re
from homeassistant.core import async_get_hass
from . import XiaoduDeviceBase
from .switch import XiaoduSwitch
from .light import XiaoduLight

class XiaoduDevice(XiaoduDeviceBase):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)

    def get_device(self):
        ''' 获取设备 '''
        domain = self.domain
        if domain == 'switch' or domain == 'input_boolean':
            return XiaoduSwitch(self.entity_id)
        elif domain == 'light':
            return XiaoduLight(self.entity_id)

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

            xiaodu = XiaoduDevice(entity_id)
            device = xiaodu.get_device()

            if name == 'TurnOnRequest':
                attributes = device.TurnOn()
            elif name == 'TurnOffRequest':
                attributes = device.TurnOff()
            elif name == 'TimingTurnOnRequest':
                pass
            elif name == 'TimingTurnOffRequest':
                pass
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
                attributes = device.SetBrightnessPercentage()
            elif name == 'IncrementBrightnessPercentageRequest':
                # 增加亮度
                attributes = device.IncrementBrightnessPercentage()
            elif name == 'DecrementBrightnessPercentageRequest':
                # 减少亮度
                attributes = device.DecrementBrightnessPercentage()
            elif name == 'SetColorRequest':
                pass
            elif name == 'IncrementColorTemperatureRequest':
                # 增加色温
                pass
            elif name == 'DecrementColorTemperatureRequest':
                # 减少色温
                pass
            elif name == 'SetColorTemperatureRequest':
                # 设置色温
                pass
            # 可控温度设备
            elif name == 'IncrementTemperatureRequest':
                pass
            elif name == 'DecrementTemperatureRequest':
                pass
            elif name == 'SetTemperatureRequest':
                pass
            # 设备模式设置
            elif name == 'SetModeRequest':
                pass
            elif name == 'UnsetModeRequest':
                pass
            elif name == 'TimingSetModeRequest':
                pass
            # 可控风速设备
            elif name == 'IncrementFanSpeedRequest':
                pass
            elif name == 'DecrementFanSpeedRequest':
                pass
            elif name == 'SetFanSpeedRequest':
                pass
            # 可控音量设备
            elif name == 'IncrementVolumeRequest':
                pass
            elif name == 'DecrementVolumeRequest':
                pass
            elif name == 'SetVolumeRequest':
                pass
            elif name == 'SetVolumeMuteRequest':
                pass
            # 电视频道设置
            elif name == 'IncrementTVChannelRequest':
                pass
            elif name == 'DecrementTVChannelRequest':
                pass
            elif name == 'SetTVChannelRequest':
                pass
            elif name == 'ReturnTVChannelRequest':
                # 返回上一个观看频道
                pass
            # 可控高度设备
            elif name == 'IncrementHeightRequest':
                pass
            elif name == 'DecrementHeightRequest':
                pass
            # 可控速度设备
            elif name == 'IncrementSpeedRequest':
                pass
            elif name == 'DecrementSpeedRequest':
                pass
            elif name == 'SetSpeedRequest':
                pass
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
            pass
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
