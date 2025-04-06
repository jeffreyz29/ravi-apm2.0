import discord
from discord.ext import commands
from discord import app_commands

class Tag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="tag", description="Tag a user with a custom message.")
    @app_commands.describe(user="User to tag", message="Message to send")
    async def tag(self, ctx, user: discord.Member, *, message: str):
        await ctx.send(f"{user.mention} {message}")

async def setup(bot):
    await bot.add_cog(Tag(bot))
