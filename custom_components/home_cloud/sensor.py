from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.helpers.device_registry import DeviceInfo

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
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

    async def async_update(self):
        self._attr_native_value = '状态正常'