from homeassistant.core import async_get_hass, split_entity_id
import time


class XiaoduDevice():

    def __init__(self, entity_id) -> None:
        self.hass = async_get_hass()
        self.entity_id = entity_id
        self.domain = split_entity_id(entity_id)[0]

    @property()
    def entity(self):
        return self.hass.states.get(self.entity_id)

    @property()
    def timestampOfSample(self):
        return int(time.time())

    def get_attribute(self):
        state = self.entity
        if state is None:
            return [
                self.get_attribute_connectivity(state)
            ]

        return [
            self.get_attribute_name(state),
            self.get_attribute_connectivity(state)
        ]

    def get_attribute_name(self, state):
        return {
            "name": "name",
            "value": state.attributes.get('friendly_name'),
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "STRING"
        }

    def get_attribute_connectivity(self, state):
        value = "UNREACHABLE" if state.state == 'unavailable' else "REACHABLE"
        return {
            "name": "connectivity",
            "value": value,
            "scale": "",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "UNREACHABLE, REACHABLE"
        }

    def get_attribute_brightness(self, state):
        value = int(state.attributes.get('brightness', 255) / 255 * 100)
        return {
            "name": "brightness",
            "value": value,
            "scale": "%",
            "timestampOfSample": self.timestampOfSample,
            "uncertaintyInMilliseconds": 10,
            "legalValue": "[0, 100]"
        }

    def get_attribute_powerState(self, state):
        ''' 设备通电状态的属性 '''
        value = "ON" if state.state == 'on' else "OFF"
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

    def get_attribute_percentage(self, state):
        ''' 百分比属性，比如把窗帘关一半，百分比属性值是50%。 '''
        return {
            "name": "percentage",
            "value": 30,
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
        return {
            "name": "colorTemperatureInKelvin",
            "value": 3000,
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

    def get_attribute_turnOnState(self, state):
        ''' 设备的开关状态属性。 '''

        if self.domain == 'cover':
            value = "ON" if state.state == 'open' else "OFF"
        if self.domain == 'media_player':
            value = "ON" if ['off', 'idle'].count(state.state) == 0 else "OFF"
        else:
            value = "ON" if state.state == 'on' else "OFF"

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

    def get_attribute_location(self, state):
        ''' 设备的位置属性。 '''
        return {
            "name": "location",
            "value": "客厅",
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
