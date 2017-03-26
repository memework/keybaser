import aiohttp
import asyncio
import json
import urllib.parse
import logging
import hashlib
import discord

KB_API_URL = 'https://keybase.io/_/api/1.0/%s.json'

KB_LOOKUP_URL = KB_API_URL % 'user/lookup'

loop = asyncio.get_event_loop()
logger = logging.getLogger('kbutils')

# define custom errors
class JSONError(Exception):
    pass

class AiohttpError(Exception):
    pass

class KeybaseError(Exception):
    pass

def mkcolor(string):
    return discord.Colour(int(hashlib.md5(string.encode("utf-8")).hexdigest()[:6], 16))

async def json_load(string):
    try:
        future_json = loop.run_in_executor(None, json.loads, string)
        return (await future_json)
    except Exception as err:
        raise JSONError("Error parsing JSON data")

async def http_get(url, **kwargs):
    timeout = kwargs.get('timeout', 5)

    try:
        response = await asyncio.wait_for(aiohttp.request('GET', url), timeout)
        content = await response.text()
        return content
    except Exception as err:
        logger.error('http_get', exc_info=True)
        raise err

async def keybase_request(url, **kwargs):
    logger.info("[ḱbrequest] %r", url)

    content = await http_get(url, **kwargs)
    data = await json_load(content)

    # check the data for errors
    status = data['status']
    stcode = status['code']

    if stcode != 0:
        print(data, status)
        raise KeybaseError('%s: %s' % (status['name'], status['desc']))

    logger.info("[kbreq] length: %d", len(content))
    return data

async def kblookup(lookup_string, lookup_type='usernames'):
    r = {lookup_type: lookup_string}
    querystr = urllib.parse.urlencode(r)
    url = f'{KB_LOOKUP_URL}?{querystr}'
    data = await keybase_request(url)
    return data
