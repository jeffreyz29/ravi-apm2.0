import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Update this to match your .env

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    synced = await bot.tree.sync()
    print(f"✅ Synced {len(synced)} slash commands.")

async def load_cogs():
    for root, dirs, files in os.walk("Cogs"):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                path = os.path.join(root, file).replace("/", ".").replace("\\", ".").replace(".py", "")
                try:
                    await bot.load_extension(path)
                    print(f"🔹 Loaded: {path}")
                except Exception as e:
                    print(f"❌ Failed to load {path}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
