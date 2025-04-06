import discord
from discord.ext import commands
from discord import app_commands

class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="quote", description="Quote a message from a channel.")
    @app_commands.describe(channel="Channel to find the message", message_id="ID of the message")
    async def quote(self, ctx, channel: discord.TextChannel, message_id: int):
        try:
            message = await channel.fetch_message(message_id)
            embed = discord.Embed(description=message.content, color=discord.Color.blurple(), timestamp=message.created_at)
            embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
            embed.set_footer(text=f"In #{channel.name}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Failed to quote message: {e}")

async def setup(bot):
    await bot.add_cog(Quote(bot))
