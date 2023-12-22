import aiohttp
import uuid
import logging
import json
from typing import Dict
from homeassistant.core import split_entity_id
from homeassistant.helpers.debounce import Debouncer
from .storage import Storage

_LOGGER = logging.getLogger(__name__)

DEBOUNCE_TIME = 90

XIAODU_REPORT_URL = 'https://xiaodu.baidu.com/saiya/smarthome/changereport'

async def http_post(url, data, headers={}):
    _LOGGER.debug
    # print('==================')
    _LOGGER.debug('URL：%s', url)
    _LOGGER.debug('BODY：%s', json.dumps(data, indent=2))
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=data) as resp:
            if url == XIAODU_REPORT_URL:
                result = json.loads(await resp.text())
            else:
                result = await resp.json()

            _LOGGER.debug('RESULT：%s', json.dumps(result, indent=2))
            return result


async def http_post_token(url, data, token):
    return await http_post(url, data, {'Authorization': f'Bearer {token}'})


class ApiCloud():

    def __init__(self, hass, config) -> None:
        self._url = config.get('url')
        self._username = config.get('username')
        self._password = config.get('password')
        self._debug = False
        self._skill_list = None
        # 加载小度设备
        storage = Storage('homecloud.xiaodu_devices')
        self.xiaodu_devices = storage.load([])
        # 设备上报
        self.xiaodu_report: Dict[str, XiaoduReport] = {}
        # 设备状态监听
        self.hass = hass
        hass.bus.async_listen("state_changed", self.state_changed)

    async def state_changed(self, event):
        data = event.data
        old_state = data.get('old_state')
        new_state = data.get('new_state')
        entity_id = data.get('entity_id')

        if entity_id in self.xiaodu_devices:

            if old_state is not None and new_state is not None:
                domain = split_entity_id(entity_id)[0]
                # 状态属性变化
                attributeName = None
                if old_state.state == new_state.state:
                    old_attrs = old_state.attributes
                    new_attrs = new_state.attributes
                    if domain == 'light':
                        if old_attrs.get('brightness') != new_attrs.get('brightness'):
                            attributeName = 'brightness'
                    elif domain == 'climate':
                        if old_attrs.get('target_temperature') != new_attrs.get('target_temperature'):
                            attributeName = 'temperature'
                else:
                    if new_state.state == 'unavailable':
                        attributeName = 'connectivity'
                    else:
                        attributeName = 'turnOnState'

                if attributeName is not None:
                    report = self.get_report(entity_id)
                    report.change(entity_id, attributeName)

    async def async_xiaodu_sync(self, entity_id, attributeName):
        ''' 同步小度设备 '''
        skill = self.getSkill('xiaodu')
        if skill is not None:
            return await http_post('https://xiaodu.baidu.com/saiya/smarthome/changereport', {
                "header": {
                    "namespace": "DuerOS.ConnectedHome.Control",
                    "name": "ChangeReportRequest",
                    "messageId": str(uuid.uuid4()),
                    "payloadVersion": "1"
                },
                "payload": {
                    "botId": "ecf5725f-7af0-0375-6bbd-95162643dbf2",
                    "openUid": skill['skill_uid'],
                    "appliance": {
                        "applianceId": entity_id,
                        "attributeName": attributeName
                    }
                }
            })

    def save_xiaodu_devices(self, xiaodu_devices):
        ''' 保存小度设备 '''
        self.xiaodu_devices = xiaodu_devices
        storage = Storage('homecloud.xiaodu_devices')
        storage.save(xiaodu_devices)

    def get_report(self, entity_id):
        ''' 获取上报对象 '''
        report = self.xiaodu_report.get(entity_id)
        if not report:
            report = XiaoduReport(self)
            self.xiaodu_report[entity_id] = report
        return report

    def get_url(self, path):
        return f'{self._url}{path}'

    async def login(self):
        res = await http_post(self.get_url('/user/login'), {
            'username': self._username,
            'password': self._password
        })
        if res['code'] == 0:
            data = res['data']
            self._token = data['token']
            self._key = data['apiKey']
            self._skill_list = await self.getUserSkill()
        else:
            raise ValueError(res['msg'], error_code=401)

    async def getUserInfo(self):
        return await http_post_token(self.get_url('/user'), {}, self._token)

    async def getUserSkill(self):
        res = await http_post_token(self.get_url('/user/getUserSkill'), {}, self._token)
        return res['data']

    def getSkill(self, skill_name):
        for skill in self._skill_list:
            if skill['skill_name'] == skill_name:
                return skill

    async def setHassLink(self, hassLink):
        return await http_post_token(self.get_url('/user/setHassLink'), {
            'hassLink': hassLink
        }, self._token)

    async def setPassword(self, password):
        return await http_post_token(self.get_url('/user/setPassword'), {
            'password': password
        }, self._token)

    async def sendWecomMsg(self, data):
        return await http_post_token(self.get_url('/wework/send'), data, self._token)


class XiaoduReport():

    def __init__(self, api_cloud) -> None:
        self.api_cloud = api_cloud
        self.hass = api_cloud.hass
        self._debouncer = Debouncer(
            hass=self.hass,
            logger=_LOGGER,
            cooldown=DEBOUNCE_TIME,
            immediate=False,
            function=self.push,
        )

    def change(self, entity_id, attribute_name):
        self.entity_id = entity_id
        self.attribute_name = attribute_name
        # 延迟上报
        self.hass.async_create_task(self._debouncer.async_call())

    async def push(self):
        await self.api_clouda.async_xiaodu_sync(self.entity_id, self.attribute_name)