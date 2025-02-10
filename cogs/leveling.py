import discord
from discord.ext import commands
import sqlite3
import math
import random
from DiscordLevelingCard import RankCard, Settings

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
        conn = sqlite3.connect("./cogs/levels.db")
        cursor = conn.cursor()
        guild_id = message.guild.id
        user_id = message.author.id
        
        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()
        
        if result is None:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            cursor.execute(
                        "INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) VALUES (?, ?, ?, ?, ?)", 
                        (guild_id, user_id, cur_level, xp, level_up_xp)
                        )
        else:
            cur_level = result[2]
            xp = result[3]
            level_up_xp = result[4]
            
            xp += random.randint(1, 25)
            
        if xp >= level_up_xp:
            cur_level += 1
            new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level +50)
            
            embed = discord.Embed(title="Level System", color=discord.Color.random())
            embed.add_field(value=f"{message.author.mention} has leveled up to level {cur_level}!", name="Level up!")
            
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(int(1331840731026948159))
            
            if not channel:
                await message.channel.send(embed=embed)
            await channel.send(embed=embed)
            
            cursor.execute("UPDATE Users SET level = ?, xp = ?, level_up_xp = ? WHERE guild_id = ? AND user_id = ?", (cur_level, xp, new_level_up_xp, guild_id, user_id))
        
        cursor.execute("UPDATE Users SET xp = ? WHERE guild_id = ? AND user_id = ?", (xp, guild_id, user_id))
        
        conn.commit()
        conn.close()
    
    @commands.command()
    async def level(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        member_id = member.id
        guild_id = ctx.guild.id
        conn = sqlite3.connect("./cogs/levels.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, member_id))
        result = cursor.fetchone()
        
        if result is None:
            embed = discord.Embed(title="Level System", color=discord.Color.random())
            embed.add_field(value=f"{member.mention} currently does not have a level.", name='Check Level')
            embed.set_footer(text=f"Resquest by {member.name}", icon_url=member.avatar)
            
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(int(1331840731026948159))
            
            if not channel:
                await ctx.send(embed=embed)
            await channel.send(embed=embed)
        else:
            level = result[2]
            xp = result[3]
            level_up_xp = result[4]
            
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
            
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(int(1331840731026948159))
            if not channel:
                await ctx.send(file=discord.File(img_send, filename="rank.png"))
            await channel.send(file=discord.File(img_send, filename="rank.png"))
        
async def setup(bot):
    await bot.add_cog(LevelSys(bot))
