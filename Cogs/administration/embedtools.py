import discord
from discord.ext import commands
from discord import app_commands
import json, os

class EmbedTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = 'data/embeds.json'
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def load_embeds(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_embeds(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @commands.hybrid_command(name='embed_create', description='Create and send a new embed.')
    async def embed_create(self, ctx, title: str, description: str, channel: discord.TextChannel = None):
        embed = discord.Embed(title=title, description=description, color=discord.Color.blurple())
        channel = channel or ctx.channel
        await channel.send(embed=embed)
        await ctx.send(f"✅ Embed sent to {channel.mention}.", ephemeral=True if ctx.interaction else False)

    @commands.hybrid_command(name='embed_save', description='Save an embed with a name.')
    async def embed_save(self, ctx, name: str, title: str, description: str):
        data = self.load_embeds()
        data[name] = {"title": title, "description": description}
        self.save_embeds(data)
        await ctx.send(f"💾 Embed `{name}` saved.")

    @commands.hybrid_command(name='embed_list', description='List all saved embeds.')
    async def embed_list(self, ctx):
        data = self.load_embeds()
        if not data:
            return await ctx.send("❌ No embeds saved.")
        embed = discord.Embed(title="📚 Saved Embeds", color=discord.Color.green())
        for name in data.keys():
            embed.add_field(name=name, value=f"Use `/embed_view {name}`", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='embed_view', description='Preview a saved embed.')
    async def embed_view(self, ctx, name: str):
        data = self.load_embeds()
        if name not in data:
            return await ctx.send("❌ Embed not found.")
        e = data[name]
        embed = discord.Embed(title=e["title"], description=e["description"], color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='embed_send', description='Send a saved embed to a specific channel.')
    async def embed_send(self, ctx, name: str, channel: discord.TextChannel = None):
        data = self.load_embeds()
        if name not in data:
            return await ctx.send("❌ Embed not found.")
        e = data[name]
        embed = discord.Embed(title=e["title"], description=e["description"], color=discord.Color.blue())
        channel = channel or ctx.channel
        await channel.send(embed=embed)
        await ctx.send(f"📨 Embed `{name}` sent to {channel.mention}.")

    @commands.hybrid_command(name='embed_edit', description='Edit an embed message by ID.')
    async def embed_edit(self, ctx, channel: discord.TextChannel, msg_id: int, title: str, description: str):
        try:
            msg = await channel.fetch_message(msg_id)
            if msg.author.id != self.bot.user.id:
                return await ctx.send("❌ I can only edit messages sent by me.")
            embed = discord.Embed(title=title, description=description, color=discord.Color.orange())
            await msg.edit(embed=embed)
            await ctx.send("✅ Embed updated.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command(name='embed_delete', description='Delete a message with an embed by ID.')
    async def embed_delete(self, ctx, channel: discord.TextChannel, msg_id: int):
        try:
            msg = await channel.fetch_message(msg_id)
            await msg.delete()
            await ctx.send("🗑️ Embed message deleted.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(EmbedTools(bot))
