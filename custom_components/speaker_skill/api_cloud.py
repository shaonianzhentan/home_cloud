import aiohttp


async def http_post(url, data, headers={}):
    print('==================')
    print('URL：', url)
    print('BODY：', data)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=data) as resp:
            result = await resp.json()
            print('RESULT：', result)
            return result


async def http_post_token(url, data, token):
    return await http_post(url, data, {'Authorization': f'Bearer {token}'})


class ApiCloud():

    def __init__(self, config) -> None:
        self._url = config.get('url')
        self._username = config.get('username')
        self._password = config.get('password')
        self._debug = True

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
        else:
            raise ValueError(res['msg'], error_code=401)

    async def getUserInfo(self):
        return await http_post_token(self.get_url('/user'), {}, self._token)

    async def setHassLink(self, hassLink):
        return await http_post_token(self.get_url('/user/setHassLink'), {
            'hassLink': hassLink
        }, self._token)
