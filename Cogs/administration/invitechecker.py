import discord
from discord.ext import commands
from discord import app_commands

class InviteChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ignore", description="Blacklist a channel from invite checks.")
    @app_commands.describe(channel="Channel to ignore")
    async def ignore(self, ctx, channel: discord.TextChannel):
        await ctx.send(f"📛 Channel `{channel}` ignored (stub)")

    @commands.hybrid_command(name="category", description="Whitelist a category for invite checks.")
    @app_commands.describe(category="Category to include")
    async def category(self, ctx, category: discord.CategoryChannel):
        await ctx.send(f"✅ Category `{category}` whitelisted (stub)")

    @commands.hybrid_command(name="ids", description="Show all category IDs in this server.")
    async def ids(self, ctx):
        embed = discord.Embed(title="🆔 Category IDs", color=discord.Color.orange())
        for category in ctx.guild.categories:
            embed.add_field(name=category.name, value=f"`{category.id}`", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="checkchannel", description="Set the channel where invite check results are sent.")
    @app_commands.describe(channel="Channel to log results to")
    async def checkchannel(self, ctx, channel: discord.TextChannel):
        await ctx.send(f"🔍 Invite check logs will go to {channel.mention} (stub)")

    @commands.hybrid_command(name="check", description="Run invite check on a category.")
    @app_commands.describe(category="Category to scan")
    async def check(self, ctx, category: discord.CategoryChannel):
        await ctx.send(f"🔎 Running invite scan on category `{category}` (stub)")

async def setup(bot):
    await bot.add_cog(InviteChecker(bot))
