import discord
from discord.ext import commands

class StubCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="boost")
    async def boost(self, ctx): await ctx.send("(stub) boost")

    @commands.hybrid_command(name="boost_delete")
    async def boost_delete(self, ctx): await ctx.send("(stub) boost delete")

    @commands.hybrid_command(name="boost_message")
    async def boost_message(self, ctx): await ctx.send("(stub) boost message")

    @commands.hybrid_command(name="bye")
    async def bye(self, ctx): await ctx.send("(stub) bye")

    @commands.hybrid_command(name="bye_delete")
    async def bye_delete(self, ctx): await ctx.send("(stub) bye delete")

    @commands.hybrid_command(name="bye_message")
    async def bye_message(self, ctx): await ctx.send("(stub) bye message")

    @commands.hybrid_command(name="bye_test")
    async def bye_test(self, ctx): await ctx.send("(stub) bye test")

    @commands.hybrid_command(name="language_set")
    async def language_set(self, ctx): await ctx.send("(stub) language set")

    @commands.hybrid_command(name="language_default")
    async def language_default(self, ctx): await ctx.send("(stub) language default")

    @commands.hybrid_command(name="language_list")
    async def language_list(self, ctx): await ctx.send("(stub) language list")

async def setup(bot):
    await bot.add_cog(StubCommands(bot))
