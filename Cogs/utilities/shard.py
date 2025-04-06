import discord
from discord.ext import commands

class Shard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="shard_stats", description="Show bot shard count")
    async def shard_stats(self, ctx):
        await ctx.send(f"Running on {self.bot.shard_count} shard(s).")

async def setup(bot):
    await bot.add_cog(Shard(bot))
