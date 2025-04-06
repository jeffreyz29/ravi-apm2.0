import discord
from discord.ext import commands
from discord import app_commands, ui
import datetime

BUG_LOG_CHANNEL_ID = 123456789012345678  # Replace with your actual dev log channel ID

class BugModal(ui.Modal, title="🐞 Bug Report Form"):
    description = ui.TextInput(label="What did you encounter?", style=discord.TextStyle.paragraph, max_length=1000)
    steps = ui.TextInput(label="Steps to Reproduce", style=discord.TextStyle.paragraph, required=False, max_length=1000)
    system = ui.TextInput(label="Browser / Device / OS", placeholder="e.g. Windows 10, Safari on iOS", required=False)

    def __init__(self, bot, author):
        super().__init__()
        self.bot = bot
        self.author = author

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🐛 New Bug Report",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=str(self.author), icon_url=self.author.display_avatar.url)
        embed.set_footer(text=f"User ID: {self.author.id}")
        embed.add_field(name="Description", value=self.description.value or "No description", inline=False)
        embed.add_field(name="Steps to Reproduce", value=self.steps.value or "Not provided", inline=False)
        embed.add_field(name="System", value=self.system.value or "Not specified", inline=False)

        await interaction.response.send_message("✅ Thank you! Your bug report has been submitted.", ephemeral=True)

        log_channel = self.bot.get_channel(BUG_LOG_CHANNEL_ID)
        if log_channel:
            view = ReportActionsView(self.author.id)
            await log_channel.send(embed=embed, view=view)


class ReportActionsView(discord.ui.View):
    def __init__(self, reporter_id):
        super().__init__(timeout=None)
        self.reporter_id = reporter_id

    @discord.ui.button(label="Mark as Resolved", style=discord.ButtonStyle.green, custom_id="resolve_bug")
    async def resolve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.edit(content="✅ Resolved", view=None)
        await interaction.response.send_message("Marked as resolved.", ephemeral=True)

    @discord.ui.button(label="DM Reporter", style=discord.ButtonStyle.blurple, custom_id="dm_reporter")
    async def dm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.client.get_user(self.reporter_id)
        if user:
            await user.send(f"📬 A dev has responded to your bug report.

*From:* {interaction.user.mention}")
            await interaction.response.send_message("Reporter has been DMed.", ephemeral=True)
        else:
            await interaction.response.send_message("User not found.", ephemeral=True)

class BugReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="bug", description="Open a bug report form")
    async def bug(self, ctx):
        modal = BugModal(self.bot, ctx.author)
        await ctx.interaction.response.send_modal(modal)

async def setup(bot):
    await bot.add_cog(BugReport(bot))
