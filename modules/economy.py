import discord
from discord.ext import commands
import random
import json
import os
import pathlib as path


class Economy(commands.Cog, name="Economy"):
    def __init__(self, client):
        self.client = client

    async def add_user_db(self, userID, ctx):
        json_data = {
            "userID": userID,
            "balance": 2500,
            "assets": [
                {}
            ]
        }
        with open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r+") as f:
            file_data = json.load(f)
            file_data["users"].append(json_data)
            f.seek(0)
            json.dump(file_data, f, indent=4)
        await ctx.respond("You didnt have an account, we have added one. Your starting balance is £2500",
                          ephemeral=True)

    @commands.slash_command(name="setup_economy", description="First time setup for the economy")
    @commands.is_owner()
    async def db_creation(self, ctx):
        if os.path.isfile(os.getcwd() + "\\lookup_tables\\economy_db.json"):
            pass
        json_data = {
            "users": [

            ]
        }
        json_object = json.dumps(json_data, indent=4)

        with open(os.getcwd() + "\\lookup_tables\\economy_db.json", "w") as f:
            f.write(json_object)

        print(os.getcwd() + "\\lookup_tables\\economy_db.json")

        await ctx.respond("Economy DB Created")

    @commands.slash_command(name="balance", description="Returns your balance")
    async def balance(self, ctx):
        user_id = ctx.author.id
        for key in json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r").read()).get("users"):
            if key.get("userID") == user_id:
                await ctx.respond(f'Your balance is: £{key.get("balance")}')
                return
        await self.add_user_db(user_id, ctx)


def setup(client):
    client.add_cog(Economy(client))
