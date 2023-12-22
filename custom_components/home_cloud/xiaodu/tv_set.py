from . import XiaoduDeviceBase, XiaoduActions


class XiaoduTVSet(XiaoduDeviceBase):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'TV_SET'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.turnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.getLocation,
            XiaoduActions.incrementVolume,
            XiaoduActions.decrementVolume,
            XiaoduActions.setVolume,
            XiaoduActions.setVolumeMute,
            XiaoduActions.decrementTVChannel,
            XiaoduActions.incrementTVChannel,
            XiaoduActions.setTVChannel,
            XiaoduActions.returnTVChannel
        ], self.get_attribute())

    def get_attribute(self, default_value=None):
        return super().get_attribute([
            self.get_attribute_turnOnState(default_value)
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

    def SetVolume(self, deltaValue):
        super().SetVolume(deltaValue)
        return {'attributes': self.get_attribute()}

    def SetVolumeMute(self, deltaValue):
        super().SetVolumeMute(deltaValue)
        return {'attributes': self.get_attribute()}

    def DecrementVolume(self, deltaValue):
        super().DecrementVolume(deltaValue)
        return {'attributes': self.get_attribute()}

    def IncrementVolume(self, deltaValue):
        super().IncrementVolume(deltaValue)
        return {'attributes': self.get_attribute()}

    def IncrementTVChannel(self):
        super().IncrementTVChannel()
        return {'attributes': self.get_attribute()}

    def DecrementTVChannel(self):
        super().DecrementTVChannel()
        return {'attributes': self.get_attribute()}

    def SetTVChannel(self, deltaValue):
        super().SetTVChannel(deltaValue)
        return {'attributes': self.get_attribute()}

    def ReturnTVChannel(self):
        super().ReturnTVChannel()
        return {'attributes': self.get_attribute()}
