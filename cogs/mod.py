import discord
from discord.ext import commands
from discord import app_commands

class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(">>> Moderation commands is ready!")
        
    @app_commands.command(name="clear", description="Delete a specified amount of messages from the channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete_messages(self, interaction: discord.Interaction, amount: int):
        if amount < 1:
            embed = discord.Embed(title="Moderation System", color=discord.Color.random())
            embed.add_field(value=f"{interaction.user.mention}, please specify a value greater than one.", name='Error')
            embed.set_footer(text=f"Resquest by {interaction.user.name}", icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
            return
        deleted_messages = await interaction.channel.purge(limit=amount)
        embed = discord.Embed(title="Moderation System", color=discord.Color.random())
        embed.add_field(value=f"{interaction.user.mention} has deleted {len(deleted_messages)} message(s).", name='Success')
        embed.set_footer(text=f"Resquest by {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="kick", description="Kick a specified member.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, ctx: discord.Interaction, member: discord.Member):
        await ctx.guild.kick(member)
        embed = discord.Embed(title="Moderation System", color=discord.Color.random())
        embed.add_field(value=f"{ctx.user.mention} has kicked {member.mention}", name='Success')
        embed.set_footer(text=f"Resquest by {ctx.user.name}", icon_url=ctx.user.avatar)
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name="ban", description="Ban a specified member.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def kick(self, ctx: discord.Interaction, member: discord.Member, reason: str = None):
        await ctx.guild.ban(member)
        embed = discord.Embed(title="Moderation System", color=discord.Color.random())
        embed.add_field(value=f"{ctx.user.mention} has banned {member.mention}", name='Success')
        if not reason is None:
            embed.add_field(value=f"{reason}", name='Reason')
        embed.set_footer(text=f"Resquest by {ctx.user.name}", icon_url=ctx.user.avatar)
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name="unban", description="Unban a specified user by user ID.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, ctx: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        embed = discord.Embed(title="Moderation System", color=discord.Color.random())
        embed.add_field(value=f"{ctx.user.mention} has unbanned {user.name}", name='Success')
        embed.set_footer(text=f"Resquest by {ctx.user.name}", icon_url=ctx.user.avatar)
        await ctx.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(Mod(bot))
