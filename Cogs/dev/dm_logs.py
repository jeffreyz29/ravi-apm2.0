import discord
from discord.ext import commands
from database import database
import datetime

class DMLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_dev():
        def predicate(ctx):
            return ctx.author.id in [123456789012345678]  # Replace with your developer ID
        return commands.check(predicate)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None and not message.author.bot:
            timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            database.insert(
                "INSERT INTO dm_logs (user_id, content, timestamp) VALUES (?, ?, ?)",
                (message.author.id, message.content, timestamp)
            )

    @commands.hybrid_command(name="viewdms", description="View paginated DM logs from a user")
    @is_dev()
    @commands.guild_only()
    @app_commands.describe(user_id="User ID", page="Page number")
    async def viewdms(self, ctx, user_id: int, page: int = 1):
        limit = 10
        offset = (page - 1) * limit
        rows = database.fetch(
            "SELECT content, timestamp FROM dm_logs WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?",
            (user_id, limit, offset)
        )
        if not rows:
            return await ctx.send("No DM logs found for that user on this page.")
        
        embed = discord.Embed(
            title=f"📥 DM Logs (Page {page}) — User ID {user_id}",
            color=discord.Color.blurple()
        )
        for content, timestamp in rows:
            embed.add_field(name=timestamp, value=content or "*No content*", inline=False)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="searchdms", description="Search DM logs for a keyword")
    @is_dev()
    @commands.guild_only()
    @app_commands.describe(user_id="User ID", keyword="Search keyword")
    async def searchdms(self, ctx, user_id: int, *, keyword: str):
        rows = database.fetch(
            "SELECT content, timestamp FROM dm_logs WHERE user_id = ? AND content LIKE ? ORDER BY id DESC LIMIT 10",
            (user_id, f"%{keyword}%")
        )
        if not rows:
            return await ctx.send("No matching logs found.")
        
        embed = discord.Embed(
            title=f"🔎 Search '{keyword}' in DM Logs for User {user_id}",
            color=discord.Color.teal()
        )
        for content, timestamp in rows:
            embed.add_field(name=timestamp, value=content or "*No content*", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="cleardms", description="Delete all DM logs for a user")
    @is_dev()
    @commands.guild_only()
    @app_commands.describe(user_id="User ID")
    async def cleardms(self, ctx, user_id: int):
        database.execute("DELETE FROM dm_logs WHERE user_id = ?", (user_id,))
        await ctx.send(f"🗑️ All DM logs for user ID `{user_id}` have been cleared.")

async def setup(bot):
    await bot.add_cog(DMLogger(bot))
