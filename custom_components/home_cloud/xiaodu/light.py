from . import XiaoduDevice


class XiaoduLight(XiaoduDevice):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)

    def device_info(self):
        device_type = 'LIGHT'
        actions = []
        actions.extend(self.get_actions_mode())
        actions.extend(self.get_actions_switch())
        actions.extend(self.get_actions_light())
        return super().device_info(device_type, actions, self.get_attribute())

    def get_attribute(self):
        attrs = self.get_attribute_base()

        state = self.entity
        color = self.get_attribute_color(state)
        if color is not None:
            attrs.append(color)
        
        brightness = self.get_attribute_brightness(state)
        if brightness is not None:
            attrs.append(brightness)

        colorTemperatureInKelvin = self.get_attribute_colorTemperatureInKelvin(state)
        if colorTemperatureInKelvin is not None:
            attrs.append(colorTemperatureInKelvin)

        return attrs