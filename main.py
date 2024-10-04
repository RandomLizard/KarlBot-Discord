import discord
import os
import asyncio
import random

from dotenv import load_dotenv
from discord import app_commands
from discord.ext import tasks, commands
from typing import Literal, Union, NamedTuple
from enum import Enum
from yt_dlp import YoutubeDL

#Install Link: https://discord.com/oauth2/authorize?client_id=1065456624665366670&permissions=2150657600&integration_type=0&scope=bot+applications.commands

load_dotenv()
MY_GUILD=discord.Object(id=os.getenv("DUMPTRUCK")) #replace this with your desired guild ID
TOKEN = os.getenv("DEV_DISCORD_TOKEN")


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

ytdl = YoutubeDL(ytdl_format_options)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'logged in as {client.user}')


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says Hello"""
    await interaction.response.send_message(f'Hi {interaction.user.mention}!')

@client.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')


@client.tree.command(name='channel-information')
@app_commands.describe(channel='the channel to get the info of')
async def channel_info(interaction: discord.Interaction, channel: Union[discord.VoiceChannel, discord.TextChannel]):
    """Shows basic information for a text or voice channel"""

    embed = discord.Embed(title='Channel Info')
    embed.add_field(name='Name', value=channel.name, inline=True)
    embed.add_field(name='ID', value=channel.id, inline=True)
    embed.add_field(
        name='Type',
        value='Voice' if isinstance(channel, discord.VoiceChannel) else 'Text',
        inline=True
    )
    embed.set_footer(text='Created').timestamp = channel.created_at
    await interaction.response.send_message(embed=embed)

#shitpost commands

@client.tree.command(name="furry-ize")
@app_commands.describe(
    user = "User to inflict furry upon"
)
async def make_furry(interaction: discord.Interaction, user: discord.Member):
    """Turns an unfortunate soul into a furry"""
    furry_name = user.display_name.replace("r", "w")
    furry_name = furry_name.replace("l", "w")
    furry_name = furry_name.replace("R", "W")
    chance = random.randrange(0,100)
    try: 
        if chance > 50:
            await user.edit(nick=f"{furry_name} OwO")
        else:
            await user.edit(nick=f"{furry_name} UwU")
    except:
        await interaction.response.send_message(f"I was not able to turn {user.display_name} into a furry. They are too powerful. (My role is below theirs)",ephemeral=True)
    else:
        await interaction.response.send_message(f"I turned {user.display_name} into a furry. I hope you're happy with yourself.", ephemeral=True)

@client.tree.command(name="ultrasecret")
async def secret(interaction: discord.Interaction):
    """Super secret do not run this"""
    await interaction.response.send_message(f"https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fstatic.demilked.com%2Fwp-content%2Fuploads%2F2018%2F03%2F5aaa1cc4c422b-funny-weird-wtf-stock-photos-28-5a3a5b135f099__700.jpg",ephemeral=True)
    

# Music related commands below

@client.tree.command(name="join")
async def join(interaction: discord.Interaction):
    """Joins the user's current voice channel"""

    if not interaction.user.voice:
        await interaction.response.send_message("I can't join you because you're not in a voice channel.")
    else:
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message("Ready to rock")

@client.tree.command(name="leave")
async def leave(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client.is_connected():
        await interaction.response.send_message("cya!")
        await voice_client.disconnect()
    else:
        await interaction.response.send_message("I'm not connected to a voice channel.")

client.run(TOKEN)