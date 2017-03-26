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

def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == kb_config.owner_id)

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

    try:
        res = None
        if location is None:
            res = await utils.kblookup(user)
        else:
            res = await utils.kblookup(user, location)
    except Exception as err:
        await bot.say("fuck: %r", err)
        logger.error('lookup cmd', exc_info=True)
        return

    logger.info("[lookup] %d bytes", len(str(res)))

    if res is None:
        await bot.say("fuckfuckfuck this shouldn't happen")
        return

    try:
        userdata = res['them'][0]
        basics = userdata.get('basics')
        if basics is None:
            await bot.say(":warning: Error getting basic data for the user `%s`" % user)
            return

        username = basics['username']
        em = discord.Embed(title=username, colour=utils.mkcolor(username))

        em.set_thumbnail(url=userdata['pictures']['primary']['url'])
        em.set_footer(text='%d bytes from API' % len(str(res)))

        await bot.say(embed=em)
    except:
        await bot.say('```\n%s\n```' % traceback.format_exc())

@is_owner()
@bot.command()
async def shutdown():
    await bot.say(":wave: bye u bitch!!!!!!! :wave:")
    await bot.logout()

async def _say(m, string):
    await bot.send_message(m.channel, string)

@bot.event
async def on_message(message):
    try:
        await bot.process_commands(message)
    except Exception as err:
        await _say(message, "fuck, we got error: ```%s```" % (traceback.format_exc()))

print("==run this shit==")
bot.run(kb_config.token)
print("\nrip me\n")
