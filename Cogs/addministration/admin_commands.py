import discord
from discord.ext import commands
from discord import app_commands
import json, os, re, asyncio
from discord.utils import get

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_config_path = "data/welcome_config.json"
        self.prefix_config_path = "data/prefixes.json"
        os.makedirs("data", exist_ok=True)
        for path in [self.welcome_config_path, self.prefix_config_path]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump({}, f)

    def load_json(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def save_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    # ==== WELCOME SYSTEM ====
    @commands.hybrid_group(name="greet", invoke_without_command=True, with_app_command=True)
    async def greet(self, ctx):
        await ctx.send("Usage: /greet set | del | msg | dm | dmmsg | test | dmtest")

    @greet.command(name="set", with_app_command=True, description="Set the welcome channel")
    @app_commands.describe(channel="Channel to set as welcome")
    async def greet_set(self, ctx, channel: discord.TextChannel):
        data = self.load_json(self.welcome_config_path)
        data[str(ctx.guild.id)] = data.get(str(ctx.guild.id), {})
        data[str(ctx.guild.id)]["channel"] = channel.id
        self.save_json(self.welcome_config_path, data)
        await ctx.send(f"Greet channel set to {channel.mention}")

    @greet.command(name="del", with_app_command=True, description="Remove welcome settings")
    async def greet_del(self, ctx):
        data = self.load_json(self.welcome_config_path)
        if str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            self.save_json(self.welcome_config_path, data)
            await ctx.send("Greet settings removed.")

    @greet.command(name="msg", with_app_command=True, description="Set the public welcome message")
    @app_commands.describe(message="Welcome message using {user}")
    async def greet_msg(self, ctx, *, message: str):
        data = self.load_json(self.welcome_config_path)
        data.setdefault(str(ctx.guild.id), {})["message"] = message
        self.save_json(self.welcome_config_path, data)
        await ctx.send("Welcome message updated.")

    @greet.command(name="dm", with_app_command=True, description="Toggle DM welcome message")
    @app_commands.describe(toggle="Enable (on) or disable (off) DM welcome")
    async def greet_dm(self, ctx, toggle: str):
        toggle = toggle.lower()
        if toggle not in ["on", "off"]:
            return await ctx.send("Use `on` or `off`.")
        data = self.load_json(self.welcome_config_path)
        data.setdefault(str(ctx.guild.id), {})["dm"] = toggle == "on"
        self.save_json(self.welcome_config_path, data)
        await ctx.send(f"DM Welcome {'enabled' if toggle == 'on' else 'disabled'}.")

    @greet.command(name="dmmsg", with_app_command=True, description="Set the DM welcome message")
    @app_commands.describe(message="DM welcome message using {user}")
    async def greet_dmmsg(self, ctx, *, message: str):
        data = self.load_json(self.welcome_config_path)
        data.setdefault(str(ctx.guild.id), {})["dmmsg"] = message
        self.save_json(self.welcome_config_path, data)
        await ctx.send("DM Welcome message updated.")

    @greet.command(name="test", with_app_command=True, description="Test the public welcome message")
    async def greet_test(self, ctx):
        config = self.load_json(self.welcome_config_path).get(str(ctx.guild.id), {})
        ch_id = config.get("channel")
        msg = config.get("message", "Welcome {user}!")
        if ch_id:
            ch = self.bot.get_channel(ch_id)
            if ch:
                await ch.send(msg.replace("{user}", ctx.author.mention))
                await ctx.send("Test sent.")

    @greet.command(name="dmtest", with_app_command=True, description="Test the DM welcome message")
    async def greet_dmtest(self, ctx):
        config = self.load_json(self.welcome_config_path).get(str(ctx.guild.id), {})
        msg = config.get("dmmsg", "Welcome {user}!")
        try:
            await ctx.author.send(msg.replace("{user}", ctx.author.name))
            await ctx.send("DM Test sent.")
        except:
            await ctx.send("Couldn’t DM you.")

    @commands.hybrid_command(name="slowmode", description="Set slowmode in the current channel")
    @app_commands.describe(seconds="Number of seconds for slowmode")
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Slowmode set to {seconds}s")

