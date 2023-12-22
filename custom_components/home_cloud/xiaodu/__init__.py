from homeassistant.helpers import template
from homeassistant.core import async_get_hass, split_entity_id
import time


class XiaoduActions():

    turnOn = 'turnOn'  # 打开
    turnOff = 'turnOff'  # 关闭
    timingTurnOn = 'timingTurnOn'  # 定时打开
    timingTurnOff = 'timingTurnOff'  # 定时关闭
    pause = 'pause'  # 暂停
    continue_ = 'continue'  # 继续
    setColor = 'setColor'  # 设置颜色
    setColorTemperature = 'setColorTemperature'  # 设置灯光色温
    incrementColorTemperature = 'incrementColorTemperature'  # 增高灯光色温
    decrementColorTemperature = 'decrementColorTemperature'  # 降低灯光色温
    setBrightnessPercentage = 'setBrightnessPercentage'  # 设置灯光亮度
    incrementBrightnessPercentage = 'incrementBrightnessPercentage'  # 调亮灯光
    decrementBrightnessPercentage = 'decrementBrightnessPercentage'  # 调暗灯光
    setPower = 'setPower'  # 设置功率
    incrementPower = 'incrementPower'  # 增大功率
    decrementPower = 'decrementPower'  # 减小功率
    incrementTemperature = 'incrementTemperature'  # 升高温度
    decrementTemperature = 'decrementTemperature'  # 降低温度
    setTemperature = 'setTemperature'  # 设置温度
    incrementFanSpeed = 'incrementFanSpeed'  # 增加风速
    decrementFanSpeed = 'decrementFanSpeed'  # 减小风速
    setFanSpeed = 'setFanSpeed'  # 设置风速
    setGear = 'setGear'  # 设置档位

    setMode = 'setMode'  # 设置模式
    unSetMode = 'unSetMode'  # 取消设置的模式
    timingSetMode = 'timingSetMode'  # 定时设置模式
    timingUnsetMode = 'timingUnsetMode'  # 定时取消设置的模式

    incrementVolume = 'incrementVolume'  # 调高音量
    decrementVolume = 'decrementVolume'  # 调低音量
    setVolume = 'setVolume'  # 设置音量
    setVolumeMute = 'setVolumeMute'  # 设置静音状态
    decrementTVChannel = 'decrementTVChannel'  # 上一个频道
    incrementTVChannel = 'incrementTVChannel'  # 下一个频道
    setTVChannel = 'setTVChannel'  # 设置频道
    returnTVChannel = 'returnTVChannel'  # 返回上个频道

    chargeTurnOn = 'chargeTurnOn'  # 开始充电
    chargeTurnOff = 'chargeTurnOff'  # 停止充电
    getTurnOnState = 'getTurnOnState'  # 查询开关状态
    getOilCapacity = 'getOilCapacity'  # 查询油量
    getElectricityCapacity = 'getElectricityCapacity'  # 查询电量
    setLockState = 'setLockState'  # 上锁/解锁
    getLockState = 'getLockState'  # 查询锁状态
    setSuction = 'setSuction'  # 设置吸力
    setWaterLevel = 'setWaterLevel'  # 设置水量
    setCleaningLocation = 'setCleaningLocation'  # 设置清扫位置
    setComplexActions = 'setComplexActions'  # 执行自定义复杂动作
    setDirection = 'setDirection'  # 设置移动方向
    submitPrint = 'submitPrint'  # 打印
    getAirPM25 = 'getAirPM25'  # 查询PM2.5
    getAirPM10 = 'getAirPM10'  # 查询PM10
    getCO2Quantity = 'getCO2Quantity'  # 查询二氧化碳含量
    getAirQualityIndex = 'getAirQualityIndex'  # 查询空气质量
    getTemperature = 'getTemperature'  # 查询温度（当前温度和目标温度）
    getTemperatureReading = 'getTemperatureReading'  # 查询当前温度
    getTargetTemperature = 'getTargetTemperature'  # 查询目标温度
    getHumidity = 'getHumidity'  # 查询湿度
    getTargetHumidity = 'getTargetHumidity'  # 查询目标湿度
    getWaterQuality = 'getWaterQuality'  # 查询水质
    getState = 'getState'  # 查询设备所有状态
    getTimeLeft = 'getTimeLeft'  # 查询剩余时间
    getRunningStatus = 'getRunningStatus'  # 查询运行状态
    getRunningTime = 'getRunningTime'  # 查询运行时间
    getLocation = 'getLocation'  # 查询设备所在位置
    setTimer = 'setTimer'  # 设备定时
    timingCancel = 'timingCancel'  # 取消设备定时
    reset = 'reset'  # 设备复位
    incrementHeight = 'incrementHeight'  # 升高高度
    decrementHeight = 'decrementHeight'  # 降低高度
    setSwingAngle = 'setSwingAngle'  # 设置摆风角度
    getFanSpeed = 'getFanSpeed'  # 查询风速
    setHumidity = 'setHumidity'  # 设置湿度模式
    incrementHumidity = 'incrementHumidity'  # 增大湿度
    decrementHumidity = 'decrementHumidity'  # 降低湿度
    incrementMist = 'incrementMist'  # 增大雾量
    decrementMist = 'decrementMist'  # 见效雾量
    setMist = 'setMist'  # 设置雾量
    startUp = 'startUp'  # 设备启动
    setFloor = 'setFloor'  # 设置电梯楼层
    decrementFloor = 'decrementFloor'  # 电梯按下
    incrementFloor = 'incrementFloor'  # 电梯按上
    incrementSpeed = 'incrementSpeed'  # 增加速度
    decrementSpeed = 'decrementSpeed'  # 降低速度
    setSpeed = 'setSpeed'  # 设置速度
    getSpeed = 'getSpeed'  # 获取速度
    getMotionInfo = 'getMotionInfo'  # 获取跑步信息
    turnOnBurner = 'turnOnBurner'  # 打开灶眼
    turnOffBurner = 'turnOffBurner'  # 关闭灶眼
    timingTurnOnBurner = 'timingTurnOnBurner'  # 定时打开灶眼
    timingTurnOffBurner = 'timingTurnOffBurner'  # 定时关闭灶眼


