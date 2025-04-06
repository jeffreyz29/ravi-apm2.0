import discord
from discord.ext import commands
from discord import app_commands

class ChannelTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="create_channel", description="Create a new text channel")
    @app_commands.describe(name="Name of the new channel")
    async def create_channel(self, ctx, name: str):
        await ctx.guild.create_text_channel(name)
        await ctx.send(f"Channel `{name}` created.")

    @commands.hybrid_command(name="delete_channel", description="Delete a specific text channel")
    @app_commands.describe(channel="Channel to delete")
    async def delete_channel(self, ctx, channel: discord.TextChannel):
        await channel.delete()
        await ctx.send(f"Channel `{channel.name}` deleted.")

    @commands.hybrid_command(name="set_topic", description="Set the topic for the current channel")
    @app_commands.describe(topic="New topic for the channel")
    async def set_topic(self, ctx, *, topic: str):
        await ctx.channel.edit(topic=topic)
        await ctx.send("Channel topic updated.")

    @commands.hybrid_command(name="set_channel_name", description="Rename the current channel")
    @app_commands.describe(name="New name for the channel")
    async def set_channel_name(self, ctx, *, name: str):
        await ctx.channel.edit(name=name)
        await ctx.send("Channel name updated.")

async def setup(bot):
    await bot.add_cog(ChannelTools(bot))
