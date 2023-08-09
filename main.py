"""
WIP Private Discord Bot
Key Features:
    - Random Memes (can be assigned to go off at random times)
    - Replies to certain words/phrases
    - Games (Tic Tac Toe, Hangman, etc.)
    - Random Num Gen that decided if we get mortal
    -
"""

# Imports
import json
import os
import discord
from discord.ext import commands
import random

# lookup Table Variables
config = json.load(open("config.json", "r"))
cringe_lookup = json.load(open(f"{os.getcwd()}\lookup_tables\cringe.json", "r"))

# Bot Variables
client = commands.Bot(intents=discord.Intents.all(), command_prefix="!")
token = config.get("bot_token")
clientID = config.get("client_id")
clientSecret = config.get("client_secret")
ownerID = config.get("owner_id")
guildID = config.get("guild_id")

# modules imports
client.load_extension("modules.funny")
client.load_extension("modules.utils")
client.load_extension("modules.economy")


# Events
@client.event
async def on_ready():
    print("Bot is ready.")
    print("Logged in as: " + client.user.name)
    print("------------------")
    await client.change_presence(activity=discord.Game(name="with your mom"))


# Core Commands
@client.slash_command(name="ping", description="Returns Bots Latency")
async def ping(ctx):
    await ctx.respond(f'Pong! {round(client.latency * 1000)}ms')


@client.slash_command(name="help", description="Get some help.")
async def help(ctx):
    help_embed = discord.Embed(title="My Bot's Help!")
    command_names_list = [x.name for x in client.commands]

    help_embed.add_field(
        name="List of supported commands:",
        value="\n".join([str(i + 1) + ". " + x.name for i,
        x in enumerate(client.walk_application_commands())]),
        inline=False
    )
    await ctx.respond(embed=help_embed)


client.run(token)
