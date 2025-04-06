import discord
from discord.ext import commands
import datetime
import os

LOG_CHANNEL_ID = 123456789012345678  # Replace with your logging channel ID

class CommandLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.guild:
            location = f"{ctx.guild.name} / #{ctx.channel.name}"
        else:
            location = "Direct Message"

        log_msg = f"[{datetime.datetime.utcnow()}] 📥 {ctx.author} ran `{ctx.message.content}` in {location}"
        print(log_msg)

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            embed = discord.Embed(title="📋 Command Log", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="User", value=f"{ctx.author} ({ctx.author.id})", inline=True)
            embed.add_field(name="Location", value=location, inline=True)
            embed.add_field(name="Command", value=ctx.message.content, inline=False)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None and not message.author.bot:
            print(f"[{datetime.datetime.utcnow()}] 💌 DM from {message.author}: {message.content}")
            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if channel:
                embed = discord.Embed(title="📩 DM Log", description=message.content, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
                await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandLogger(bot))
