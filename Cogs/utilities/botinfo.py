import discord
from discord.ext import commands
import platform
import time
import datetime

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    def get_uptime(self):
        total_seconds = int(time.time() - self.start_time)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{days}d {hours}h {minutes}m {seconds}s"

    @commands.hybrid_command(name="botinfo", description="Show info and statistics about the bot")
    async def botinfo(self, ctx):
        embed = discord.Embed(title="🤖 Bot Info", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Developer", value="Your Name or Team", inline=True)
        embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(set(self.bot.get_all_members())), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)} ms", inline=True)
        embed.add_field(name="Uptime", value=self.get_uptime(), inline=True)
        embed.add_field(name="Platform", value=platform.system(), inline=True)
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="discord.py", value=discord.__version__, inline=True)
        embed.set_footer(text="Requested by " + str(ctx.author), icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))