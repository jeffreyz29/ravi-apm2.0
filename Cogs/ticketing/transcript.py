import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime
import json

class TicketTranscript(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.transcript_settings_path = "data/transcripts.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.transcript_settings_path):
            with open(self.transcript_settings_path, "w") as f:
                json.dump({}, f)

    def get_transcript_channel(self, guild_id):
        with open(self.transcript_settings_path, "r") as f:
            data = json.load(f)
        return data.get(str(guild_id))

    def save_transcript_channel(self, guild_id, channel_id):
        with open(self.transcript_settings_path, "r") as f:
            data = json.load(f)
        data[str(guild_id)] = channel_id
        with open(self.transcript_settings_path, "w") as f:
            json.dump(data, f, indent=4)

    @commands.hybrid_command(name="setup_transcripts", description="Set the transcript logging channel")
    @app_commands.describe(channel="Channel to send transcripts to")
    async def setup_transcripts(self, ctx, channel: discord.TextChannel):
        self.save_transcript_channel(ctx.guild.id, channel.id)
        await ctx.send(f"✅ Transcript channel set to {channel.mention}")

    @commands.hybrid_command(name="close", description="Close the current ticket and send a transcript")
    @app_commands.describe(reason="Reason for closing the ticket")
    async def close(self, ctx, *, reason: str = "No reason provided"):
        guild_id = ctx.guild.id
        transcript_channel_id = self.get_transcript_channel(guild_id)
        transcript_channel = self.bot.get_channel(transcript_channel_id) if transcript_channel_id else None

        transcript_lines = []
        async for msg in ctx.channel.history(limit=1000, oldest_first=True):
            timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            line = f"[{timestamp}] {msg.author}: {msg.content}"
            transcript_lines.append(line)

        filename = f"transcript-{ctx.channel.id}.txt"
        filepath = f"/tmp/{filename}"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(transcript_lines))

        file = discord.File(filepath, filename=filename)
        if transcript_channel:
            await transcript_channel.send(
                f"📄 Transcript for ticket `{ctx.channel.name}` closed by {ctx.author.mention} — Reason: {reason}",
                file=file
            )
        await ctx.send("Ticket closed and transcript sent.")
        await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(TicketTranscript(bot))
