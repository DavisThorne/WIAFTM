import discord
from discord.ext import commands
import random
import json
import os


class Funny(commands.Cog, name="Funny"):
    def __init__(self, client):
        self.client = client
        self.quote_role = (json.load(open("config.json", "r"))).get("quote_role")
        self.cringe_lookup = json.load(open(f"{os.getcwd()}\\lookup_tables\\cringe.json", "r"))
        self.quote_lookup = json.load(open(f"{os.getcwd()}\\lookup_tables\\quotes.json", "r"))

    @commands.slash_command(name="quote_add", description="Adds a quote to the quote lookup table")
    @commands.has_role(f"Quote Master")
    async def add_quote(self, ctx,
                        quote_type: discord.Option(str, choices=["quote", "cringe"], required=True),
                        message_id: discord.Option(str)):
        message = await ctx.channel.fetch_message(message_id)
        quote = message.content
        if quote_type == "quote":
            items = len(self.quote_lookup)
            self.quote_lookup[f"{str(items + 1)}"] = quote
            with open(f"{os.getcwd()}\\lookup_tables\\quotes.json", "w") as f:
                json.dump(self.quote_lookup, f, indent=4)
            await ctx.respond(f'"{str(quote)}" has been added to the quote lookup table.', ephemeral=True)

        if quote_type == "cringe":
            items = len(self.cringe_lookup)
            self.cringe_lookup[f"{str(items + 1)}"] = quote
            with open(f"{os.getcwd()}\\lookup_tables\\cringe.json", "w") as f:
                json.dump(self.cringe_lookup, f, indent=4)
            await ctx.respond(f'"{str(quote)}" has been added to the cringe lookup table.', ephemeral=True)

    @commands.slash_command(name="quote", description="Returns a random quote")
    async def quote(self, ctx,
                    quote_type: discord.Option(str, choices=["quote", "cringe"], required=True)):
        if quote_type == "quote":
            embed = discord.Embed(title="Quote",
                                  color=0x00ff00)
            items = len(self.quote_lookup)
            num = random.randint(1, items)
            reply = self.quote_lookup.get(f"{str(num)}")
            embed.add_field(name="Sick As Fuck", value=reply, inline=False)
            await ctx.respond(embed=embed)

        if quote_type == "cringe":
            embed = discord.Embed(title="Quote",
                                  color=0x00ff00)
            items = len(self.cringe_lookup)
            num = random.randint(1, items)
            reply = self.cringe_lookup.get(f"{str(num)}")
            embed.add_field(name="Cringe As Fuck", value=reply, inline=False)
            await ctx.respond(embed=embed)

    @add_quote.error
    async def role_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRole):
            print("error handling worked")
            await ctx.send("You must have role 'Quote Master' to use this command", ephemeral=True)
        else:
            raise error


def setup(client):
    client.add_cog(Funny(client))
