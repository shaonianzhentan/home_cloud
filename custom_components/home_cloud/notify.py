"""Notify.Events platform for notify component."""
from __future__ import annotations
import time
import logging

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TITLE,
    BaseNotificationService,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .utils import call_service
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
        title = kwargs.get(ATTR_TITLE) or time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime())
        image = data.get('image')
        if not image:
            # 文本
            msg = {
                'msgtype': 'text',
                'text': {
                    'content': message
                }
            }
        else:
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

        api_cloud = self.hass.data[manifest.domain]
        res = await api_cloud.sendWecomMsg(msg)
        if res.get('code') != 0:
            _LOGGER.error(res)
            call_service('persistent_notification.create', {
                'title': '微信推送服务异常',
                'message': res['msg']
            })
