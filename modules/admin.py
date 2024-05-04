from datetime import datetime

import discord
from discord.ext import commands
import random
import numpy as np
import csv
import json
import os


class Admin(commands.Cog, name="Admin"):
    def __init__(self, client):
        self.client = client
        self.muted_logs_dir = os.path.join(os.getcwd(), "muted_logs")
        self.muted_users = []

        self.load_muted_users()

    async def load_lookup_table(self, filename):
        file_path = os.path.join(self.lookup_dir, filename)
        with open(file_path, "r") as f:
            return json.load(f)

    async def save_muted_log(self, filename, data):
        file_path = os.path.join(self.muted_logs_dir, filename)
        with open(file_path, "a") as f:
            f.write(data)

    async def save_muted_user(self, data, header="Muted Users"):
        with open("muted_users.csv", "w", newline="") as f:
            wr = csv.writer(f)
            wr.writerow([header])
            for user in data:
                wr.writerow([user])

    def load_muted_users(self):
        with open("muted_users.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                self.muted_users.append(row[0])
            self.muted_users.pop(0)
            return self.muted_users

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author) in self.muted_users:
            date = datetime.now()
            date = date.strftime("%d/%m/%Y %H:%M:%S")
            data = f"\n{date}: {message.author} - {message.content}"
            await self.save_muted_log(f"{message.author}_muted_log.txt", data)
        if str(message.author) in self.muted_users:
            await message.delete()

    @commands.command(name="clear", description="Clears the chat")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=15):
        channel_id = ctx.channel.id
        channel_name = ctx.channel.name
        print(ctx.channel)
        channel_name.purge(limit=amount)

    @commands.slash_command(name="mute", description="Mutes a user")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member):
        date = datetime.now()
        date = date.strftime("%d/%m/%Y %H:%M:%S")
        data = f"\n{date}: {member} has been muted"
        await self.save_muted_log(f"{member}_muted_log.txt", data)
        self.muted_users.append(str(member))
        await self.save_muted_user(self.muted_users)
        await ctx.respond(f"{member} has been muted")

    @commands.slash_command(name="unmute", description="Unmutes a user")
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        date = datetime.now()
        date = date.strftime("%d/%m/%Y %H:%M:%S")
        data = f"\n{date}: {member} has been unmuted"
        await self.save_muted_log(f"{member}_muted_log.txt", data)
        self.muted_users.remove(str(member))
        await self.save_muted_user(self.muted_users)
        await ctx.respond(f"{member} has been unmuted")

    @commands.slash_command(name="chatisthisreal", description="kek")
    async def chatIsThisReal(self, ctx):
        for i in range(10):
            i += 1
            await ctx.respond("Chat is this real?")


def setup(client):
    client.add_cog(Admin(client))
