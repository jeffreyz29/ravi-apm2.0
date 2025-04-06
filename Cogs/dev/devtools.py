import discord
from discord.ext import commands
from discord import app_commands
import os

class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blacklisted_guilds_path = "data/blacklisted_guilds.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.blacklisted_guilds_path):
            with open(self.blacklisted_guilds_path, 'w') as f:
                f.write("[]")

    def is_dev():
        def predicate(ctx):
            return ctx.author.id in [123456789012345678]  # Replace with your actual ID
        return commands.check(predicate)

    def load_blacklist(self):
        with open(self.blacklisted_guilds_path, 'r') as f:
            return json.load(f)

    def save_blacklist(self, data):
        with open(self.blacklisted_guilds_path, 'w') as f:
            json.dump(data, f, indent=4)

    # Presence / Status
    @commands.hybrid_command(name="setpresence", description="Set the bot's presence message.")
    @commands.check(is_dev())
    async def setpresence(self, ctx, *, status: str):
        await self.bot.change_presence(activity=discord.Game(name=status))
        await ctx.send(f"Presence set to `{status}`.")

    @commands.hybrid_command(name="setstatus", description="Set the bot's online status.")
    @commands.check(is_dev())
    async def setstatus(self, ctx, status: str):
        mapping = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible
        }
        status_lower = status.lower()
        if status_lower in mapping:
            await self.bot.change_presence(status=mapping[status_lower])
            await ctx.send(f"Status set to `{status_lower}`.")
        else:
            await ctx.send("Invalid status. Use online, idle, dnd, or invisible.")

    @commands.hybrid_command(name="setavatar", description="Set the bot's avatar.")
    @commands.check(is_dev())
    async def setavatar(self, ctx, url: str):
        async with self.bot.session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send("Couldn't fetch image.")
            data = await resp.read()
            await self.bot.user.edit(avatar=data)
            await ctx.send("Avatar updated.")

    @commands.hybrid_command(name="setbanner", description="Set the bot's profile banner.")
    @commands.check(is_dev())
    async def setbanner(self, ctx, url: str):
        async with self.bot.session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send("Couldn't fetch banner image.")
            data = await resp.read()
            await self.bot.user.edit(banner=data)
            await ctx.send("Banner updated.")

    @commands.hybrid_command(name="setactivity", description="Set the bot's activity type.")
    @commands.check(is_dev())
    async def setactivity(self, ctx, activity_type: str, *, text: str):
        types = {
            "watching": discord.ActivityType.watching,
            "listening": discord.ActivityType.listening,
            "playing": discord.ActivityType.playing,
            "competing": discord.ActivityType.competing
        }
        if activity_type.lower() in types:
            activity = discord.Activity(type=types[activity_type.lower()], name=text)
            await self.bot.change_presence(activity=activity)
            await ctx.send(f"Activity set to `{activity_type} {text}`.")
        else:
            await ctx.send("Invalid activity type.")

    # Control
    @commands.hybrid_command(name="restart", description="Restart the bot.")
    @commands.check(is_dev())
    async def restart(self, ctx):
        await ctx.send("Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.hybrid_command(name="die", description="Shutdown the bot.")
    @commands.check(is_dev())
    async def die(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.close()

    # Guild blacklist & control
    @commands.hybrid_command(name="blacklist", description="Blacklist a guild from using the bot.")
    @commands.check(is_dev())
    async def blacklist(self, ctx, guild_id: int):
        data = self.load_blacklist()
        if guild_id not in data:
            data.append(guild_id)
            self.save_blacklist(data)
            await ctx.send(f"Guild `{guild_id}` blacklisted.")
        else:
            await ctx.send("Guild already blacklisted.")

    @commands.hybrid_command(name="unblacklist", description="Remove a guild from blacklist.")
    @commands.check(is_dev())
    async def unblacklist(self, ctx, guild_id: int):
        data = self.load_blacklist()
        if guild_id in data:
            data.remove(guild_id)
            self.save_blacklist(data)
            await ctx.send(f"Guild `{guild_id}` removed from blacklist.")
        else:
            await ctx.send("Guild not found in blacklist.")

    @commands.hybrid_command(name="guildleave", description="Leave a server the bot is in.")
    @commands.check(is_dev())
    async def guildleave(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        if guild:
            await guild.leave()
            await ctx.send(f"Left guild `{guild.name}`.")
        else:
            await ctx.send("Guild not found.")

    @commands.hybrid_command(name="serverlist", description="List all servers the bot is in.")
    @commands.check(is_dev())
    async def serverlist(self, ctx):
        embed = discord.Embed(title="📋 Server List", description="List of all servers:", color=discord.Color.blurple())
        for guild in self.bot.guilds:
            embed.add_field(name=guild.name, value=f"ID: `{guild.id}` | Members: {guild.member_count}", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DevTools(bot))
