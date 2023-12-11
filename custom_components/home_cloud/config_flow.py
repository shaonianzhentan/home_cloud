from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant.data_entry_flow import FlowResult

import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.const import CONF_URL, CONF_USERNAME, CONF_PASSWORD, CONF_TYPE
from .manifest import manifest

from .api_cloud import http_post

OP_LOGIN_NAME = '登录'
OP_REGISTER_NAME = '注册'


class SimpleConfigFlow(ConfigFlow, domain=manifest.domain):

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None, errors={}) -> FlowResult:
        
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            url = user_input[CONF_URL]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            type = user_input[CONF_TYPE]
            if type == OP_REGISTER_NAME:
                result = await http_post(f'{url}/user/register', {'username': username, 'password': password})
            else:
                result = await http_post(f'{url}/user/login', {'username': username, 'password': password})

            res_code = result.get('code')
            if res_code == 0:
                return self.async_create_entry(title=manifest.domain, data={
                    'url': url,
                    'username': username,
                    'password': password
                })

            errors['base'] = str(res_code)
            DATA_SCHEMA = vol.Schema({
                vol.Required(CONF_URL, default=url): str,
                vol.Required(CONF_USERNAME, default=username): str,
                vol.Required(CONF_PASSWORD, default=password): str,
                vol.Required(CONF_TYPE, default=type): vol.In([OP_LOGIN_NAME, OP_REGISTER_NAME]),
            })
        else:
            DATA_SCHEMA = vol.Schema({
                vol.Required(CONF_URL): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_TYPE, default=OP_LOGIN_NAME): vol.In([OP_LOGIN_NAME, OP_REGISTER_NAME]),
            })
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(entry: ConfigEntry):
        return OptionsFlowHandler(entry)


class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None, errors={}):

        api_cloud = self.hass.data[manifest.domain]
        if user_input is not None:
            url = user_input.get(CONF_URL)
            res = await api_cloud.setHassLink(url)
            if res.get('code') == 0:
                return self.async_create_entry(title='', data=user_input)
            else:
                errors['base'] = '500'

        res = await api_cloud.getUserInfo()
        data = res.get('data')
        DATA_SCHEMA = vol.Schema({
            vol.Required(CONF_URL, default=data.get('hassLink')): str,
        })
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
