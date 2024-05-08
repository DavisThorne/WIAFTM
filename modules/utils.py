import requests
# import openai
import discord
from discord.ext import commands
import random
import json
import io
import aiohttp


class Utils(commands.Cog, name="Utils"):
    def __init__(self, client):
        self.client = client
        self.api_key = json.load(open("config.json", "r")).get("api_key")
        self.base_url = "https://api.pawan.krd/v1/completions"
        self.allowed_channel = json.load(open("config.json", "r")).get("ai_channel")

    async def pawan_ai(self, question):
        api_key = self.api_key
        base_url = self.base_url
        temperature = json.load(open("config.json", "r")).get("ai_temperature")
        max_tokens = json.load(open("config.json", "r")).get("ai_max_tokens")

        json_data = {
            "model": "pai-001-light",
            "prompt": f"{question}\nAI:",
            "temperature": float(temperature),
            "max_tokens": int(max_tokens),
            "stop": ["Human:",
                     "AI:"]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.post(base_url, headers=headers, json=json_data).json()
        print(response)
        response = response["choices"][0]["text"]

        return response

    # if you have an OpenAI API key, you can use this function instead of the pawan_ai function

    # async def get_AI(self, question):
    #     openai.api_key = self.api_key
    #
    #     completion = openai.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "user", "content": f"{question}"},
    #         ],
    #     )
    #
    #     return completion.choices[0].message.content

    @commands.slash_command(name="clyde", description="Sends @Clyde a message(Fuck Clyde)")
    async def clyde(self, ctx,
                    message: discord.Option(str, required=True)):
        await ctx.respond(f"<@1081004946872352958> {message}")

    @commands.slash_command(name="ask_ai", description="Asks an AI a question")
    async def ask_ai(self, ctx,
                     question: discord.Option(str, required=True)):

        if str(ctx.channel.id) != self.allowed_channel:
            await ctx.respond("You can only use this command in #ai-channel ")
        else:
            await ctx.respond(f"Asking the all mighty gods", ephemeral=True)
            response = await self.pawan_ai(question)

            await ctx.channel.send(f"The Gods State:\n{response}")

    @commands.slash_command(name="random_hex_code", descriprion="Returns are random hex code")
    async def random_hex_code(self, ctx):

        charset = "0123456789ABCDF"
        output = ""
        channel = ctx.channel
        for _ in range(6):
            temp = random.choice(charset)
            output += temp

        url = f"https://singlecolorimage.com/get/{output}/512x512"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.respond(f"Here is your random hex code: #{output}",
                                  file=discord.File(data, 'cool_image.png'))


def setup(client):
    client.add_cog(Utils(client))
