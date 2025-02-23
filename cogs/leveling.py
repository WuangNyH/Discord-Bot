import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import math
import random
from DiscordLevelingCard import RankCard, Settings
from database import db

class LevelSys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(">>> Level System is ready!")
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        # conn = sqlite3.connect("./cogs/levels.db")
        # cursor = conn.cursor()
        guild_id = message.guild.id
        user_id = message.author.id
        
        # cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        # result = cursor.fetchone()
        doc_ref = db.collection("level").document(str(guild_id) + "_" + str(user_id))
        data = await doc_ref.get()
        data = data.to_dict()
        
        if not data:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            data = {"cur_level": cur_level, "xp": xp, "level_up_xp": level_up_xp}
            # cursor.execute(
            #             "INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) VALUES (?, ?, ?, ?, ?)",
            #             (guild_id, user_id, cur_level, xp, level_up_xp)
            #             )
            await doc_ref.set(data)
        else:
            cur_level = int(data.get("cur_level"))
            xp = int(data.get("xp"))
            level_up_xp = int(data.get("level_up_xp"))
            
            xp += random.randint(1, 25)
            
        if xp >= level_up_xp:
            cur_level += 1
            new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level +50)
            
            embed = discord.Embed(title="Level System", color=discord.Color.random())
            embed.add_field(value=f"{message.author.mention} has leveled up to level {cur_level}!", name="Level up!")
            
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(int(1331840731026948159))
            await channel.send(embed=embed)
            
            # cursor.execute("UPDATE Users SET level = ?, xp = ?, level_up_xp = ? WHERE guild_id = ? AND user_id = ?", (cur_level, xp, new_level_up_xp, guild_id, user_id))
            data = {"cur_level": cur_level, "xp": xp, "level_up_xp": new_level_up_xp}
            await doc_ref.update(data)

        data = {"xp": xp}
        await doc_ref.update(data)
    
    @app_commands.command(name="level", description="Sends the level card for a given user.")
    async def level(self, ctx: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = ctx.user
        
        member_id = member.id
        guild_id = ctx.guild.id
        # conn = sqlite3.connect("./cogs/levels.db")
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, member_id))
        # result = cursor.fetchone()
        doc_ref = db.collection("level").document(str(guild_id) + "_" + str(member_id))
        data = await doc_ref.get()
        data = data.to_dict()
        
        if data is None:
            embed = discord.Embed(title="Level System", color=discord.Color.random())
            embed.add_field(value=f"{member.mention} currently does not have a level.", name='Check Level')
            embed.set_footer(text=f"Resquest by {member.name}", icon_url=member.avatar)
            
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(int(1331840731026948159))
            await channel.send(embed=embed)
        else:
            level = data.get("cur_level")
            xp = data.get("xp")
            level_up_xp = data.get("level_up_xp")
            
            card_settings = Settings(
                background="https://xuonginhanoi.vn/files/background-la-gi%20(13).jpg",
                text_color="white",
                bar_color="#c98f2a"
            )
            img = RankCard(
                settings=card_settings,
                avatar=member.display_avatar.url,
                level=level,
                current_exp=xp,
                max_exp=level_up_xp,
                username=member.name
            )
            
            img_send = await img.card3()
            await ctx.response.defer()
            await asyncio.sleep(3)
            await ctx.followup.send(file=discord.File(img_send, filename="rank.png"))
async def setup(bot):
    await bot.add_cog(LevelSys(bot))
