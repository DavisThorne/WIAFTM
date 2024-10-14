# Description: Main file for the discord bot.
"""
Main entrypoint for the discord bot.
Handles basic bot setup and imports other modules.
Has core basic commands and on_ready event
"""

# Imports
import json
import os
import discord
from discord.ext import commands
import random

# lookup Table Variables
if not os.path.exists(f"{os.getcwd()}/lookup_tables/cringe.json"):
    with open(f"{os.getcwd()}/lookup_tables/cringe.json", "w") as f:
        json.dump({}, f, indent=4)

if not os.path.exists(f"{os.getcwd()}/lookup_tables/quote.json"):
    with open(f"{os.getcwd()}/lookup_tables/quote.json", "w") as f:
        json.dump({}, f, indent=4)

if not os.path.exists(f"{os.getcwd()}/config.json"):
    json_data = {
        "bot_token": "Enter bot token",
        "client_id": "Enter client ID, (this is currently unused)",
        "client_secret": "Enter client secret, (currently unused)",
        "owner_id": "Enter owner ID, (Currently unused)",
        "guild_id": "Enter guild ID, (currently unused)",
        "quote_roll": "Enter the role ID for the quote master role",
        "api_key": "API key for pawan-krd or OpenAI reverse proxy (discord.pawan.krd for pawan-krd AI)",
        "ai_channel": "channel that the ai commands to be used in"
    }
    with open(f"{os.getcwd()}/config.json", "w") as f:
        json.dump(json_data, f, indent=4)

config = json.load(open("config.json", "r"))
cringe_lookup = json.load(open(f"{os.getcwd()}/lookup_tables/cringe.json", "r"))
quotes_lookup = json.load(open(f"{os.getcwd()}/lookup_tables/quote.json", "r"))

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
client.load_extension("modules.casino")
client.load_extension("modules.admin")


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


@client.slash_command(name="change_status", description="Changes the bots status to a random quote")
async def change_status(ctx):
    items = len(quotes_lookup)
    num = random.randint(1, items)
    reply = quotes_lookup.get(f"{str(num)}")
    await client.change_presence(activity=discord.Game(name=reply))
    await ctx.respond("Status Changed")


client.run(token)
