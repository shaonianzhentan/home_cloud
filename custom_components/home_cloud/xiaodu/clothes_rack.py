from . import XiaoduDeviceBase, XiaoduActions


class XiaoduClothesRack(XiaoduDeviceBase):
    ''' 晾衣架 '''

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'CLOTHES_RACK'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.getLocation,
            XiaoduActions.pause,
            XiaoduActions.incrementHeight,
            XiaoduActions.decrementHeight
        ], self.get_attribute())

    def get_attribute(self):
        return super().get_attribute([
            self.get_attribute_percentage()
        ])

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