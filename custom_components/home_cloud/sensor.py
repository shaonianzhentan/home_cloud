from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.helpers.device_registry import DeviceInfo

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from datetime import datetime
from .manifest import manifest


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HomeCloudSensor(config_entry)])


class HomeCloudSensor(SensorEntity):

    def __init__(self, config_entry):
        self._attr_unique_id = f'{config_entry.entry_id}-homecloud'
        self._attr_name = manifest.name
        self._attr_icon = 'mdi:home-assistant'
        self._attr_device_info = DeviceInfo(
            identifiers={(manifest.domain, config_entry.entry_id)},
            manufacturer="shaonianzhentan",
            model=manifest.domain,
            name=manifest.name,
            sw_version=manifest.version,
        )
        self._attributes = {}

    @property
    def state_attributes(self):
        return self._attributes

    async def async_update(self):
        api_cloud = self.hass.data[manifest.domain]

        self._attr_native_value = '授权成功' if api_cloud._skill_list is not None else '授权失败'
        self._attributes.update({
            'username': api_cloud._username,
            'skill': list(map(lambda x: {
                'name': x['skill_name'],
                'expired': datetime.strptime(x['expired'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            }, api_cloud._skill_list))
        })
