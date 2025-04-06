import discord
from discord.ext import commands
import traceback

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return  # Allow command-specific errors to override this

        error = getattr(error, "original", error)

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 You don’t have permission to do that.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ This command is on cooldown. Try again in {round(error.retry_after, 2)}s.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❗ Missing required argument.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ You can’t use this command.")
        else:
            await ctx.send("⚠️ An unexpected error occurred. The devs have been notified.")
            print(f"Ignoring exception in command {ctx.command}:", flush=True)
            traceback.print_exception(type(error), error, error.__traceback__)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
