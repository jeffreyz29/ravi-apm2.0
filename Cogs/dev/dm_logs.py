import discord
from discord.ext import commands
from database import database
import datetime

class DMLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None and not message.author.bot:
            timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            database.insert(
                "INSERT INTO dm_logs (user_id, content, timestamp) VALUES (?, ?, ?)",
                (message.author.id, message.content, timestamp)
            )

async def setup(bot):
    await bot.add_cog(DMLogger(bot))
