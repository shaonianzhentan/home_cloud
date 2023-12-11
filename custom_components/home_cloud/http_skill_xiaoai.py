import json
import logging
from homeassistant.components.http import HomeAssistantView

from .const import API_SKILL_XIAOAI, CONVERSATION_ASSISTANT

from .api_xiaoai import (XiaoAIAudioItem, XiaoAIDirective, XiaoAIOpenResponse,
                         XiaoAIResponse, XiaoAIStream, XiaoAIToSpeak, XiaoAITTSItem,
                         xiaoai_request, xiaoai_response)

from .manifest import manifest

DOMAIN = manifest.domain

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

def build_music_message(to_speak, mp3_urls):
    ''' 音乐回复 '''
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


async def parse_input(event, hass, api_cloud):
    req = xiaoai_request(event)
    text = req.query
    open_mic = True

    if req.session.user.access_token != api_cloud._key:
        return build_text_message('抱歉，您没有权限', is_session_end=True, open_mic=False, not_understand=True)
    
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

class HttpSkillXiaoai(HomeAssistantView):

    url = API_SKILL_XIAOAI
    name = API_SKILL_XIAOAI[1:].replace('/', ':')
    requires_auth = False

    async def post(self, request):
        data = await request.json()
        hass = request.app["hass"]

        api_cloud = hass.data[manifest.domain]

        if api_cloud._debug:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '接收信息',
                'message': json.dumps(data, indent=2)
            })

        response = await parse_input(data, hass, api_cloud)

        if api_cloud._debug:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '发送信息',
                'message': json.dumps(response, indent=2)
            })
        return self.json(json.loads(response))
