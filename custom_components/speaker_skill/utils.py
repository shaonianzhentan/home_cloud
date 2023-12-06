import re
from homeassistant.helpers import template, entity_registry, area_registry
import hashlib


def get_area_entity(hass):
    ''' 获取实体的区域信息 '''
    area_entity = {}
    # 获取所有区域
    area = area_registry.async_get(hass)
    area_list = area.async_list_areas()
    for area_item in area_list:
        # 获取区域实体
        entity = entity_registry.async_get(hass)
        entity_list = entity_registry.async_entries_for_area(entity, area_item.id)
        for entity_item in entity_list:
            area_entity.update({
                entity_item.entity_id: area_item.name
            })
    return area_entity




def md5(data):
    ''' MD5加密 '''
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def trim_char(text):
    return text.strip(' 。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑·¨….¸;！´？！～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=<­­＿_-\ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼')


def matcher_query_state(text):
    matchObj = re.match(r'(查看|查询)(.*)的状态', text)
    if matchObj is not None:
        return trim_char(matchObj.group(2))

    matchObj = re.match(r'(查看|查询)(.*)', text)
    if matchObj is not None:
        return trim_char(matchObj.group(2))

    matchObj = re.match(r'(.*)的状态', text)
    if matchObj is not None:
        return trim_char(matchObj.group(1))

# 查询实体


def isMatchDomain(type, domain):
    return type is None or (isinstance(type, list) and type.count(domain) == 1) or (isinstance(type, str) and type == domain)


async def find_entity(hass, name, type=None):
    # 遍历所有实体
    states = hass.states.async_all()
    for state in states:
        entity_id = state.entity_id
        domain = state.domain
        attributes = state.attributes
        friendly_name = attributes.get('friendly_name')
        # 查询对应的设备名称
        if friendly_name is not None and friendly_name.lower() == name.lower():
            # 指定类型
            if isMatchDomain(type, domain):
                return state
    # 如果没有匹配到实体，则开始从区域里查找
    arr = name.split('的', 1)
    if len(arr) == 2:
        area_name = arr[0]
        device_name = arr[1]
        # 获取所有区域
        area = await area_registry.async_get_registry(hass)
        area_list = area.async_list_areas()
        _list = list(filter(lambda item: item.name == area_name, area_list))
        if (len(_list) > 0):
            area_id = _list[0].id
            entity = await entity_registry.async_get_registry(hass)
            entity_list = entity_registry.async_entries_for_area(
                entity, area_id)
            # 有设备才处理
            if len(entity_list) > 0:
                # 查找完整设备
                _list = list(filter(lambda item: item.name ==
                             device_name or item.original_name == device_name, entity_list))
                if (len(_list) > 0):
                    # print(_list)
                    item = _list[0]
                    state = hass.states.get(item.entity_id)
                    if isMatchDomain(type, state.domain):
                        return state
                # 如果直接说了灯或开关
                if device_name == '灯':
                    # 如果只有一个设备
                    if len(entity_list) == 1:
                        item = entity_list[0]
                        state = hass.states.get(item.entity_id)
                        if isMatchDomain(type, state.domain):
                            return state
                    else:
                        # 取第一个含有灯字的设备（这里可以通过其他属性来判断，以后再考虑）
                        for item in entity_list:
                            state = hass.states.get(item.entity_id)
                            friendly_name = state.attributes.get(
                                'friendly_name')
                            if '灯' in friendly_name and isMatchDomain(type, state.domain):
                                return state
