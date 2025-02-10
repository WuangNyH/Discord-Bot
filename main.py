import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv("BOT_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(">>> Status: Bot is ready!")
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(bot_token)

asyncio.run(main())