class XiaoduDeviceBase():

    def __init__(self, entity_id) -> None:
        self.hass = async_get_hass()
        self.entity_id = entity_id
        self.domain = split_entity_id(entity_id)[0]
        self.entity = self.hass.states.get(entity_id)

    @property
    def friendly_name(self):
        return self.entity.attributes.get('friendly_name')

    @property
    def device_class(self):
        return self.entity.attributes.get('device_class')

    @property
    def timestampOfSample(self):
        return int(time.time())

    def device_info(self, device_type, actions, attributes):
        ''' 设备信息 '''
        return {
            'applianceId': self.entity_id,
            'friendlyName': self.friendly_name,
            'friendlyDescription': self.friendly_name,
            'additionalApplianceDetails': {},
            'applianceTypes': [device_type],
            'isReachable': True,
            'manufacturerName': 'HomeAssistant',
            'modelName': self.domain,
            'version': '1.0',
            'actions': actions,
            'attributes': attributes
        }

    def call_service(self, domain, service, data):
        self.hass.async_create_task(
            self.hass.services.async_call(domain, service, data))

    def call(self, service, data):
        self.call_service(self.domain, service, data)

    def call_entity(self, service, data={}):
        ''' 调用当前实体ID '''
        data.update({'entity_id': self.entity_id})
        self.call(service, data)

    def TurnOn(self):
        ''' 打开 '''
        service = 'turn_on'
        if self.domain == 'cover':
            service = 'open_cover'
        self.call_entity(service)

    def TurnOnPercent(self, deltValue):
        ''' 打开百分比 '''
        if self.domain == 'cover':
            self.call_entity('set_cover_position', {
                'position': deltValue
            })

    def TurnOff(self):
        ''' 关闭 '''
        service = 'turn_off'
        if self.domain == 'cover':
            service = 'close_cover'
        self.call_entity(service)

    def TimingTurnOn(self, timestamp):
        pass

    def TimingTurnOff(self, timestamp):
        pass

    def Pause(self):
        ''' 暂停 '''
        if self.domain == 'cover':
            self.call_entity('stop_cover')

    def Continue(self):
        pass

    def StartUp(self):
        pass

    def SetBrightnessPercentage(self, brightness):
        self.call_entity('turn_on', {
            'brightness_pct': brightness
        })

    def IncrementBrightnessPercentage(self, brightness):
        self.call_entity('turn_on', {
            'brightness_step_pct': -brightness
        })

    def DecrementBrightnessPercentage(self, brightness):
        self.call_entity('turn_on', {
            'brightness_step_pct': brightness
        })

    def SetColor(self, color):
        pass

    def IncrementColorTemperature(self, deltaPercentage):
        ''' 增加色温 '''
        if self.domain == 'light':
            color_temp_kelvin = self.entity.attributes.get('color_temp_kelvin')
            min_color_temp_kelvin = self.entity.attributes.get(
                'min_color_temp_kelvin')
            max_color_temp_kelvin = self.entity.attributes.get(
                'max_color_temp_kelvin')
            if color_temp_kelvin is not None and min_color_temp_kelvin is not None and max_color_temp_kelvin is not None:
                kelvin = color_temp_kelvin + deltaPercentage * \
                    (max_color_temp_kelvin - min_color_temp_kelvin) / 100
                self.call_entity('turn_on', {
                    'kelvin': kelvin
                })

    def DecrementColorTemperature(self, deltaPercentage):
        ''' 降低色温 '''
        if self.domain == 'light':
            color_temp_kelvin = self.entity.attributes.get('color_temp_kelvin')
            min_color_temp_kelvin = self.entity.attributes.get(
                'min_color_temp_kelvin')
            max_color_temp_kelvin = self.entity.attributes.get(
                'max_color_temp_kelvin')
            if color_temp_kelvin is not None and min_color_temp_kelvin is not None and max_color_temp_kelvin is not None:
                kelvin = color_temp_kelvin - deltaPercentage * \
                    (max_color_temp_kelvin - min_color_temp_kelvin) / 100
                self.call_entity('turn_on', {
                    'kelvin': kelvin
                })

    def SetColorTemperature(self, colorTemperatureInKelvin):
        if self.domain == 'light':
            self.call_entity('turn_on', {
                'kelvin': colorTemperatureInKelvin
            })

    def IncrementTemperature(self, deltaValue):
        ''' 温度高 '''
        if self.domain == 'climate':
            self.call_entity('set_temperature', {
                             'temperature': self.entity.attributes.get('temperature') + deltaValue})

    def DecrementTemperature(self, deltaValue):
        ''' 温度低 '''
        if self.domain == 'climate':
            self.call_entity('set_temperature', {
                             'temperature': self.entity.attributes.get('temperature') - deltaValue})

    def SetTemperature(self, targetTemperature):
        ''' 设置温度 '''
        if self.domain == 'climate':
            self.call_entity('set_temperature', {
                             'temperature': targetTemperature})

    def SetMode(self, mode):
        # 空调
        if self.domain == 'climate':
            '''
            # 上下摆风
            if mode == 'UP_DOWN_SWING':
                self.call_entity('set_swing_mode', {'hvac_mode': mode.lower()})
            # 左右摆风
            elif mode == 'LEFT_RIGHT_SWING':
                self.call_entity('set_swing_mode', {'hvac_mode': mode.lower()})
            '''
            if mode == 'COOL' or mode == 'HEAT' or mode == 'AUTO':
                self.call_entity('set_hvac_mode', {'hvac_mode': mode.lower()})
        elif self.domain == 'media_player':
            if mode == 'MUTE':
                self.call_entity('volume_mute', {'is_volume_muted': True})

    def UnsetMode(self, mode):
        if self.domain == 'climate':
            self.call_entity('set_fan_mode', {'hvac_mode': 'auto'})
        elif self.domain == 'media_player':
            if mode == 'MUTE':
                self.call_entity('volume_mute', {'is_volume_muted': False})

    def TimingSetMode(self, timestamp, mode):
        pass

    def IncrementFanSpeed(self, deltaValue):
        ''' 风速高 '''
        if self.domain == 'climate':
            self.call_entity('set_fan_mode', {'fan_mode': 'high'})

    def DecrementFanSpeed(self, deltaValue):
        ''' 风速低 '''
        if self.domain == 'climate':
            self.call_entity('set_fan_mode', {'fan_mode': 'low'})

    def SetFanSpeed(self, fanSpeed):
        pass

    def IncrementVolume(self, deltaValue):
        if self.domain == 'media_player':
            self.call_entity('volume_up')

    def DecrementVolume(self, deltaValue):
        if self.domain == 'media_player':
            self.call_entity('volume_down')

    def SetVolume(self, deltaValue):
        if self.domain == 'media_player':
            self.call_entity('volume_set', {
                'volume_level': deltaValue / 100
            })

    def SetVolumeMute(self, deltaValue):
        if self.domain == 'media_player':
            self.call_entity('volume_mute', {
                'is_volume_muted': deltaValue == 'on'
            })

    def IncrementTVChannel(self):
        if self.domain == 'media_player':
            self.call_entity('media_previous_track')

    def DecrementTVChannel(self):
        if self.domain == 'media_player':
            self.call_entity('media_next_track')

    def SetTVChannel(self, deltaValue):
        pass

    def ReturnTVChannel(self):
        pass

    def IncrementHeight(self, percentage=None):
        service_data = {'entity_id': self.entity_id}
        ''' 升高 '''
        if self.domain == 'cover':
            if percentage is None:
                self.call('open_cover', service_data)
            else:
                service_data['position'] = percentage
                self.call('set_cover_position', service_data)

    def DecrementHeight(self, percentage=None):
        ''' 降低 '''
        service_data = {'entity_id': self.entity_id}
        if self.domain == 'cover':
            if percentage is None:
                self.call('close_cover', service_data)
            else:
                service_data['position'] = percentage
                self.call('set_cover_position', service_data)

    def IncrementSpeed(self, deltaValue):
        pass

    def DecrementSpeed(self, deltaValue):
        pass

    def SetSpeed(self, speed):
        pass

    def SetLockState(self):
        pass

    def SubmitPrint(self):
        pass

    def SetSuction(self):
        pass

    def SetWaterLevel(self):
        pass

    def Charge(self):
        pass

    def Discharge(self):
        pass

    def SetDirection(self):
        pass

    def SetCleaningLocation(self):
        pass

    def SetComplexActions(self):
        pass

    def SetTimer(self):
        pass

    def TimingCancel(self):
        pass

    def Reset(self):
        pass

    def SetFloor(self):
        pass

    def IncrementFloor(self):
        pass

    def DecrementFloor(self):
        pass

    def SetHumidity(self):
        pass

    def GetTemperatureReading(self):
        pass

    def GetTargetTemperature(self):
        pass

    def GetHumidity(self):
        pass

    def GetTargetHumidity(self):
        pass

    def get_attribute(self, attributes):
        state = self.entity
        if state is None:
            return [
                self.get_attribute_connectivity()
            ]
        _list = list(filter(lambda x: x is not None, attributes))
        _list.extend([
            self.get_attribute_name(),
            self.get_attribute_connectivity(),
            self.get_attribute_location()
        ])
        return _list

    def get_attribute_name(self):
        return {
            "name": "name",
            "value": self.entity.attributes.get('friendly_name'),
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "STRING"
        }

    def get_attribute_connectivity(self):
        value = "UNREACHABLE" if self.entity.state == 'unavailable' else "REACHABLE"
        return {
            "name": "connectivity",
            "value": value,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "UNREACHABLE, REACHABLE"
        }

    def get_attribute_brightness(self):
        brightness = self.entity.attributes.get('brightness')
        if not brightness:
            brightness = 0
        value = int(brightness / 255 * 100)
        return {
            "name": "brightness",
            "value": value,
            "scale": "%",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0, 100]"
        }

    def get_attribute_powerState(self):
        ''' 设备通电状态的属性 '''
        value = "ON" if self.entity.state == 'on' else "OFF"
        return {
            "name": "powerState",
            "value": value,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "(ON, OFF)"
        }

    def get_attribute_powerState(self, state):
        ''' 设备的功率功率属性，比如电磁炉的功率是800w。 '''
        return {
            "name": "powerLevel",
            "value": 30,
            "scale": "W",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "INTEGER"
        }

    def get_attribute_temperature(self, state):
        ''' 设备对应的温度属性，可以指设备本身的温度、周围环境的温度、设备目标温度等等。 '''
        return {
            "name": "temperature",
            "value": 16,
            "scale": "CELSIUS",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[16, 31]"
        }

    def get_attribute_mode(self, state):
        ''' 设备控制模式属性，比如空气净化器的急速模式HIGHSPEED。 '''
        return {
            "name": "mode",
            "value": "HIGHSPEED",
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "(SLEEP, HOME, OUT, AUTO, MANUAL, MUTE, INTELLIGENT, HIGHSPEED, DUST, HCHO_FREE)"
        }

    def get_attribute_humidity(self, state):
        ''' 湿度属性，比如传感器显示的当前空气的湿度。 '''
        return {
            "name": "humidity",
            "value": 22.9,
            "scale": "%",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0.0, 100.0]"
        }

    def get_attribute_airQuality(self, state):
        ''' 空气质量的属性。 '''
        return {
            "name": "airQuality",
            "value": "良",
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "(优, 良, 差, 轻度污染, 中度污染, 重度污染, 严重污染)"
        }

    def get_attribute_pm25(self, state):
        ''' 该属性表示空气中PM2.5的含量。 '''
        return {
            "name": "pm2.5",
            "value": 53.3,
            "scale": "μg/m3",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0.0, 1000.0]"
        }

    def get_attribute_co2(self, state):
        ''' 该属性表示空气中CO2的浓度。 '''
        return {
            "name": "co2",
            "value": 1000,
            "scale": "ppm",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "INTEGER"
        }

    def get_attribute_tovc(self, state):
        ''' 该属性表示空气中总挥发性有机化合物的浓度。 '''
        return {
            "name": "tovc",
            "value": 0.003,
            "scale": "mg/m3",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "DOUBLE"
        }

    def get_attribute_formaldehyde(self, state):
        ''' 该属性表示空气中甲醛的浓度。 '''
        return {
            "name": "formaldehyde",
            "value": 0.003,
            "scale": "mg/m3",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "DOUBLE"
        }

    def get_attribute_percentage(self):
        ''' 百分比属性，比如把窗帘关一半，百分比属性值是50%。 '''
        return {
            "name": "percentage",
            "value": self.entity.attributes.get('current_position') or 0,
            "scale": "%",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0, 100]"
        }

    def get_attribute_color(self, state):
        ''' 设备的颜色，比如智能彩色灯泡，属性值是一个表示颜色的对象。 '''
        return {
            "name": "color",
            "value": {
                "hue": 350.5,
                "saturation": 0.7138,
                "brightness": 0.6524
            },
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "OBJECT"
        }

    def get_attribute_colorTemperatureInKelvin(self, state):
        ''' 设备的色温属性，比如可调白光的灯泡。 '''
        color_temp_kelvin = self.entity.attributes.get('color_temp_kelvin')
        if color_temp_kelvin is not None:
            return {
                "name": "colorTemperatureInKelvin",
                "value": color_temp_kelvin,
                "scale": "K",
                "timestampOfSample": self.timestampOfSample,
                "uncertaintyInMilliseconds": 10,
                "legalValue": "[1000, 10000]"
            }

    def get_attribute_dateTime(self, state):
        ''' 日期和时间属性，比如电饭煲的定时做饭的时间。 '''
        return {
            "name": "dateTime",
            "value": "2018-03-30T11:18:33Z",
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "STRING"
        }

    def get_attribute_turnOnState(self, default_value=None):
        ''' 设备的开关状态属性。 '''

        if default_value is None:
            state = self.entity
            if self.domain == 'cover':
                value = "ON" if state.state == 'open' else "OFF"
            if self.domain == 'media_player':
                value = "ON" if ['off', 'idle'].count(
                    state.state) == 0 else "OFF"
            else:
                value = "ON" if state.state == 'on' else "OFF"
        else:
            value = default_value

        return {
            "name": "turnOnState",
            "value": value,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "(ON, OFF)"
        }

    def get_attribute_pauseState(self, state):
        ''' 设备的暂停属性。 '''
        return {
            "name": "pauseState",
            "value": True,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "BOOLEAN"
        }

    def get_attribute_lockState(self, state):
        ''' 锁的状态属性。 '''
        return {
            "name": "lockState",
            "value": "LOCKED",
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "(LOCKED, UNLOCKED, JAMMED)"
        }

    def get_attribute_electricityCapacity(self, state):
        ''' 设备电池的电量属性。 '''
        return {
            "name": "electricityCapacity",
            "value": 20.5,
            "scale": "%",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0.0, 100.0]"
        }

    def get_attribute_oilCapacity(self, state):
        ''' 设备油箱的油量属性。 '''
        return {
            "name": "oilCapacity",
            "value": 32,
            "scale": "%",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0.0, 100.0]"
        }

    def get_attribute_drivingDistance(self, state):
        ''' 设备可行驶距离属性，比如车里的油可供车行使50.0公里。 '''
        return {
            "name": "drivingDistance",
            "value": 50.0,
            "scale": "公里",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "DOUBLE"
        }

    def get_attribute_fanSpeed(self, state):
        ''' 设备风速值属性，比如把空调风速是2档。 '''
        return {
            "name": "fanSpeed",
            "value": 2,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0, 10]"
        }

    def get_attribute_speed(self, state):
        ''' 设备速度值属性，比如跑步机当前速度多少。 '''
        return {
            "name": "speed",
            "value": 2.0,
            "scale": "KM/H",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0, 10]"
        }

    def get_attribute_motionInfo(self, state):
        ''' 运动信息属性，比如在跑步机上跑了2公里。 eg: 我跑了多久，我跑了多少步，我跑了多少米/千米 '''
        return {
            "name": "motionInfo",
            "value": 2.0,
            "scale": "KM",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": ""
        }

    def get_attribute_channel(self, state):
        ''' 电视频道属性，比如电视3频道。 '''
        return {
            "name": "channel",
            "value": 3,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "INTEGER"
        }

    def get_attribute_muteState(self, state):
        ''' 发声设备当前的静音属性 '''
        return {
            "name": "muteState",
            "value": True,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "BOOLEAN"
        }

    def get_attribute_volume(self, state):
        ''' 设备的音量属性。 '''
        return {
            "name": "volume",
            "value": 50,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0, 100]"
        }

    def get_attribute_suction(self, state):
        ''' 设备的吸力属性。 '''
        return {
            "name": "suction",
            "value": "STANDARD",
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "(STANDARD, STRONG)"
        }

    def get_attribute_waterLevel(self, state):
        ''' 设备的水量属性。 '''
        return {
            "name": "waterLevel",
            "value": "MEDIUM",
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "(LOW, MEDIUM, HIGH)"
        }

    def get_attribute_location(self):
        ''' 设备的位置属性。 '''
        value = self.template("{{area_name('" + self.entity_id + "')}}")
        if not value:
            value = ""
        return {
            "name": "location",
            "value": value,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "STRING"
        }

    def get_attribute_workState(self, state):
        ''' 设备的工作状态属性。 '''
        return {
            "name": "workState",
            "value": "WORKING",
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "(STOP, START, PAUSE, WORKING, WORK_NEARLY_FINISHED, DONE)"
        }

    def template(self, message):
        ''' 模板语法解析 '''
        tpl = template.Template(message, self.hass)
        return tpl.async_render(None)
