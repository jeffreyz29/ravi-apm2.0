import discord
from discord.ext import commands
from discord import app_commands
import datetime
import importlib.util
import os

class FileChangelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.changelog_path = "data/changelog.py"
        self.changelog_var = "changelogs"

    def is_dev():
        def predicate(ctx):
            return ctx.author.id in [123456789012345678]  # Replace with your dev ID
        return commands.check(predicate)

    def load_changelogs(self):
        spec = importlib.util.spec_from_file_location("changelog", self.changelog_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, self.changelog_var)

    def save_changelogs(self, changelogs):
        with open(self.changelog_path, "w", encoding="utf-8") as f:
            f.write(f"{self.changelog_var} = {repr(changelogs)}")

    @commands.hybrid_command(name="addchangelogfile", description="Add a changelog entry to the file")
    @is_dev()
    @app_commands.describe(version="Version number", changes="Comma-separated list of changes")
    async def addchangelogfile(self, ctx, version: str, *, changes: str):
        changes_list = [line.strip() for line in changes.split(",") if line.strip()]
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        changelogs = self.load_changelogs()
        changelogs.insert(0, {
            "version": version,
            "created_at": timestamp,
            "changes": changes_list
        })
        self.save_changelogs(changelogs)
        await ctx.send(f"✅ Changelog `{version}` added to the file.")

    @commands.hybrid_command(name="changelogfile", description="View file-based changelogs")
    @app_commands.describe(page="Page number")
    async def changelogfile(self, ctx, page: int = 1):
        per_page = 5
        changelogs = self.load_changelogs()
        start = (page - 1) * per_page
        entries = changelogs[start:start + per_page]
        if not entries:
            return await ctx.send("No changelogs found on this page.")

        embed = discord.Embed(
            title=f"📜 Changelog (From File) — Page {page}",
            color=discord.Color.orange()
        )
        for entry in entries:
            version = entry["version"]
            date = entry["created_at"]
            formatted = "\n".join(f"- {line}" for line in entry["changes"])
            embed.add_field(name=f"🔹 {version} — {date}", value=formatted, inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FileChangelog(bot))

