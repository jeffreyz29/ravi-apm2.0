import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Whois(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="whois", description="Show detailed user information")
    @app_commands.describe(user="The user to look up")
    async def whois(self, ctx, user: discord.Member = None):
        user = user or ctx.author

        roles = [role.mention for role in user.roles if role != ctx.guild.default_role]
        embed = discord.Embed(
            title=f"👤 User Info: {user}",
            color=user.color,
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Display Name", value=user.display_name, inline=True)
        embed.add_field(name="Bot?", value=str(user.bot), inline=True)
        embed.add_field(name="Top Role", value=user.top_role.mention, inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Joined Discord", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name=f"Roles [{len(roles)}]", value=" ".join(roles) or "None", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Whois(bot))
