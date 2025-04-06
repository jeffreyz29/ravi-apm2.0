import discord
from discord.ext import commands
from discord import app_commands
from database import database
import datetime

class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_dev():
        def predicate(ctx):
            return ctx.author.id in [123456789012345678]  # Replace with your dev ID
        return commands.check(predicate)

    @commands.hybrid_command(name="addchangelog", description="Add a new changelog entry (dev only)")
    @is_dev()
    @app_commands.describe(version="Version number (e.g. v2.0.1)", changes="Summary of updates (comma-separated)")
    async def addchangelog(self, ctx, version: str, *, changes: str):
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        database.insert(
            "INSERT INTO changelog (version, changes, created_at) VALUES (?, ?, ?)",
            (version, changes, timestamp)
        )
        await ctx.send(f"✅ Changelog `{version}` added.")

    @commands.hybrid_command(name="changelog", description="View the bot's changelog")
    @app_commands.describe(page="Page number (default: 1)")
    async def changelog(self, ctx, page: int = 1):
        per_page = 5
        offset = (page - 1) * per_page
        rows = database.fetch(
            "SELECT version, changes, created_at FROM changelog ORDER BY id DESC LIMIT ? OFFSET ?",
            (per_page, offset)
        )
        if not rows:
            return await ctx.send("No changelogs found on this page.")
        
        embed = discord.Embed(
            title=f"📜 Changelog (Page {page})",
            color=discord.Color.orange()
        )
        for version, changes, date in rows:
            formatted = "\n".join(f"- {line.strip()}" for line in changes.split(","))
            embed.add_field(name=f"🔹 {version} — {date}", value=formatted, inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Changelog(bot))
