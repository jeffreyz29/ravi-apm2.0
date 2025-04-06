import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import datetime

class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    @commands.hybrid_command(name="remind", description="Set a reminder")
    @app_commands.describe(time="Time in seconds, minutes, or hours (e.g. 10s, 5m, 1h)", message="Reminder message")
    async def remind(self, ctx, time: str, *, message: str):
        multiplier = {"s": 1, "m": 60, "h": 3600}
        unit = time[-1]
        if unit not in multiplier:
            return await ctx.send("Invalid time format. Use `10s`, `5m`, or `1h`.")
        try:
            seconds = int(time[:-1]) * multiplier[unit]
        except ValueError:
            return await ctx.send("Time must be a number followed by `s`, `m`, or `h`.")
        
        await ctx.send(f"⏰ Okay! I’ll remind you in {time}.")
        await asyncio.sleep(seconds)

        try:
            await ctx.author.send(f"🔔 Reminder: {message}")
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention} 🔔 Reminder: {message}")

async def setup(bot):
    await bot.add_cog(Remind(bot))
