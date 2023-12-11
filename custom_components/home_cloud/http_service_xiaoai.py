from homeassistant.components.http import HomeAssistantView

from .const import API_SERVICE_XIAOAI


class HttpServiceXiaoai(HomeAssistantView):

    url = API_SERVICE_XIAOAI
    name = API_SERVICE_XIAOAI[1:].replace('/', ':')
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        data = await request.json()