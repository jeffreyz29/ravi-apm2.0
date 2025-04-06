import discord
from discord.ext import commands
from discord import app_commands
from database import database\nfrom cogs.administration import embedtools_util
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
        embed = await embedtools_util.get_embed_from_tag(reason)\n        if embed:\n            await ctx.send(embed=embed)\n        else:\n            await ctx.send(f"🚪 Ticket closed. Reason: **{reason}**")
        await ctx.channel.delete()


    @commands.hybrid_command(name="listtickets", description="List active or all tickets")
    @app_commands.describe(page="Page number", status="Filter by status: open/closed/all")
    async def listtickets(self, ctx, page: int = 1, status: str = "all"):
        limit = 10
        offset = (page - 1) * limit
        valid_statuses = ["open", "closed", "all"]
        if status not in valid_statuses:
            return await ctx.send("Status must be 'open', 'closed', or 'all'.")

        base_query = "SELECT channel_id, opener_id, status, created_at FROM tickets WHERE guild_id = ?"
        args = [ctx.guild.id]

        if status != "all":
            base_query += " AND status = ?"
            args.append(status)

        base_query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        args.extend([limit, offset])

        rows = database.fetch(base_query, tuple(args))
        if not rows:
            return await ctx.send("No tickets found on this page.")

        embed = discord.Embed(
            title=f"🎫 Tickets (Page {page}) - Status: {status.title()}",
            color=discord.Color.blurple()
        )
        for ch_id, user_id, stat, created in rows:
            ch = self.bot.get_channel(ch_id)
            ch_name = ch.mention if ch else f"(ID: {ch_id})"
            embed.add_field(name=f"{ch_name} — {stat.title()}", value=f"Opened by <@{user_id}> at `{created}`", inline=False)

        await ctx.send(embed=embed)


    async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
