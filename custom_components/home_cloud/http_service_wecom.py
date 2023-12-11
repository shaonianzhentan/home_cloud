import json
from homeassistant.components.http import HomeAssistantView

from .const import API_SERVICE_WECOM, CONVERSATION_ASSISTANT
from .manifest import manifest

class HttpServiceWecom(HomeAssistantView):

    url = API_SERVICE_WECOM
    name = API_SERVICE_WECOM[1:].replace('/', ':')
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

        accessToken = data.get('token')
        # 验证权限
        if accessToken == api_cloud._key:
            Content = data.get('Content')
            MsgType = data.get('MsgType')
            message = '未实现该功能'
            if MsgType == 'text':

                conversation = hass.data.get(CONVERSATION_ASSISTANT)

                message = '请安装最新版语音助手插件'
                if conversation is not None:
                    res = await conversation.recognize(Content)
                    intent_result = res.response
                    message = intent_result.speech['plain']['speech']

            return self.json({'MsgType': 'text', 'Content': message})
        else:
            return self.json_message("没有权限", status_code=401)