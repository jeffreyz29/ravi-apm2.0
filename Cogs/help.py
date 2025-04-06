import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="modules", description="List all bot modules and their commands.")
    async def modules(self, ctx):
        embed = discord.Embed(title="📦 Bot Modules", description="Each module contains grouped commands:", color=discord.Color.blurple())
        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)
            commands_list = [f"`{cmd.name}`" for cmd in cog.get_commands() if not cmd.hidden]
            embed.add_field(name=cog_name, value=", ".join(commands_list) or "No commands", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="commands", description="List all commands in a specific module.")
    @app_commands.describe(module="Name of the module to view commands for")
    async def commands_(self, ctx, *, module: str = None):
        if not module:
            await self.modules(ctx)
            return
        cog = self.bot.get_cog(module)
        if not cog:
            await ctx.send(f"Module `{module}` not found.")
            return
        embed = discord.Embed(title=f"🧩 Commands in {module}", color=discord.Color.green())
        for cmd in cog.get_commands():
            if not cmd.hidden:
                embed.add_field(name=f"{cmd.name}", value=cmd.help or "No description.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="help", description="Show help for a specific command.")
    @app_commands.describe(command="The command you want help with")
    async def help(self, ctx, command: str):
        cmd = self.bot.get_command(command)
        if not cmd:
            await ctx.send(f"Command `{command}` not found.")
            return
        embed = discord.Embed(title=f"❓ Help for `{command}`", color=discord.Color.orange())
        embed.add_field(name="Description", value=cmd.help or "No description provided.", inline=False)
        if cmd.signature:
            embed.add_field(name="Usage", value=f"`{ctx.prefix}{command} {cmd.signature}`", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="guide", description="View a guide to using the bot.")
    async def guide(self, ctx):
        embed = discord.Embed(title="📖 Bot Guide", description="A quick overview of how to use the bot effectively.", color=discord.Color.teal())
        embed.add_field(name="Getting Started", value="Use `/modules` to explore bot functionality.", inline=False)
        embed.add_field(name="Finding Commands", value="Use `/commands module_name` to see commands in a module.", inline=False)
        embed.add_field(name="Help on a Command", value="Use `/help command_name` for detailed usage.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="donate", description="Support the bot's development and hosting.")
    async def donate(self, ctx):
        embed = discord.Embed(title="❤️ Donate", description="Thank you for considering a donation!", color=discord.Color.red())
        embed.add_field(name="Support Link", value="[Click to donate](https://your-donation-link.example)", inline=False)
        embed.set_footer(text="Your support keeps the bot alive and improving!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
