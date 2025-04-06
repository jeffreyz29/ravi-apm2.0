import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="slowmode", description="Set slowmode in the current channel")
    @app_commands.describe(seconds="Number of seconds for slowmode")
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Slowmode set to {seconds}s")

    @commands.hybrid_command(name="delete", description="Delete a specific message by channel and message ID")
    @app_commands.describe(channel="Channel containing the message", msg_id="ID of the message to delete")
    async def delete(self, ctx, channel: discord.TextChannel, msg_id: int):
        try:
            msg = await channel.fetch_message(msg_id)
            await msg.delete()
            await ctx.send("Message deleted.")
        except Exception as e:
            await ctx.send(f"Failed to delete message: {e}")

    @commands.hybrid_command(name="prune", description="Delete a number of messages from the current channel")
    @app_commands.describe(amount="Number of messages to delete")
    async def prune(self, ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=5)

    @commands.hybrid_command(name="prune_cancel", description="Cancel an active prune session (stub)")
    async def prune_cancel(self, ctx):
        await ctx.send("Prune cancel requested (no active pruning logic set up).")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
