import time
import discord
from discord.ext import commands
import config as kb_config

bot = commands.Bot(command_prefix=['kb!', 'Kb!', 'kB!'])

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

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(kb_config.token)
