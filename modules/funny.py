import discord
from discord.ext import commands
import random
import json
import os


class Funny(commands.Cog, name="Funny"):
    def __init__(self, client):
        self.client = client
        self.config = json.load(open("config.json", "r"))
        self.quote_role = self.config.get("quote_role")
        self.lookup_dir = os.path.join(os.getcwd(), "lookup_tables")
        self.cringe_lookup = self.load_lookup_table("cringe.json")
        self.quote_lookup = self.load_lookup_table("quote.json")

    def load_lookup_table(self, filename):
        file_path = os.path.join(self.lookup_dir, filename)
        with open(file_path, "r") as f:
            return json.load(f)

    def save_lookup_table(self, filename, data):
        file_path = os.path.join(self.lookup_dir, filename)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    @commands.slash_command(name="quote_add", description="Adds a quote to the quote or cringe lookup table")
    @commands.has_role("Quote Master")
    async def add_quote(self, ctx,
                        quote_type: discord.Option(str, choices=["quote", "cringe"], required=True),
                        message_id: discord.Option(str)):
        message = await ctx.channel.fetch_message(message_id)
        quote = message.content
        lookup_table = self.quote_lookup if quote_type == "quote" else self.cringe_lookup
        items = len(lookup_table)
        lookup_table[str(items + 1)] = quote
        self.save_lookup_table(f"{quote_type}.json", lookup_table)
        await ctx.respond(f'"{quote}" has been added to the {quote_type} lookup table.', ephemeral=True)

    @commands.slash_command(name="quote", description="Returns a random quote or cringe")
    async def quote(self, ctx,
                    quote_type: discord.Option(str, choices=["quote", "cringe"], required=True)):
        lookup_table = self.quote_lookup if quote_type == "quote" else self.cringe_lookup
        items = len(lookup_table)
        num = random.randint(1, items)
        reply = lookup_table.get(str(num))
        embed_title = "Quote" if quote_type == "quote" else "Cringe"
        embed_color = 0x00ff00
        if quote_type == "cringe":
            embed_color = 0xff0000
        embed = discord.Embed(title=embed_title, color=embed_color)
        embed.add_field(name="Sick As Fuck" if quote_type == "quote" else "Cringe As Fuck", value=reply, inline=False)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="true_or_false", description="Returns True or False")
    async def true_or_false(self, ctx,
                            message: discord.Option(str, required=True)):
        choice = random.randint(0, 100)
        if choice < 50:
            await ctx.respond(f"\"{message}\" \nThat is true")
        elif choice >= 50:
            await ctx.respond(f"\"{message}\" \nThat is false")

    @add_quote.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You must have the 'Quote Master' role to use this command", ephemeral=True)
        else:
            raise error


def setup(client):
    client.add_cog(Funny(client))
