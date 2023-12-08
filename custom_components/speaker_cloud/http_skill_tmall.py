import json
from homeassistant.components.http import HomeAssistantView

from .const import API_SKILL_TMALL, CONVERSATION_ASSISTANT

from .manifest import manifest

def build_text_message(message, is_session_end, open_mic):
    # 固定响应格式
    RETURN_DATA = {
        "returnCode": "0",
        "returnErrorSolution": "",
        "returnMessage": "",
        "returnValue": {
            "resultType": "RESULT",
            "executeCode": "SUCCESS",
            "msgInfo": "",
            "gwCommands": [
                {
                    "commandDomain": "AliGenie.Speaker",
                    "commandName": "Speak",
                    "payload": {
                        "type": "text",
                        "text": message,
                        "expectSpeech": open_mic,
                        "needLight": True,
                        "needVoice": True,
                        "wakeupType": "continuity"
                    }
                }
            ]
        }
    }
    return RETURN_DATA


async def conversation_process(hass, text, open_mic):
    ''' 消息处理 '''
    is_session_end = (open_mic == False)

    message = '请安装最新版语音助手插件'
    conversation = hass.data.get(CONVERSATION_ASSISTANT)
    if conversation is not None:
        res = await conversation.recognize(text)
        intent_result = res.response
        message = intent_result.speech['plain']['speech']

    if open_mic:
        message += '，还有什么事吗？'

    return build_text_message(message, is_session_end, open_mic)


async def parse_input(hass, data, aligenie_name, open_mic):
    # 原始语音内容（这里先写死测试）
    text = data['utterance']
    if text.startswith(aligenie_name):
        text = text[len(aligenie_name):]

    if text != '':
        return await conversation_process(hass, text, open_mic)

    return build_text_message('我没听懂欸', is_session_end=True, open_mic=False)


class HttpSkillTmall(HomeAssistantView):

    url = API_SKILL_TMALL
    name = API_SKILL_TMALL[1:].replace('/', ':')
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
        aligenie_name = data.get('skillName')
        open_mic = True
        # 验证权限
        if accessToken != api_cloud._key:
            response = build_text_message(
                '抱歉，您没有权限', is_session_end=True, open_mic=False)
        else:
            response = await parse_input(hass, data, aligenie_name, open_mic)

        if api_cloud._debug:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '发送信息',
                'message': json.dumps(response, indent=2)
            })
        return self.json(response)
