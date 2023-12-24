from . import XiaoduDeviceBase, XiaoduActions


class XiaoduLight(XiaoduDeviceBase):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'LIGHT'

    @property
    def brightness(self):
        brightness = self.entity.attributes.get('brightness')
        if not brightness:
            return 0
        return brightness

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.timingTurnOn,
            XiaoduActions.turnOff,
            XiaoduActions.timingTurnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.setBrightnessPercentage,
            XiaoduActions.incrementBrightnessPercentage,
            XiaoduActions.decrementBrightnessPercentage,
            XiaoduActions.setColorTemperature,
            XiaoduActions.setColor,
            XiaoduActions.incrementColorTemperature,
            XiaoduActions.decrementColorTemperature,
        ], self.get_attribute())

    def get_attribute(self, default_value=None):
        return super().get_attribute([
            self.get_attribute_turnOnState(default_value),
            self.get_attribute_brightness(),
            # self.get_attribute_color(),
            self.get_attribute_colorTemperatureInKelvin()
        ])

    def TurnOn(self):
        super().TurnOn()
        return {
            'attributes': self.get_attribute('ON')
        }

    def TurnOff(self):
        super().TurnOff()
        return {
            'attributes': self.get_attribute('OFF')
        }

    def SetBrightnessPercentage(self, percentage):
        brightness = int(self.brightness / 255 * 100)
        super().SetBrightnessPercentage(percentage)
        return {
            "attributes": self.get_attribute(),
            "previousState": {
                "brightness": {
                    "value": brightness
                }
            },
            "brightness": {
                "value": percentage
            }
        }

    def IncrementBrightnessPercentage(self, percentage):

        brightness = int(self.brightness / 255 * 100)
        super().IncrementBrightnessPercentage(percentage)
        return {
            "attributes": self.get_attribute(),
            "previousState": {
                "brightness": {
                    "value": brightness
                }
            },
            "brightness": {
                "value": 100 - percentage
            }
        }

    def DecrementBrightnessPercentage(self, percentage):

        brightness = int(self.brightness / 255 * 100)
        super().DecrementBrightnessPercentage(percentage)
        return {
            "attributes": self.get_attribute(),
            "previousState": {
                "brightness": {
                    "value": brightness
                }
            },
            "brightness": {
                "value": brightness + percentage
            }
        }
    
    def SetColor(self, color):
        super().SetColor(color)
        return {
            "attributes": self.get_attribute()
        }

    def SetColorTemperature(self, colorTemperatureInKelvin):
        super().SetColorTemperature(colorTemperatureInKelvin)
        return {
            "attributes": self.get_attribute()
        }
    
    def DecrementColorTemperature(self, deltaPercentage):
        super().DecrementColorTemperature(deltaPercentage)
        return {
            "attributes": self.get_attribute()
        }
    
    def IncrementColorTemperature(self, deltaPercentage):
        super().IncrementColorTemperature(deltaPercentage)
        return {
            "attributes": self.get_attribute()
        }