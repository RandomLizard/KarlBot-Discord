import discord
from discord import app_commands
import os
from dotenv import load_dotenv
from discord.ext import tasks, commands

from typing import Literal, Union, NamedTuple
from enum import Enum

#Install Link: https://discord.com/oauth2/authorize?client_id=1065456624665366670&permissions=2150657600&integration_type=0&scope=bot+applications.commands

load_dotenv()
MY_GUILD=discord.Object(id=os.getenv("DIMMADOME")) #replace this with your desired guild ID
TOKEN = os.getenv("DEV_DISCORD_TOKEN")

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


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


@client.tree.command(name="ultrasecret")
async def secret(interaction: discord.Interaction):
    """Super secret do not run this"""
    await interaction.response.send_message(f"https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fstatic.demilked.com%2Fwp-content%2Fuploads%2F2018%2F03%2F5aaa1cc4c422b-funny-weird-wtf-stock-photos-28-5a3a5b135f099__700.jpg")
    

@client.tree.command(name="Play")
@app_commands.describe(source="Either a youtube link or a search for something to play")
async def play_music(interaction: discord.Interaction):
    """Plays audio from a youtube video"""



client.run(TOKEN)