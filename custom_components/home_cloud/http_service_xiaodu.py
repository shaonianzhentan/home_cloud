import json
import logging
from homeassistant.components.http import HomeAssistantView

from .const import API_SERVICE_XIAODU
from .manifest import manifest
from .xiaodu.api import XiaoduCloud

_LOGGER = logging.getLogger(__name__)

class HttpServiceXiaodu(HomeAssistantView):

    url = API_SERVICE_XIAODU
    name = API_SERVICE_XIAODU[1:].replace('/', ':')
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        body = await request.json()
        api_cloud = hass.data[manifest.domain]

        _LOGGER.debug('接收信息 %s', json.dumps(body, indent=2))

        payload = body['payload']

        xiaodu = XiaoduCloud(body)
        response = xiaodu.validate(api_cloud._key)
        if not response:
            namespace = body['header']['namespace']
            if namespace == 'DuerOS.ConnectedHome.Discovery':
                response = xiaodu.discovery()
                # 本地设备状态上报
                api_cloud.save_xiaodu_devices(list(map(lambda x: x['applianceId'], response['payload']['discoveredAppliances'])))

            elif namespace == 'DuerOS.ConnectedHome.Control':
                response = xiaodu.control()
                # 暂停上报5秒钟
                entity_id = payload['appliance']['applianceId']
                api_cloud.set_report_time(entity_id, 5)        

            elif namespace == 'DuerOS.ConnectedHome.Query':
                response = xiaodu.query()

        # 如果包含Uid则返回用户ID
        if 'openUid' in payload:
            response['payload']['openUid'] = payload['openUid']

        _LOGGER.debug('返回信息 %s', json.dumps(response, indent=2))
        return self.json(response)
