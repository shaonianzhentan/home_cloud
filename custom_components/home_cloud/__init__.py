from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers import discovery

from .http_skill_tmall import HttpSkillTmall
from .http_skill_xiaoai import HttpSkillXiaoai
from .http_skill_xiaodu import HttpSkillXiaodu
from .http_service_tmall import HttpServiceTmall
from .http_service_xiaoai import HttpServiceXiaoai
from .http_service_xiaodu import HttpServiceXiaodu
from .http_service_wecom import HttpServiceWecom

from .manifest import manifest
from .api_cloud import ApiCloud

PLATFORMS = (
    Platform.SENSOR,
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    hass.http.register_view(HttpSkillTmall)
    hass.http.register_view(HttpSkillXiaoai)
    hass.http.register_view(HttpSkillXiaodu)
    hass.http.register_view(HttpServiceTmall)
    hass.http.register_view(HttpServiceXiaoai)
    hass.http.register_view(HttpServiceXiaodu)
    hass.http.register_view(HttpServiceWecom)

    api_cloud = ApiCloud(hass, entry.data)
    hass.data.setdefault(manifest.domain, {})
    hass.data[manifest.domain] = api_cloud
    hass.async_create_task(api_cloud.login())

    entry.async_on_unload(entry.add_update_listener(update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await discovery.async_load_platform(
        hass,
        Platform.NOTIFY,
        manifest.domain,
        {
            'name': f'{manifest.domain}_wechat',
            'entry_id': entry.entry_id,
            **entry.data
        },
        {},
    )
    return True


async def update_listener(hass, entry):
    pass


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
