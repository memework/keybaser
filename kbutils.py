import aiohttp
import asyncio
import json
import urllib.parse
import logging

KB_API_URL = 'https://keybase.io/_/api/1.0/%s.json'

KB_LOOKUP_URL = KB_API_URL % 'lookup'

loop = asyncio.get_event_loop()
logger = logging.getLogger('kbutils')

# define custom errors
class JSONError(Exception):
    pass

class AiohttpError(Exception):
    pass

class KeybaseError(Exception):
    pass

async def json_load(string):
    try:
        future_json = loop.run_in_executor(None, json.loads, string)
        return (await future_json)
    except Exception as err:
        raise JSONError("Error parsing JSON data")

async def http_get(self, url, **kwargs):
    timeout = kwargs.get('timeout', 5)

    try:
        response = await asyncio.wait_for(aiohttp.request('GET', url), timeout)
        content = await response.text()
        return content
    except Exception as err:
        logger.error('http_get', exc_info=True)
        raise err

async def keybase_request(self, url, **kwargs):
    content = await self.http_get(url, **kwargs)
    data = await self.json_load(content)

    # check the data for errors
    status = data['status']
    stcode = status['code']

    if stcode != 0:
        # API gave up on us
        raise KeybaseError('{}: {}'.format(status['name'], status['desc']))

    logger.info("[kbreq] length: %d", len(data))

    return data

async def kblookup(lookup_string, lookup_type='usernames'):
    print(lookup_type, lookup_string)
    r = {lookup_type, lookup_string}
    print(r, type(r))
    querystr = urllib.parse.urlencode(r)
    url = f'{KB_LOOKUP_URL}?{querystr}'
    data = await keybase_request(url)
    return data
