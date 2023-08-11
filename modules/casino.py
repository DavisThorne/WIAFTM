import discord
from discord.ext import commands
import random
import json
import os


class Casino(commands.Cog, name="Casino"):
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

    @commands.slash_command(name="slots", description="Spin a slot machine, maybe you win")
    async def slots(self, ctx,
                    bet: discord.Option(int)):
        user_id = ctx.author.id
        n = 0

        data = json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r").read())

        for key in json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r").read()).get("users"):
            if key.get("userID") == user_id:
                if bet > data["users"][n]["balance"]:
                    await ctx.respond("You dont have enough money to make that bet")
                    return
                break
            n += 1

        spin1 = random.randint(1, 5)
        spin2 = random.randint(1, 5)
        spin3 = random.randint(1, 5)

        if spin1 == spin2 == spin3:
            winnings = (bet * 10) - bet
            await ctx.respond(f"All three numbers were equal, you win: {winnings}")
        elif spin1 == spin2 or spin2 == spin3 or spin1 == spin3:
            winnings = (bet * 5) - bet
            await ctx.respond(f"two of the numbers were equal, you win: {winnings}")
        else:
            winnings = 0 - bet
            await ctx.respond(f"No numbers were equal, you lost: {bet}")
        n = 0
        for key in json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r").read()).get("users"):
            if key.get("userID") == user_id:
                data = json.loads(open(os.getcwd() + "\\lookup_tables\\economy_db.json", "r+").read())
                if data["users"][n]["balance"] <= 0:
                    data["users"][n]["balance"] = 0
                data["users"][n]["balance"] = data["users"][n]["balance"] + winnings
                break
            n += 1

        with open(os.getcwd() + "\\lookup_tables\\economy_db.json", "w") as f:
            f.write(json.dumps(data, indent=4))


def setup(client):
    client.add_cog(Casino(client))
