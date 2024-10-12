import discord
from discord.ext import commands
import random,os
import logging
import requests
description = description = '''An example bot to showcase the discord.ext.commands extension
module.An example bot to showcase the discord.ext.commands extension
module.description = '''



intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('duck')
async def duck(ctx):
    '''Cada vez que se llama a la solicitud de pato, el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)
@bot.command()
async def meme4(ctx):
    img_name = random.choice(os.listdir('./M2L1/imagenes'))
    with open(f'./M2L1/imagenes/{img_name}', 'rb') as f:
        # ¡Vamos a almacenar el archivo de la biblioteca Discord convertido en esta variable!
        picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)
nombre="vicki"
print(nombre,"ese es mi nombre")
print(f'{nombre} es mi nombre')
bot.run('MTI4OTYyODEyOTYzMTE0MjA1MA.GFIx9x.TpElXy_6863My1_0Dnei7p1OfayjU0M2EMEQ6w')