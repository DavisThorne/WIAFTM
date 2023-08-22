import discord
from discord.ext import commands
import json
import os


class Economy(commands.Cog, name="Economy"):
    def __init__(self, client):
        self.client = client
        self.data_path = os.path.join(os.getcwd(), "lookup_tables", "economy_db.json")

    async def load_data(self):
        with open(self.data_path, "r") as f:
            return json.load(f)

    async def save_data(self, data):
        with open(self.data_path, "w") as f:
            json.dump(data, f, indent=4)

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

    @commands.slash_command(name="setup_economy", description="First time setup for the economy")
    @commands.is_owner()
    async def db_creation(self, ctx):
        if os.path.isfile(self.data_path):
            pass
        else:
            json_data = {"users": []}
            with open(self.data_path, "w") as f:
                json.dump(json_data, f, indent=4)
            await ctx.respond("Economy DB Created")

    async def get_user_data(self, user_id):
        data = await self.load_data()
        for user in data["users"]:
            if user["userID"] == user_id:
                return user
        return None

    @commands.slash_command(name="balance", description="Returns your balance")
    async def balance(self, ctx):
        user_id = ctx.author.id
        user_data = await self.get_user_data(user_id)
        if user_data:
            await ctx.respond(f'Your balance is: £{user_data["balance"]:,}')
        else:
            await self.add_user_db(user_id, ctx)

    async def modify_balance(self, user_id, amount):
        data = await self.load_data()
        for user in data["users"]:
            if user["userID"] == user_id:
                user["balance"] += amount
                await self.save_data(data)
                break

    @commands.slash_command(name="edit_money", description="Give a user some money")
    @commands.has_permissions(administrator=True)
    async def edit_money(self, ctx,
                         action: discord.Option(str, choices=["give", "take"], required=True),
                         user: discord.Option(str, required=True),
                         amount: discord.Option(str, required=True)):
        action_text = "given" if action == "give" else "taken"
        user_id = int(user)
        user_data = await self.get_user_data(user_id)
        if not user_data:
            await ctx.respond("User not found.", ephemeral=True)
            return

        amount = int(amount) if action == "give" else -int(amount)
        await self.modify_balance(user_id, amount)
        await ctx.respond(f'You have {action_text} from <@{user_id}> £{abs(amount)}', ephemeral=True)


def setup(client):
    client.add_cog(Economy(client))
