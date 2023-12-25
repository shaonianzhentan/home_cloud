from . import XiaoduDeviceBase, XiaoduActions


class XiaoduSwitch(XiaoduDeviceBase):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'SWITCH'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.turnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.getLocation
        ], self.get_attribute())

    def get_attribute(self, default_value=None):
        return super().get_attribute([
            self.get_attribute_turnOnState(default_value)
        ])

    def TurnOn(self, params):
        super().TurnOn(params)
        return {
            'attributes': self.get_attribute('ON')
        }

    def TurnOff(self, params):
        super().TurnOff(params)
        return {
            'attributes': self.get_attribute('OFF')
        }