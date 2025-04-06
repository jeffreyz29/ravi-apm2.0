import discord
from discord.ext import commands
from discord import app_commands

class Nicknames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="set_nick", description="Set a member's nickname")
    @app_commands.describe(member="Member to change nickname", nick="New nickname")
    async def set_nick(self, ctx, member: discord.Member, *, nick: str):
        await member.edit(nick=nick)
        await ctx.send(f"{member.display_name}'s nickname changed to `{nick}`.")

async def setup(bot):
    await bot.add_cog(Nicknames(bot))
