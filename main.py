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
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} command.")
    except Exception as e:
        print("An error with syncing application commands has occurred: ", e)
        
@bot.tree.command(name="ping", description="Check ping for bot!")
async def ping(interaction: discord.Interaction):
    bot_latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! {bot_latency}ms.")
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(bot_token)

asyncio.run(main())
