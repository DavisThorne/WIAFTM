import discord
from discord.ext import commands
import random
import json
import os


class Casino(commands.Cog, name="Casino"):
    def __init__(self, client):
        self.client = client
        self.data_path = os.path.join(os.getcwd(), "lookup_tables", "economy_db.json")

    async def load_data(self):
        with open(self.data_path, "r") as f:
            return json.load(f)

    async def save_data(self, data):
        with open(self.data_path, "w") as f:
            json.dump(data, f, indent=4)

    async def get_user_data(self, user_id):
        data = await self.load_data()
        for user in data["users"]:
            if user["userID"] == user_id:
                return user
        return None

    async def update_user_balance(self, user_id, amount):
        data = await self.load_data()
        for user in data["users"]:
            if user["userID"] == user_id:
                user["balance"] += amount
                if user["balance"] < 0:
                    user["balance"] = 0
                await self.save_data(data)
                return

    @commands.slash_command(name="slots", description="Spin a slot machine, maybe you win")
    async def slots(self, ctx, bet: discord.Option(int)):
        user_id = ctx.author.id
        user_data = await self.get_user_data(user_id)
        if not user_data:
            await self.add_user_db(user_id, ctx)
            return

        if bet > user_data["balance"]:
            await ctx.respond("You don't have enough money to make that bet")
            return

        spin_results = [random.randint(1, 7) for _ in range(3)]

        if len(set(spin_results)) == 1:
            winnings = (bet * 5) - bet
            await ctx.respond(f"All three numbers were equal, you win: £{winnings}")
        elif len(set(spin_results)) == 2:
            winnings = (bet * 3) - bet
            await ctx.respond(f"Two of the numbers were equal, you win: £{winnings}")
        else:
            winnings = 0 - bet
            await ctx.respond(f"No numbers were equal, you lost: £{bet}")

        await self.update_user_balance(user_id, winnings)

    @commands.slash_command(name="coinflip", description="Flip a coin, maybe you win")
    async def coinflip(self, ctx, choices: discord.Option(str, choices=["Heads", "Tails"], required=True),
                       bet: discord.Option(int, required=True)):
        user_id = ctx.author.id
        user_data = await self.get_user_data(user_id)
        if not user_data:
            await self.add_user_db(user_id, ctx)
            return

        if bet > user_data["balance"]:
            await ctx.respond("You don't have enough money to make that bet")
            return

        result = random.choice(["Heads", "Tails"])
        if result == choices:
            winnings = bet * 2
            await ctx.respond(f"The coin landed on {result}, you win: £{winnings}")
        else:
            winnings = 0 - bet
            await ctx.respond(f"The coin landed on {result}, you lost: £{bet}")

        await self.update_user_balance(user_id, winnings)

    async def add_user_db(self, userID, ctx):
        json_data = {
            "userID": userID,
            "balance": 2500,
            "assets": [{}]
        }
        data = await self.load_data()
        data["users"].append(json_data)
        await self.save_data(data)
        await ctx.respond("You didn't have an account, we have added one. Your starting balance is £2500",
                          ephemeral=True)


def setup(client):
    client.add_cog(Casino(client))
