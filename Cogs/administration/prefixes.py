import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Prefixes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix_config_path = "data/prefixes.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.prefix_config_path):
            with open(self.prefix_config_path, 'w') as f:
                json.dump({}, f)

    def load_json(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def save_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    @commands.hybrid_command(name="prefix", description="Set a custom command prefix for this server")
    @app_commands.describe(new_prefix="New prefix to set")
    async def prefix(self, ctx, new_prefix: str):
        data = self.load_json(self.prefix_config_path)
        data[str(ctx.guild.id)] = new_prefix
        self.save_json(self.prefix_config_path, data)
        await ctx.send(f"Prefix set to `{new_prefix}`.")

    @commands.hybrid_command(name="defprefix", description="Set the default prefix for all servers")
    @app_commands.describe(default="Default prefix")
    async def defprefix(self, ctx, default: str):
        data = self.load_json(self.prefix_config_path)
        data["default"] = default
        self.save_json(self.prefix_config_path, data)
        await ctx.send(f"Default prefix set to `{default}`.")

async def setup(bot):
    await bot.add_cog(Prefixes(bot))
