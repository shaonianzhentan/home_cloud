from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .manifest import manifest
from .http_aligenie_view import HttpAligenieView
from .http_xiaoai_view import HttpXiaoaiView

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    hass.http.register_view(HttpAligenieView)
    hass.http.register_view(HttpXiaoaiView)

    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True

async def update_listener(hass, entry):
    pass

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True