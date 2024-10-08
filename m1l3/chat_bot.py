# This example requires the 'members' and 'message_content' privileged intents to function.
import discord
from discord.ext import commands
import logging
import random
import math
import wikipediaapi
from googletrans import Translator, LANGUAGES
import requests
import os

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
wiki_wiki = wikipediaapi.Wikipedia('es.wikipedia.org')
translator = Translator()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
GOOGLE_API_KEY = 'AIzaSyAiBWfsk9SlAtCPfv27Bg8QjlI2yQRxweU'
SEARCH_ENGINE_ID = 'd200fa26092704bf6'

def realizar_busqueda(termino):
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={termino}"
    respuesta = requests.get(url)
    resultado = respuesta.json()
    if 'items' in resultado:
        return resultado['items']  # Lista con resultados de búsqueda
    else:
        return None
def buscar_imagenes(termino):
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={termino}&lr=lang_es&hl=es&searchType=image"
    
    try:
        respuesta = requests.get(url)
        resultado = respuesta.json()
        
        if 'items' in resultado:
            # Devuelve una lista de URLs de imágenes
            return [item['link'] for item in resultado['items']]
        else:
            print("No se encontraron imágenes.")
            return None
            
    except requests.RequestException as e:
        print(f"Error al buscar imágenes: {e}")
        return None
# El resto de tu código...
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = commands.Bot(command_prefix='!', description=description, intents=intents)



# Ejemplo de uso:
@bot.command()
async def buscar(ctx, *, termino):
    resultados = realizar_busqueda(termino)
    if resultados:
        # Procesa y envía los resultados
        await ctx.send(str(resultados[0]))  # Envía el primer resultado como ejemplo
    else:
        await ctx.send("No se encontraron resultados.")


palabras_random = ["si,eres muy cool", "tal vez un poco", "eres el mas cool de tod@s", "obvio no jaja", "ni un poco", "muchisimo,definitivamente eres cool"]

palabras_random2=["El corazón de un camarón: Está ubicado en su cabeza.",
                  "Los pulpos: Tienen tres corazones y su sangre es azul.",
                  "Las fresas: No son realmente berries, pero los plátanos sí lo son.",
                  "Los flamencos: Son rosas debido a su dieta rica en betacarotenos.",
                  "5. La lengua de una ballena azul: Puede pesar tanto como un elefante."
                  ,"Las mariposas: Tienen receptores de sabor en sus patas.",
                  "Las vacas: Tienen amigos y se estresan si se separan de ellos.",
                  "Los koalas: Tienen huellas dactilares muy similares a las de los humanos.",
                  "La miel: Nunca se echa a perder; se han encontrado tarros de miel en tumbas egipcias que aún eran comestibles.",
                  ]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    # Responder con una palabra aleatoria
    if message.content.startswith('!soycool'):
        palabra = random.choice(palabras_random)
        await message.channel.send(palabra)

    # Responder con una palabra aleatoria
    if message.content.startswith('!datocurioso'):
        palabra1 = random.choice(palabras_random2)
        await message.channel.send(palabra1)

    if message.author == bot.user:
        return

    # Comando para buscar en Google
    if message.content.startswith('!buscar'):
        termino = message.content[len('!buscar '):]
        if termino:
            await message.channel.send(f'Buscando "{termino}" en Google...')
            resultados = realizar_busqueda(termino)
            
            if resultados:
                # Mandar los primeros 3 resultados
                for resultado in resultados[:3]:
                    titulo = resultado['title']
                    link = resultado['link']
                    descripcion = resultado.get('snippet', 'Sin descripción')
                    await message.channel.send(f"*{titulo}*\n{descripcion}\n{link}\n")
            else:
                await message.channel.send("No se encontraron resultados.")
        else:
            await message.channel.send("Por favor, proporciona un término para buscar.")

    

    if message.author == bot.user:
        return

    # Verifica si el mensaje empieza con el comando !chat
   
    await bot.process_commands(message)



