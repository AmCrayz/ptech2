from rivescript import RiveScript
import discord
import os

# Init Rivescript bot
bot = RiveScript()
bot.load_directory("./eg/brain")
bot.sort_replies()

# Init Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Handles Discord login event
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Handles Discord message event
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    reply = bot.reply("localuser", message.content)
    await message.channel.send(reply)

  # Run discord client using bot token
client.run(os.environ['DISCORD_TOKEN'])

