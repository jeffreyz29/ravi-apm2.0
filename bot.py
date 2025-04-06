import discord
from discord.ext import commands
import os
import asyncio
import logging

# ========== CONFIG ==========
COMMAND_PREFIX = "."
LOGGING_CHANNEL = None  # You can hook this later for logging
TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your token or load from env
INTENTS = discord.Intents.all()

# ========== BOT SETUP ==========
bot = commands.Bot(command_prefix=commands.when_mentioned_or(COMMAND_PREFIX), intents=INTENTS)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")
    print("🔄 Syncing slash commands...")
    synced = await bot.tree.sync()
    print(f"✅ Synced {len(synced)} slash commands.")
    print("📡 Bot is now running.")

async def load_all_cogs():
    for root, _, files in os.walk("cogs"):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                path = os.path.splitext(os.path.join(root, file))[0]
                module = path.replace("/", ".").replace("\\", ".")
                try:
                    await bot.load_extension(module)
                    print(f"✅ Loaded {module}")
                except Exception as e:
                    print(f"❌ Failed to load {module}: {e}")

# Optional error handler
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"❌ Error: {str(error)}")

# ========== MAIN ==========
async def main():
    async with bot:
        await load_all_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
