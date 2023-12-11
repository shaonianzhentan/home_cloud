import re
import time
from homeassistant.helpers import template, entity_registry, area_registry
from homeassistant.core import async_get_hass
import hashlib

def call_service(service, data={}):
    ''' 调用服务 '''
    hass = async_get_hass()
    arr = service.split('.')
    hass.async_create_task(hass.services.async_call(arr[0], arr[1], data))

def date_now():
    ''' 获取当前时间戳 '''
    return int(time.time())

def get_area_entity(hass):
    ''' 获取实体的区域信息 '''
    area_entity = {}
    # 获取所有区域
    area = area_registry.async_get(hass)
    area_list = area.async_list_areas()
    for area_item in area_list:
        # 获取区域实体
        entity = entity_registry.async_get(hass)
        entity_list = entity_registry.async_entries_for_area(
            entity, area_item.id)
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
