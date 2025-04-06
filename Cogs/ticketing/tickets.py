import discord
from discord.ext import commands
from discord import app_commands
import os, json
from typing import Optional

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = "data/tickets.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                json.dump({}, f)

    def load_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_config(self, data):
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=4)

    # 🎟️ Ticket Commands

    @commands.hybrid_command(name="open", description="Create a new support ticket.")
    @app_commands.describe(subject="What do you need help with?")
    async def open(self, ctx, *, subject: str = "No subject provided"):
        await ctx.send(f"🎟️ Ticket created for: `{subject}` (Stub)", ephemeral=True if ctx.interaction else False)

    @commands.hybrid_command(name="close", description="Close the current ticket.")
    @app_commands.describe(reason="Why are you closing this ticket?")
    async def close(self, ctx, *, reason: str = "No reason provided"):
        await ctx.send(f"❌ Ticket closed. Reason: `{reason}` (Stub)")

    @commands.hybrid_command(name="reopen", description="Reopen a previously closed ticket.")
    @app_commands.describe(ticket_id="ID of the ticket to reopen")
    async def reopen(self, ctx, ticket_id: str):
        await ctx.send(f"🔓 Ticket `{ticket_id}` reopened. (Stub)")

    @commands.hybrid_command(name="add", description="Add a user to this ticket.")
    @app_commands.describe(user="User to add to the ticket")
    async def add(self, ctx, user: discord.Member):
        await ctx.send(f"✅ {user.mention} added to ticket. (Stub)")

    @commands.hybrid_command(name="remove", description="Remove a user from the ticket.")
    @app_commands.describe(user="User to remove")
    async def remove(self, ctx, user: discord.Member):
        await ctx.send(f"🚫 {user.mention} removed from ticket. (Stub)")

    @commands.hybrid_command(name="rename", description="Rename the ticket.")
    @app_commands.describe(new_ticket_name="New name for the ticket")
    async def rename(self, ctx, *, new_ticket_name: str):
        await ctx.send(f"✏️ Ticket renamed to `{new_ticket_name}`. (Stub)")

    @commands.hybrid_command(name="claim", description="Claim this ticket.")
    async def claim(self, ctx):
        await ctx.send(f"🎯 {ctx.author.mention} claimed this ticket. (Stub)")

    @commands.hybrid_command(name="unclaim", description="Unclaim the ticket.")
    async def unclaim(self, ctx):
        await ctx.send("🎯 Ticket unclaimed. (Stub)")

    @commands.hybrid_command(name="transfer", description="Transfer ticket ownership.")
    @app_commands.describe(user="User to transfer ownership to")
    async def transfer(self, ctx, user: discord.Member):
        await ctx.send(f"🔁 Ticket transferred to {user.mention}. (Stub)")

    @commands.hybrid_command(name="closerequest", description="Request ticket closure from the opener.")
    @app_commands.describe(delay="How long to wait before closing", reason="Reason for closure")
    async def closerequest(self, ctx, delay: Optional[int] = 30, *, reason: str = "No reason provided"):
        await ctx.send(f"🕒 Closure requested. Will auto-close in {delay}s. Reason: {reason} (Stub)")

    # 🔧 Admin Management

    @commands.hybrid_command(name="addadmin", description="Give ticket admin privileges.")
    async def addadmin(self, ctx, user_or_role: discord.abc.Snowflake):
        await ctx.send(f"🔧 Admin added: {user_or_role} (Stub)")

    @commands.hybrid_command(name="removeadmin", description="Remove ticket admin privileges.")
    async def removeadmin(self, ctx, user_or_role: discord.abc.Snowflake):
        await ctx.send(f"🔧 Admin removed: {user_or_role} (Stub)")

    @commands.hybrid_command(name="addsupport", description="Add support staff.")
    async def addsupport(self, ctx, user_or_role: discord.abc.Snowflake):
        await ctx.send(f"🛠️ Support added: {user_or_role} (Stub)")

    @commands.hybrid_command(name="removesupport", description="Remove support staff.")
    async def removesupport(self, ctx, user_or_role: discord.abc.Snowflake):
        await ctx.send(f"🛠️ Support removed: {user_or_role} (Stub)")

    @commands.hybrid_command(name="blacklist", description="Blacklist a user or role from tickets.")
    async def blacklist(self, ctx, user_or_role: discord.abc.Snowflake):
        await ctx.send(f"🚫 Blacklisted: {user_or_role} (Stub)")

    @commands.hybrid_command(name="setup_auto", description="Auto-configure ticket system basics.")
    async def setup_auto(self, ctx):
        await ctx.send("⚙️ Auto-setup complete. (Stub)")

    @commands.hybrid_command(name="setup_limit", description="Set max tickets per user.")
    @app_commands.describe(number="Max number of tickets per user")
    async def setup_limit(self, ctx, number: int):
        await ctx.send(f"⚙️ Max tickets per user set to {number}. (Stub)")

    @commands.hybrid_command(name="setup_transcripts", description="Set the transcript channel.")
    @app_commands.describe(channel="Channel to send transcripts to")
    async def setup_transcripts(self, ctx, channel: discord.TextChannel):
        await ctx.send(f"📄 Transcripts will be sent to {channel.mention}. (Stub)")

    @commands.hybrid_command(name="setup_use_threads", description="Toggle thread mode for tickets.")
    @app_commands.describe(enable="Use threads or not", notification_channel="Notify this channel if enabled")
    async def setup_use_threads(self, ctx, enable: bool, notification_channel: Optional[discord.TextChannel] = None):
        toggle = "enabled" if enable else "disabled"
        await ctx.send(f"🧵 Threads {toggle}. Notify: {notification_channel.mention if notification_channel else 'None'} (Stub)")

    # 🏷️ Tag Management

    @commands.hybrid_group(name="managetags", description="Manage ticket tags.")
    async def managetags(self, ctx):
        await ctx.send("🏷️ Use `/managetags add/delete/list` (Stub)")

    @managetags.command(name="add", description="Add a tag.")
    async def tag_add(self, ctx, tag_id: str, *, contents: str):
        await ctx.send(f"✅ Tag `{tag_id}` added. (Stub)")

    @managetags.command(name="delete", description="Delete a tag.")
    async def tag_delete(self, ctx, tag_id: str):
        await ctx.send(f"🗑️ Tag `{tag_id}` deleted. (Stub)")

    @managetags.command(name="list", description="List all tags.")
    async def tag_list(self, ctx):
        await ctx.send("🏷️ Tags: (Stub)")  # You can list all tag IDs here

    @commands.hybrid_command(name="tag", description="Show a saved tag.")
    async def tag(self, ctx, tag_id: str):
        await ctx.send(f"🏷️ Tag `{tag_id}` contents: (Stub)")

    # 📊 Stats

    @commands.hybrid_command(name="stats_server", description="Show ticket stats for this server.")
    async def stats_server(self, ctx):
        await ctx.send("📊 Server stats: (Stub)")  # Expand later with real data

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
