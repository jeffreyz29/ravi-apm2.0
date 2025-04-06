import discord
from discord.ext import commands
from discord import app_commands

class Threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="thread_create", description="Create a public thread in the current channel")
    @app_commands.describe(name="Name of the thread")
    async def thread_create(self, ctx, *, name: str):
        thread = await ctx.channel.create_thread(name=name, type=discord.ChannelType.public_thread)
        await ctx.send(f"Thread `{thread.name}` created.")

    @commands.hybrid_command(name="thread_delete", description="Delete a thread")
    @app_commands.describe(thread="Thread to delete")
    async def thread_delete(self, ctx, thread: discord.Thread):
        await thread.delete()
        await ctx.send("Thread deleted.")

async def setup(bot):
    await bot.add_cog(Threads(bot))
