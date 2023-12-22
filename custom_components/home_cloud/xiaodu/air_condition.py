from . import XiaoduDevice, XiaoduActions

class XiaoduAirCondition(XiaoduDevice):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'AIR_CONDITION'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.turnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.getLocation,
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
            self.get_attribute_percentage()
        ])


    def IncrementFanSpeed(self):
        return super().IncrementFanSpeed()  