import discord
from discord.ext import commands
from discord import app_commands
import datetime

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="serverinfo", description="Show information about this server")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        roles = len(guild.roles)
        emojis = len(guild.emojis)
        channels = len(guild.channels)
        boosts = guild.premium_subscription_count
        boost_tier = guild.premium_tier
        members = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        humans = members - bots

        embed = discord.Embed(
            title=f"🏠 Server Info: {guild.name}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Owner", value=str(guild.owner), inline=True)
        embed.add_field(name="Region", value=str(guild.region).title(), inline=True)
        embed.add_field(name="Members", value=f"👤 {humans} | 🤖 {bots} | Total: {members}", inline=False)
        embed.add_field(name="Channels", value=channels, inline=True)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.add_field(name="Emojis", value=emojis, inline=True)
        embed.add_field(name="Boosts", value=f"Level {boost_tier} ({boosts} boosts)", inline=False)
        embed.set_footer(text=f"Created at: {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
