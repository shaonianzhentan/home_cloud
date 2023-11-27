from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .http_skill_tmall import HttpSkillTmall
from .http_skill_xiaoai import HttpSkillXiaoai
from .http_skill_xiaodu import HttpSkillXiaodu
from .http_service_tmall import HttpServiceTmall
from .http_service_xiaoai import HttpServiceXiaoai
from .http_service_xiaodu import HttpServiceXiaodu

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    hass.http.register_view(HttpSkillTmall)
    hass.http.register_view(HttpSkillXiaoai)
    hass.http.register_view(HttpSkillXiaodu)
    hass.http.register_view(HttpServiceTmall)
    hass.http.register_view(HttpServiceXiaoai)
    hass.http.register_view(HttpServiceXiaodu)

    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True

async def update_listener(hass, entry):
    pass

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True