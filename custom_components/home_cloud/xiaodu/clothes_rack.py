from . import XiaoduDeviceBase, XiaoduActions


class XiaoduClothesRack(XiaoduDeviceBase):
    ''' 晾衣架 '''

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)
        self.device_type = 'CLOTHES_RACK'

    def device_info(self):
        return super().device_info(self.device_type, [
            XiaoduActions.turnOn,
            XiaoduActions.turnOff,
            XiaoduActions.getTurnOnState,
            XiaoduActions.pause,
            XiaoduActions.incrementHeight,
            XiaoduActions.decrementHeight
        ], self.get_attribute())

    @property
    def light(self):
        ''' 获取关联的灯泡 '''
        light_id = self.entity.attributes.get('light_id')
        if light_id:
            return self.hass.states.get(light_id)

    def get_attribute(self, default_value=None):
        ''' 获取晾衣架的属性 '''

        if not default_value:
            light = self.light
            if light:
                default_value = 'ON' if light.state == 'on' else 'OFF'

        return super().get_attribute([
            self.get_attribute_turnOnState(default_value),
            self.get_attribute_percentage()
        ])

    def TurnOn(self, params):
        ''' 打开照明 '''
        light = self.light
        if light:
            self.call_service('light', 'turn_on', {
                              'entity_id': light.entity_id})
            return {
                'attributes': self.get_attribute('ON')
            }

    def TurnOff(self, params):
        ''' 关闭照明 '''
        light = self.light
        if light:
            self.call_service('light', 'turn_off', {
                              'entity_id': light.entity_id})
            return {
                'attributes': self.get_attribute('OFF')
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
