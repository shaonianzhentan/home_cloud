"""Notify.Events platform for notify component."""
from __future__ import annotations

import logging

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TITLE,
    BaseNotificationService,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .manifest import manifest

_LOGGER = logging.getLogger(__name__)

def get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> HomeCloudNotificationService:
    return HomeCloudNotificationService(hass, discovery_info)


class HomeCloudNotificationService(BaseNotificationService):

    def __init__(self, hass, config):
        self.hass = hass

    async def async_send_message(self, message, **kwargs):
        """Send a message."""
        data = kwargs.get(ATTR_DATA) or {}
        title = kwargs.get(ATTR_TITLE)
        image = data.get('image')
        image = None
        if not image:
            # 图片
            msg = {
                'msgtype': 'news',
                "news": {
                    "articles": [
                        {
                            "title": title,
                            "description": message,
                            "url": data.get('url'),
                            "picurl": image
                        }
                    ]
                },
            }
        else:
            # 文本
            msg = {
                'msgtype': 'text',
                'text': {
                    'content': message
                }
            }

        api_cloud = self.hass.data[manifest.domain]
        await api_cloud.sendWecomMsg(msg)