import discord
from discord.ext import commands
from discord import app_commands

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="edit", description="Edit a bot's own message")
    @app_commands.describe(channel="Channel of the message", msg_id="ID of the message", new_content="New content")
    async def edit(self, ctx, channel: discord.TextChannel, msg_id: int, *, new_content: str):
        try:
            msg = await channel.fetch_message(msg_id)
            if msg.author.id == self.bot.user.id:
                await msg.edit(content=new_content)
                await ctx.send("Message edited.")
            else:
                await ctx.send("That message wasn't sent by me.")
        except Exception as e:
            await ctx.send(f"Failed to edit message: {e}")

async def setup(bot):
    await bot.add_cog(Messages(bot))
