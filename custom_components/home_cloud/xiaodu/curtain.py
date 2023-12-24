from . import XiaoduDeviceBase, XiaoduActions


class XiaoduCurtCurtain(XiaoduDeviceBase):
    ''' 窗帘 '''

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'CURTAIN'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.turnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.pause
        ], self.get_attribute())

    def get_attribute(self, default_value=None):
        return super().get_attribute([
            self.get_attribute_turnOnState(default_value),
            self.get_attribute_percentage()
        ])

    def TurnOn(self):
        super().TurnOn()
        return {
            'attributes': self.get_attribute('ON')
        }
    
    def TurnOnPercent(self, deltValue):
        super().TurnOnPercent(deltValue)
        return {
            'attributes': self.get_attribute('ON')
        }

    def TurnOff(self):
        super().TurnOff()
        return {
            'attributes': self.get_attribute('OFF')
        }

    def Pause(self):
        super().Pause()
        return {
            'attributes': self.get_attribute('ON')
        }