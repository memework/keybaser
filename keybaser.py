import time
import discord
import config as kb_config

client = discord.Client()

PREFIX = 'kb!'

@client.event
async def on_message(message):
    if message.content.lower().startswith(PREFIX):
        cmd = message.content[3:]

        print(f"recv cmd {cmd}")
        if cmd == 'ping':
            tinit = time.monotonic()
            m = await client.send_message(message.channel, 'pong')
            tfinish = time.monotonic()

            delta = (tfinish - tinit) * 1000
            await client.edit_message(m, '%.2fms' % (delta))

@client.event
async def on_ready():
    print('--READY--')
    print(client.user.name)
    print(client.user.id)
    print('!!!!!')

client.run(kb_config.token)
