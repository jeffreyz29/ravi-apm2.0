import discord
from discord.ext import commands
from discord import app_commands
from database import database
import datetime

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def log_ticket(self, guild_id, channel_id, opener_id, status="open"):
        created_at = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        database.insert(
            "INSERT INTO tickets (guild_id, channel_id, opener_id, status, created_at) VALUES (?, ?, ?, ?, ?)",
            (guild_id, channel_id, opener_id, status, created_at)
        )

    def close_ticket(self, channel_id):
        database.execute(
            "UPDATE tickets SET status = 'closed' WHERE channel_id = ?",
            (channel_id,)
        )

    @commands.hybrid_command(name="open", description="Open a new ticket")
    @app_commands.describe(subject="Subject for your ticket")
    async def open(self, ctx, *, subject: str = "No subject"):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(view_channel=True),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True)
        }
        ticket_channel = await ctx.guild.create_text_channel(
            name=f"ticket-{ctx.author.name}".replace(" ", "-"),
            overwrites=overwrites,
            topic=subject,
            reason="New support ticket"
        )
        self.log_ticket(ctx.guild.id, ticket_channel.id, ctx.author.id)
        await ticket_channel.send(f"🎫 Ticket created by {ctx.author.mention}
Subject: **{subject}**")
        await ctx.send(f"✅ Ticket created: {ticket_channel.mention}")

    @commands.hybrid_command(name="close", description="Close the current ticket")
    @app_commands.describe(reason="Reason for closing the ticket")
    async def close(self, ctx, *, reason: str = "No reason provided"):
        self.close_ticket(ctx.channel.id)
        await ctx.send(f"🚪 Ticket closed. Reason: **{reason}**")
        await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
