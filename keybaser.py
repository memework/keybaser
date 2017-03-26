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

_fields = ['basics', 'profile', 'proofs_summary', 'pictures']

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
            res = await utils.kblookup(user, 'usernames', _fields)
        else:
            res = await utils.kblookup(user, location, _fields)
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
        user_id = userdata['id']
        if userdata is None:
            await bot.say("¯\_(ツ)_/¯")
            return

        basics = userdata.get('basics')
        profile = userdata.get('profile')
        proofs = userdata.get('proofs_summary')
        if basics is None or profile is None or proofs is None:
            await bot.say(":warning: Error getting data for the user `%s`" % user)
            return

        username = basics['username']
        em = discord.Embed(title=username, colour=utils.mkcolor(username))

        em.set_thumbnail(url=userdata['pictures']['primary']['url'])
        em.set_footer(text='userid %s, got %d bytes from API' % (user_id, len(str(res))))

        em.add_field(name='Name', value=profile['full_name'])
        em.add_field(name='Location', value=profile['location'])
        em.add_field(name='Bio', value=profile['bio'])

        # proofs
        for proof_key in proofs['by_proof_type']:
            proof = proofs['by_proof_type'][proof_key][0]

            em.add_field(name='{}'.format(proof_key.capitalize()), \
                value='[{}]({})'.format(proof['nametag'], proof['proof_url']))

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
