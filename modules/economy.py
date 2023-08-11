import discord
from discord.ext import commands
import json
import os


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

    @commands.slash_command(name="give_money", description="Give a user some money")
    @commands.has_permissions(administrator=True)
    async def give_money(self, ctx,
                         user: discord.Option(str, required=True),
                         amount: discord.Option(str, required=True)):
        await ctx.respond("Locating user...", ephemeral=True)
        n = 0
        for key in json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r").read()).get("users"):
            if key.get("userID") == int(user):
                data = json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r+").read())
                data["users"][n]["balance"] = data["users"][n]["balance"] + int(amount)
                await ctx.respond(f'You have given <@{user}> £{amount}', ephemeral=True)
                break
            n += 1

        with open(os.getcwd() + "\\lookup_tables\\economy_db.json", "w") as f:
            f.write(json.dumps(data, indent=4))

    @commands.slash_command(name="take_money", description="Give a user some money")
    @commands.has_permissions(administrator=True)
    async def give_money(self, ctx,
                         user: discord.Option(str, required=True),
                         amount: discord.Option(str, required=True)):
        await ctx.respond("Locating user...", ephemeral=True)
        n = 0
        for key in json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r").read()).get("users"):
            if key.get("userID") == int(user):
                data = json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r+").read())
                data["users"][n]["balance"] = data["users"][n]["balance"] - int(amount)
                await ctx.respond(f'You have taken from <@{user}> £{amount}', ephemeral=True)
                break
            n += 1

        with open(os.getcwd() + "\\lookup_tables\\economy_db.json", "w") as f:
            f.write(json.dumps(data, indent=4))



def setup(client):
    client.add_cog(Economy(client))
