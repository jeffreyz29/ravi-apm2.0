import discord
from discord.ext import commands
import datetime

LOG_CHANNEL_ID = 123456789012345678  # Replace with your logging channel ID

class GuildLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_to_channel(self, embed: discord.Embed):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title="✅ Joined Guild", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Members", value=guild.member_count)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        print(f"[Joined] {guild.name} ({guild.id})")
        await self.log_to_channel(embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title="❌ Left Guild", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="ID", value=guild.id)
        print(f"[Left] {guild.name} ({guild.id})")
        await self.log_to_channel(embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        embed = discord.Embed(title="🔁 Guild Updated", color=discord.Color.orange(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Before", value=before.name)
        embed.add_field(name="After", value=after.name)
        print(f"[Updated] {before.name} -> {after.name}")
        await self.log_to_channel(embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title="📺 Channel Created", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Name", value=channel.name)
        embed.add_field(name="Type", value=str(channel.type))
        embed.add_field(name="Guild", value=channel.guild.name)
        print(f"[Channel Created] {channel.name}")
        await self.log_to_channel(embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title="🗑️ Channel Deleted", color=discord.Color.dark_red(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Name", value=channel.name)
        embed.add_field(name="Type", value=str(channel.type))
        embed.add_field(name="Guild", value=channel.guild.name)
        print(f"[Channel Deleted] {channel.name}")
        await self.log_to_channel(embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = discord.Embed(title="🔖 Role Created", color=discord.Color.purple(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Role", value=role.name)
        embed.add_field(name="Guild", value=role.guild.name)
        print(f"[Role Created] {role.name}")
        await self.log_to_channel(embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = discord.Embed(title="❌ Role Deleted", color=discord.Color.dark_purple(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Role", value=role.name)
        embed.add_field(name="Guild", value=role.guild.name)
        print(f"[Role Deleted] {role.name}")
        await self.log_to_channel(embed)

async def setup(bot):
    await bot.add_cog(GuildLogger(bot))
