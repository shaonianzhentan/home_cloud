import logging
import json
from homeassistant.components.http import HomeAssistantView

from .const import API_SKILL_TMALL
from .utils import matcher_query_state, find_entity

from .manifest import manifest

DOMAIN = manifest.domain
_LOGGER = logging.getLogger(__name__)


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

# 消息处理


async def conversation_process(hass, text, open_mic):
    is_session_end = (open_mic == False)
    hass.async_create_task(hass.services.async_call(
        'conversation', 'process', {'text': text}))
    # 如果配置到了查询，则不进入系统意图
    result = matcher_query_state(text)
    if result is not None:
        friendly_name = result
        state = await find_entity(hass, friendly_name)
        if state is not None:
            message = f'{friendly_name}的状态是{state.state}'
            if open_mic:
                message += '，请问还有什么事吗？'
            return build_text_message(message, is_session_end, open_mic)
    message = '收到'
    if open_mic:
        message += '，还有什么事吗？'
    return build_text_message(message, is_session_end, open_mic)

# 格式转换


async def parse_input(hass, data, aligenie_name, open_mic):
    # 原始语音内容（这里先写死测试）
    text = data['utterance'].replace(aligenie_name, '')
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

        options = hass.data[DOMAIN]

        if options.get('debug', False) == True:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '接收信息',
                'message': json.dumps(data, indent=2)
            })

        userOpenId = options.get('open_id', '')
        aligenie_name = options.get('name', '请帮我')
        open_mic = options.get('open_mic', True)
        # 验证权限
        if userOpenId != '' and userOpenId != data['requestData']['userOpenId']:
            response = build_text_message(
                '抱歉，您没有权限', is_session_end=True, open_mic=False)
        else:
            response = await parse_input(hass, data, aligenie_name, open_mic)

        if options.get('debug', False) == True:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '发送信息',
                'message': json.dumps(response, indent=2)
            })
        return self.json(response)
