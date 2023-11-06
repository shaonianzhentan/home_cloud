import json
import logging
from homeassistant.components.http import HomeAssistantView

from .const import DOMAIN, XIAOAI_API
from .ha import matcher_query_state, find_entity

from .xiaoai import (XiaoAIAudioItem, XiaoAIDirective, XiaoAIOpenResponse,
                    XiaoAIResponse, XiaoAIStream, XiaoAIToSpeak, XiaoAITTSItem,
                    xiaoai_request, xiaoai_response)

_LOGGER = logging.getLogger(__name__)

# 文本回复
def build_text_message(to_speak, is_session_end, open_mic, not_understand=False):
    xiao_ai_response = XiaoAIResponse(
        not_understand=not_understand,
        to_speak=XiaoAIToSpeak(type_=0, text=to_speak),
        open_mic=open_mic)
    response = xiaoai_response(XiaoAIOpenResponse(version='1.0',
                                                  is_session_end=is_session_end,
                                                  response=xiao_ai_response))
    return response

# 音乐回复
def build_music_message(to_speak, mp3_urls):
    all_list = []
    if to_speak is not None:
        info_tts = XiaoAIDirective(
            type_='tts',
            tts_item=XiaoAITTSItem(
                type_='0', text=to_speak
            ))

        all_list.append(info_tts)
    for url in mp3_urls:
        info_audio = XiaoAIDirective(
            type_='audio',
            audio_item=XiaoAIAudioItem(stream=XiaoAIStream(url=url))
        )
        all_list.append(info_audio)
    xiao_ai_response = XiaoAIResponse(directives=all_list, open_mic=False)
    response = xiaoai_response(XiaoAIOpenResponse(
        version='1.0', is_session_end=True, response=xiao_ai_response))
    return response

# 格式转换
async def parse_input(event, hass):
    req = xiaoai_request(event)
    text = req.query
    # 判断当前用户是否是自己
    options = hass.data[DOMAIN]
    open_mic = options.get('open_mic', True)
    user_id = options.get('open_id', '')
    if user_id != '' and user_id != req.session.user.user_id:
        return build_text_message('我真的好笨笨哦，不知道你在说啥，换个方式叫我吧', is_session_end=True, open_mic=False, not_understand=True)
    # 插槽：req.request.slot_info.intent_name
    intent_name = ''
    if hasattr(req.request.slot_info, 'intent_name'):
        intent_name = req.request.slot_info.intent_name
    # 消息内容：req.query
    if req.request.type == 0:
        # 技能进入请求
        if intent_name == 'Mi_Welcome':
            return build_text_message('欢迎使用语音小助手', is_session_end=False, open_mic=True)
        # 初始化识别内容
        return await conversation_process(hass, text, open_mic)
    elif req.request.type == 1 or req.request.type == 2:
        # 退出意图
        if ['没事', '没事了', '退下', '没有了', '没有', '没用了', '没了', '没有呢'].count(text) > 0:
            return build_text_message('再见了您！', is_session_end=True, open_mic=False)
        else:
            return await conversation_process(hass, text, open_mic)

    return build_text_message('我没听懂欸', is_session_end=True, open_mic=False)

# 消息处理
async def conversation_process(hass, text, open_mic):
    is_session_end = (open_mic == False)
    hass.async_create_task(hass.services.async_call('conversation', 'process', {'text': text}))
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

# 网关视图
class HttpXiaoaiView(HomeAssistantView):

    url = XIAOAI_API
    name = XIAOAI_API[1:].replace('/', ':')
    requires_auth = False

    async def post(self, request):
        data = await request.json()
        hass = request.app["hass"]        
        options = hass.data[DOMAIN]

        if options.get('debug', False) == True:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '接收信息',
                'message': json.dumps(data, indent=2)
            })

        response = await parse_input(data, hass)

        if options.get('debug', False) == True:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '发送信息',
                'message': json.dumps(response, indent=2)
            })
        return self.json(json.loads(response))