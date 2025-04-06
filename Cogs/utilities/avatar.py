import discord
from discord.ext import commands
from discord import app_commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="avatar", description="View a user's avatar")
    @app_commands.describe(user="The user to get the avatar of")
    async def avatar(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(title=f"🖼️ Avatar for {user}", color=discord.Color.blurple())
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Avatar(bot))