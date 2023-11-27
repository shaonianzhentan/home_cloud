import json
from homeassistant.components.http import HomeAssistantView

from .api_xiaodu import discoveryDevice, controlDevice, queryDevice
from .const import API_SERVICE_XIAODU
from .manifest import manifest

class HttpServiceXiaodu(HomeAssistantView):

    url = API_SERVICE_XIAODU
    name = API_SERVICE_XIAODU[1:].replace('/', ':')
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        data = await request.json()
        options = hass.data[manifest.domain]
        if options.get('debug', False) == True:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '接收信息',
                'message': json.dumps(data, indent=2)
            })
        header = data['header']
        payload = data['payload']
        name = header['name']
        accessToken = payload['accessToken']
        # 验证权限
        if accessToken == f'apiKey验证是否有权限':
            token = accessToken
        # 走正常流程
        result = {}
        if token is not None:
            namespace = header['namespace']
            if namespace == 'DuerOS.ConnectedHome.Discovery':
                # 发现设备
                result = await discoveryDevice(hass)
                name = 'DiscoverAppliancesResponse'
            elif namespace == 'DuerOS.ConnectedHome.Control':
                # 控制设备
                result = await controlDevice(hass, name, payload)
                if result is None:
                    name = 'UnsupportedOperationError'
                else:
                    name = name.replace('Request', 'Confirmation')
            elif namespace == 'DuerOS.ConnectedHome.Query':
                # 查询设备
                result = queryDevice(hass, name, payload)
                name = name.replace('Request', 'Response')
        else:
            name = 'InvalidAccessTokenError'

        header['name'] = name
        # 如果包含Uid则返回用户ID
        if 'openUid' in payload:
            result['openUid'] = payload['openUid']
        response = {'header': header, 'payload': result}
        
        if options.get('debug', False) == True:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '发送信息',
                'message': json.dumps(response, indent=2)
            })
        return self.json(response)