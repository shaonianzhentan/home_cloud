from . import XiaoduDeviceBase, XiaoduActions


class XiaoduSwitch(XiaoduDeviceBase):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'SWITCH'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.timingTurnOn,
            XiaoduActions.turnOff,
            XiaoduActions.timingTurnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.getLocation
        ], self.get_attribute())

    def get_attribute(self):
        return super().get_attribute([
            self.get_attribute_turnOnState()
        ])

    def TurnOn(self):
        super().TurnOn()
        return {
            'attributes': super().get_attribute([
                self.get_attribute_turnOnState('ON')
            ])
        }

    def TurnOff(self):
        super().TurnOff()
        return {
            'attributes': super().get_attribute([
                self.get_attribute_turnOnState('OFF')
            ])
        }