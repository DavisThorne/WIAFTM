import discord
from discord.ext import commands
import random
import json
import os


class Admin(commands.Cog, name="Admin"):
    def __init__(self, client):
        self.client = client