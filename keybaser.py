import time
import traceback
import discord
import kbutils as utils
import logging

from discord.ext import commands
import config as kb_config

bot = commands.Bot(command_prefix=['kb!', 'Kb!', 'kB!', 'KB!'])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('keybaser')

@bot.event
async def on_ready():
    print('!!READY!!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def ping(ctx):
    """Ping the fucker."""
    tinit = time.monotonic()
    m = await bot.say('pong')
    tfinish = time.monotonic()

    delta = (tfinish - tinit) * 1000
    await bot.edit_message(m, '`%.2fms`' % (delta))

@bot.command(pass_context=True)
async def lookup(ctx, user : str, location : str = ''):
    if len(location.strip()) < 1:
        location = None

    res = None
    if location is None:
        res = await utils.kblookup(user, location)
    else:
        res = await utils.kblookup(user, location)

    logger.info("[lookup] %d bytes", len(res))

    if res is None:
        await bot.say("fuckfuckfuck this shouldn't happen")
        return

    await bot.say("We got %d bytes from API" % len(res))

async def _say(m, string):
    await bot.send_message(m.channel, string)

@bot.event
async def on_message(message):
    try:
        await bot.process_commands(message)
    except Exception as err:
        await _say(message, "fuck, we got error: ```%s```" % (traceback.format_exc()))

bot.run(kb_config.token)
