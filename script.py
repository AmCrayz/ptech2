from rivescript import RiveScript
import requests
import discord
import os


# Function to get current time of selected timezone
def get_time(timezone):
    url = f"https://timeapi.io/api/Time/current/zone?timeZone={timezone}"
    response = requests.request('GET', url, headers={}, data={})
    return response.json()

# Inits Rivescript bot
bot = RiveScript()
bot.load_directory('./eg/brain')
bot.sort_replies()

# Inits Discord client
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
    reply = bot.reply('localuser', message.content)
    if reply.startswith('!!'):
        action = reply.replace('!!', '').split('$$')[0]
        if action == 'time':
            location = reply.replace('!!', '').split('$$')[1]
            timezone = 'Europe/Paris'
            if location == 'londres':
                timezone = 'Europe/London'
            elif location == 'new york':
                timezone = 'America/New_York'
            elif location == 'tokyo':
                timezone = 'Asia/Tokyo'
            time = get_time(timezone)
            reply = f'A {location}, il est {time["time"]}'
        elif action == 'temps':
            location = reply.replace('!!', '').split('$$')[1]
            lat = 0
            lon = 0
            if location == 'montpellier':
                lat = 43.608
                lon = 3.879
            elif location == 'nyc':
                lat = 40.730192
                lon = -74.051786
            temps = get_weather(lat, lon)
            print(temps)
            reply = f'A {location}, il fait {temps["weather"][0]["description"]}, et il fait {temps["main"]["temp"]}°C'
        elif action == 'meteo':
            location = reply.replace('!!', '').split('$$')[1]
            lat = 0
            lon = 0
            if location == 'montpellier':
                lat = 43.608
                lon = 3.879
            elif location == 'nyc':
                lat = 40.730192
                lon = -74.051786
            meteo = get_weather_forecast(lat, lon)
            #print(meteo)
            reply = f'A {location} il fera:\n'
            list = meteo['list']
            cur_day = ''
            for item in list:
                day = item["dt_txt"][:10]
                if (day != cur_day):
                    cur_day = day
                    reply += f' -{day}: {item["weather"][0]["description"]}\n'
    await message.channel.send(reply)

# Function to get weather
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={os.environ['WEATHER_API_KEY']}&lang=fr&units=Metric"
    response = requests.request('GET', url, headers={}, data={})
    return response.json()

# Function to get 5 days weather forecast
def get_weather_forecast(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={os.environ['WEATHER_API_KEY']}&lang=fr&units=Metric"
    response = requests.request('GET', url, headers={}, data={})
    return response.json()




# Run discord client using bot token
client.run(os.environ['DISCORD_TOKEN'])


