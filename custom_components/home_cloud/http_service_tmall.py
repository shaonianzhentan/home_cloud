import json
from homeassistant.components.http import HomeAssistantView

from .api_tmall import discoveryDevice, controlDevice, errorResult
from .const import API_SERVICE_TMALL

from .manifest import manifest

class HttpServiceTmall(HomeAssistantView):

    url = API_SERVICE_TMALL
    name = API_SERVICE_TMALL[1:].replace('/', ':')
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        data = await request.json()

        api_cloud = hass.data[manifest.domain]

        if api_cloud._debug:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '接收信息',
                'message': json.dumps(data, indent=2)
            })

        header = data['header']
        payload = data['payload']
        name = header['name']
        accessToken = payload['accessToken']
        # 验证权限
        result = {}
        if accessToken == api_cloud._key:
            namespace = header['namespace']
            if namespace == 'AliGenie.Iot.Device.Discovery':
                # 发现设备
                result = await discoveryDevice(hass)
                name = 'DiscoveryDevicesResponse'
            elif namespace == 'AliGenie.Iot.Device.Control':
                # 控制设备
                result = await controlDevice(hass, name, payload)
                name = 'CorrectResponse'
        else:
            result = errorResult('ACCESS_TOKEN_INVALIDATE')

        # Check error and fill response name
        header['name'] = name
        response = {'header': header, 'payload': result}

        if api_cloud._debug:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '发送信息',
                'message': json.dumps(response, indent=2)
            })
        return self.json(response)