import discord
from discord.ext import commands
from discord import app_commands

class Pin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="pin", description="Pin a message by ID.")
    @app_commands.describe(channel="Channel with the message", message_id="Message ID")
    async def pin(self, ctx, channel: discord.TextChannel, message_id: int):
        try:
            msg = await channel.fetch_message(message_id)
            await msg.pin()
            await ctx.send(f"📌 Pinned message in {channel.mention}.")
        except Exception as e:
            await ctx.send(f"Failed to pin: {e}")

    @commands.hybrid_command(name="unpin", description="Unpin a message by ID.")
    @app_commands.describe(channel="Channel with the message", message_id="Message ID")
    async def unpin(self, ctx, channel: discord.TextChannel, message_id: int):
        try:
            msg = await channel.fetch_message(message_id)
            await msg.unpin()
            await ctx.send(f"📍 Unpinned message in {channel.mention}.")
        except Exception as e:
            await ctx.send(f"Failed to unpin: {e}")

async def setup(bot):
    await bot.add_cog(Pin(bot))
