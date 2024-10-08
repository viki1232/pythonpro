import typing
import discord
from discord.ext import commands
import logging
import random
import requests
import traceback
palabras=["hola",
          "mama",'python', 'ahorcado', 'desafío', 'programación', 'bot', 
    'computadora', 'algoritmo', 'inteligencia', 'artificial', 'tecnología', 
    'software', 'hardware', 'internet', 'redes', 'servidor', 
    'cliente', 'desarrollador', 'ingeniero', 'informática', 'base', 
    'datos', 'seguridad', 'criptografía', 'sistema', 'operativo', 
    'aplicación', 'virtualización', 'memoria', 'procesador', 'compilador', 
    'depurador', 'lenguaje', 'script', 'variable', 'constante', 
    'función', 'parámetro', 'modulo', 'biblioteca', 'interfaz', 
    'objeto', 'clase', 'herencia', 'polimorfismo', 'encapsulamiento', 
    'protocolo', 'dominio', 'servidor', 'navegador', 'cookies',"vale",'arbol', 'montaña', 'rio', 'guitarra', 'elefante',
    'camiseta', 'biblioteca', 'universo', 'planeta', 'oceano',
    'perro', 'ciudad', 'avion', 'fotografia', 'telescopio',
    'pintura', 'musica', 'carretera', 'reloj', 'bicicleta',
    'flor', 'murcielago', 'desierto', 'nieve', 'isla',
    'mariposa', 'estrella', 'guitarra', 'castillo', 'volcan',
    'caballo', 'tormenta', 'silla', 'computadora', 'llave',
    'puente', 'barco', 'cerveza', 'libro', 'fuego',
    'piedra', 'tren', 'globo', 'luna', 'sol',
    'jardin', 'telefono', 'sombra', 'pajaro', 'tigre']

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

def elegir_palabra():
    return random.choice(palabras)

# Función para mostrar el estado actual de la palabra
def mostrar_palabra(palabra, letras_adivinadas):
    return ''.join([letra if letra in letras_adivinadas else '_' for letra in palabra])

# Clase del juego de Ahorcado
class Ahorcado:
    def __init__(self):
        self.palabra = elegir_palabra()
        self.letras_adivinadas = set()
        self.intentos = 8
        self.letras_incorrectas = []
        self.juego_terminado = False

    def adivinar(self, letra):
        letra = letra.lower()
        if self.juego_terminado:
            return "El juego ya ha terminado. Inicia un nuevo juego para seguir jugando."
        if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
            return "Ya has adivinado esa letra."
        if letra in self.palabra:
            self.letras_adivinadas.add(letra)
            if set(self.palabra) <= self.letras_adivinadas:
                self.juego_terminado = True
                return f"¡Felicidades! Has adivinado la palabra '{self.palabra}'"
            return f"¡Correcto! La letra '{letra}' está en la palabra."
        else:
            self.intentos -= 1
            self.letras_incorrectas.append(letra)
            if self.intentos == 0:
                self.juego_terminado = True
                return f"¡Perdiste! La palabra era '{self.palabra}'."
            return f"Incorrecto. La letra '{letra}' no está en la palabra. Te quedan {self.intentos} intentos."

    def mostrar_estado(self):
        return ' '.join(letra if letra in self.letras_adivinadas else '_' for letra in self.palabra)

    def dibujar_ahorcado(self):
        etapas = [
            "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n  |   |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n  |   |\n==|=|===="
        ]
        return etapas[8 - self.intentos]
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
juegos = {}


  
bot = commands.Bot(command_prefix='!', description=description, intents=intents)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
YOUTUBE_API_KEY= 'AIzaSyDMsW9IxSq3xZbZV7jEdMeQVzMMMyTE-20'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


# Ejecuta el bot
@bot.group(hidden=True)
async def secret(ctx: commands.Context):
    """What is this "secret" you speak of?"""
    if ctx.invoked_subcommand is None:
        await ctx.send('Shh!', delete_after=5)

def create_overwrites(ctx, *objects):
    overwrites = {obj: discord.PermissionOverwrite(view_channel=True) for obj in objects}
    overwrites.setdefault(ctx.guild.default_role, discord.PermissionOverwrite(view_channel=False))
    overwrites[ctx.guild.me] = discord.PermissionOverwrite(view_channel=True)

    return overwrites

