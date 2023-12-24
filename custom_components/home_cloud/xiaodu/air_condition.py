from . import XiaoduDeviceBase, XiaoduActions


class XiaoduAirCondition(XiaoduDeviceBase):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'AIR_CONDITION'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.turnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.setMode,
            XiaoduActions.unSetMode,
            XiaoduActions.getFanSpeed,
            XiaoduActions.setFanSpeed,
            XiaoduActions.getTemperature,
            XiaoduActions.setTemperature,
            XiaoduActions.getTargetTemperature
        ], self.get_attribute())

    def get_attribute(self, default_value=None):
        return super().get_attribute([
            self.get_attribute_turnOnState(default_value),
            self.get_attribute_temperature(),
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

    def SetTemperature(self, targetTemperature):
        super().SetTemperature(targetTemperature)
        return {
            'attributes': self.get_attribute()
        }
    
    def IncrementTemperature(self, deltaValue):
        super().IncrementTemperature(deltaValue)
        return {
            'attributes': self.get_attribute()
        }

    def DecrementTemperature(self, deltaValue):
        super().DecrementTemperature(deltaValue)
        return {
            'attributes': self.get_attribute()
        }

    def SetMode(self, mode):
        super().SetMode(mode)
        return {
            'attributes': self.get_attribute()
        }

    def UnsetMode(self, mode):
        super().UnsetMode(mode)
        return {
            'attributes': self.get_attribute()
        }

    def IncrementFanSpeed(self, deltaValue):
        super().IncrementFanSpeed(deltaValue)
        return {
            'attributes': self.get_attribute()
        }

    def DecrementFanSpeed(self, deltaValue):
        super().DecrementFanSpeed(deltaValue)
        return {
            'attributes': self.get_attribute()
        }
