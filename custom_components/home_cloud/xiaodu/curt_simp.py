from . import XiaoduDeviceBase, XiaoduActions


class XiaoduCurtSimp(XiaoduDeviceBase):
    ''' 窗纱 '''

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'CURT_SIMP'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.timingTurnOn,
            XiaoduActions.turnOff,
            XiaoduActions.timingTurnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.pause,
            XiaoduActions.incrementHeight,
            XiaoduActions.decrementHeight
        ], self.get_attribute())

    def get_attribute(self):
        return super().get_attribute([
            self.get_attribute_turnOnState(),
            self.get_attribute_percentage()
        ])

    def TurnOn(self, params):
        super().TurnOn(params)
        return {
            'attributes': super().get_attribute([
                self.get_attribute_turnOnState('ON')
            ])
        }

    def TurnOff(self, params):
        super().TurnOff(params)
        return {
            'attributes': super().get_attribute([
                self.get_attribute_turnOnState('OFF')
            ])
        }

    def Pause(self):
        super().Pause()
        return {
            'attributes': self.get_attribute()
        }
    
    def IncrementHeight(self, percentage):
        super().IncrementHeight(percentage)
        return {
            'attributes': self.get_attribute()
        }
    
    def DecrementHeight(self, percentage):
        super().DecrementHeight(percentage)
        return {
            'attributes': self.get_attribute()
        }