@secret.command()
@commands.guild_only()
async def text(ctx: commands.Context, name: str, *objects: typing.Union[discord.Role, discord.Member]):

    overwrites = create_overwrites(ctx, *objects)

    await ctx.guild.create_text_channel(
        name,
        overwrites=overwrites,
        topic='Top secret text channel. Any leakage of this channel may result in serious trouble.',
        reason='Very secret business.',
    )
@secret.command()
@commands.guild_only()
async def voice(ctx: commands.Context, name: str, *objects: typing.Union[discord.Role, discord.Member]):

    overwrites = create_overwrites(ctx, *objects)

    await ctx.guild.create_voice_channel(
        name,
        overwrites=overwrites,
        reason='Very secret business.',
    )

@bot.command()
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, *, name):
    try:
        await ctx.guild.create_role(name=name)
        await ctx.send(f"Rol '{name}' creado con éxito.")
    except discord.Forbidden:
        await ctx.send("No tengo permiso para crear roles.")
    except discord.HTTPException:
        await ctx.send("Ocurrió un error al crear el rol.")
@bot.command()
@commands.has_permissions(manage_roles=True)
async def asignar_rol(ctx, usuario: discord.Member, rol: discord.Role):
    try:
        await usuario.add_roles(rol)
        await ctx.send(f"Rol {rol.name} asignado a {usuario.name} con éxito.")
    except discord.Forbidden:
        await ctx.send("No tengo permiso para asignar roles.")
     
@bot.command()
async def buscar_musica(ctx, *, query):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'key': YOUTUBE_API_KEY,
        'type': 'video',
        'videoCategoryId': '10',  # ID de categoría para música
        'maxResults': 1
    }
    
    response = requests.get(url, params=params)
    results = response.json()
    
    if 'items' in results and results['items']:
        video = results['items'][0]
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        await ctx.send(f"Resultado de música para '{query}':\n"
                       f"Título: {video_title}\n"
                       f"Enlace: {video_url}")
    else:
        await ctx.send(f"No se encontraron resultados de música para '{query}'.")

# Comando para iniciar un nuevo juego
@bot.command(name="iniciar")
async def iniciar(ctx):
    juegos[ctx.author.id] = Ahorcado()
    await ctx.send("¡Nuevo juego de Ahorcado iniciado! Adivina la palabra letra por letra.")
    await mostrar_estado_juego(ctx)

@bot.command(name="adivinar")
async def adivinar(ctx, letra: str):
    try:
        if len(letra) != 1:
            await ctx.send("Por favor, introduce solo una letra.")
            return
        if ctx.author.id in juegos:
            juego = juegos[ctx.author.id]
            resultado = juego.adivinar(letra)
            await ctx.send(resultado)
            if "Ya has adivinado esa letra" not in resultado:
                await mostrar_estado_juego(ctx)
            if juego.juego_terminado:
                del juegos[ctx.author.id]
        else:
            await ctx.send("No tienes un juego activo. Usa !iniciar para comenzar uno.")
    except Exception as e:
        print(f"Error en adivinar: {str(e)}")  # Para debugging
        await ctx.send("Lo siento, ocurrió un error al procesar tu comando. Por favor, intenta de nuevo.")
        
@bot.command(name="estado")
async def estado(ctx):
    if ctx.author.id in juegos:
        await mostrar_estado_juego(ctx)
    else:
        await ctx.send("No tienes un juego activo. Usa !iniciar para comenzar uno.")

@bot.command(name="terminar")
async def terminar(ctx):
    if ctx.author.id in juegos:
        del juegos[ctx.author.id]
        await ctx.send("Juego terminado. Puedes iniciar uno nuevo con !iniciar")
    else:
        await ctx.send("No tienes un juego activo para terminar.")

async def mostrar_estado_juego(ctx):
    juego = juegos[ctx.author.id]
    estado = f"```\n{juego.dibujar_ahorcado()}\n```"
    estado += f"Palabra: `{juego.mostrar_estado()}`\n"
    estado += f"Letras incorrectas: {', '.join(juego.letras_incorrectas)}\n"
    estado += f"Intentos restantes: {juego.intentos}"
    await ctx.send(estado)

bot.run('MTI4OTYyODEyOTYzMTE0MjA1MA.GFIx9x.TpElXy_6863My1_0Dnei7p1OfayjU0M2EMEQ6w')