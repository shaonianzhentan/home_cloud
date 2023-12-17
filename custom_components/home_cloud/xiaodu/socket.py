from . import XiaoduDevice, XiaoduActions

class XiaoduSocket(XiaoduDevice):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)        
        self.device_type = 'SOCKET'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.timingTurnOn,
            XiaoduActions.turnOff,
            XiaoduActions.timingTurnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.getLocation,
            XiaoduActions.setComplexActions
        ], self.get_attribute())

    def get_attribute(self):
        return super().get_attribute([
            self.get_attribute_turnOnState()
        ])