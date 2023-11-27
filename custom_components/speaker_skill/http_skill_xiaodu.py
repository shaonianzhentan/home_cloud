from homeassistant.components.http import HomeAssistantView

from .const import API_SKILL_XIAODU


class HttpSkillXiaodu(HomeAssistantView):

    url = API_SKILL_XIAODU
    name = API_SKILL_XIAODU[1:].replace('/', ':')
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        data = await request.json()