@bot.command()
async def imagen(ctx, *, termino=""):


    logger.info(f"Búsqueda de imagen iniciada para: '{termino}'")
    await ctx.send(f"Buscando imágenes de '{termino}'...")
    
    try:
        imagenes = buscar_imagenes(termino)
        if imagenes:
            logger.info(f"Imagen encontrada para '{termino}'")
            await ctx.send(f"Imagen encontrada para '{termino}':")
            await ctx.send(imagenes[0])
        else:
            logger.warning(f"No se encontraron imágenes para '{termino}'")
            await ctx.send(f"No se encontraron imágenes para '{termino}'.")
    except Exception as e:
        logger.error(f"Error inesperado al buscar imagen: {str(e)}")
        await ctx.send(f"Ocurrió un error al buscar la imagen: {str(e)}")
@bot.command()
async def traducir(ctx, lang, *, text):
    """
    Traduce el texto al idioma especificado.
    Uso: !traducir [código de idioma] [texto]
    Ejemplo: !traducir es Hello, world!
    """
    try:
        if lang not in LANGUAGES:
            await ctx.send(f"Código de idioma '{lang}' no válido. Usa un código de idioma de dos letras (por ejemplo, 'es' para español).")
            return

        translation = translator.translate(text, dest=lang)
        await ctx.send(f"Traducción a {LANGUAGES[lang]}:\n{translation.text}")
    except Exception as e:
        logger.error(f"Error al traducir: {str(e)}")
        await ctx.send(f"Ocurrió un error al traducir: {str(e)}")

@bot.command()
async def idiomas(ctx):
    """Muestra una lista de códigos de idioma disponibles."""
    lang_list = "\n".join([f"{code}: {name}" for code, name in LANGUAGES.items()])
    await ctx.send(f"Códigos de idioma disponibles:\n```\n{lang_list}\n```")

@bot.command()
async def concepto(ctx, *, query):
    page = wiki_wiki.page(query)
    # Verifica si la página existe
    if page.exists():
        if wiki_wiki.language == 'en':  # Si la búsqueda es en inglés
            translated_summary = translator.translate(page.summary, src='en', dest='es').text
            await ctx.send(f"*{page.title}*: {translated_summary[0:500]}...")
        else:
            await ctx.send(f"*{page.title}*: {page.summary[0:500]}...")
        
    else:
        await ctx.send("Lo siento, no encontré ese concepto en Wikipedia.")

@bot.command()
async def suma(ctx, left: int, right: int):
    resultado = left + right
    await ctx.send(f" la suma de {left} + {right} es:{resultado}" )
@bot.command()

async def resta(ctx, num1: int, num2: int):
    resultado = num1 - num2
    await ctx.send(f'La resta de {num1} - {num2} es: {resultado}')

@bot.command()
async def multi(ctx, num1: int, num2: int):
    resultado = num1 * num2
    await ctx.send(f'La multiplicacion de {num1} * {num2} es: {resultado}')
        
@bot.command()
async def divi(ctx, num1: int, num2: int):
    resultado = num1 / num2
    await ctx.send(f'La division de {num1} / {num2} es: {resultado}')
        
@bot.command()
async def poten(ctx, num1: int):
    resultado = num1 * num1
    await ctx.send(f'La potencia de {num1} es: {resultado}')
@bot.command()
async def raiz(ctx, numero: int):
    try:
        resultado = math.sqrt(numero)
        await ctx.send(f'La raíz cuadrada de {numero} es {resultado}')
    except ValueError:
        await ctx.send('Por favor, introduce un número válido.')
@bot.command()
async def raizcubica(ctx, numero: int):
    try:
        resultado = numero ** (1/3)
        await ctx.send(f'La raíz cúbica de {numero} es {resultado}')
    except ValueError:
        await ctx.send('Por favor, introduce un número válido.')

async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


 
bot.run('MTI4OTYyODEyOTYzMTE0MjA1MA.GFIx9x.TpElXy_6863My1_0Dnei7p1OfayjU0M2EMEQ6w')

