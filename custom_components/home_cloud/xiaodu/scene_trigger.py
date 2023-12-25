from . import XiaoduDeviceBase, XiaoduActions


class XiaoduSceneTrigger(XiaoduDeviceBase):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'SCENE_TRIGGER'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn
        ], self.get_attribute())

    def TurnOn(self, params):
        super().TurnOn(params)
        return {
            'attributes': self.get_attribute()
        }