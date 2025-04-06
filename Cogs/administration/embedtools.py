import discord
from discord.ext import commands
from discord import app_commands
from database import database

class EmbedTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="embed_save", description="Save an embed with a name")
    @app_commands.describe(name="Name to save the embed under", content="Text to include in the embed")
    async def embed_save(self, ctx, name: str, *, content: str):
        data = {"title": f"Embed: {name}", "description": content}
        database.insert(
            "INSERT INTO embeds (name, data, created_by) VALUES (?, ?, ?)",
            (name, str(data), ctx.author.id)
        )
        await ctx.send(f"✅ Embed `{name}` saved.")

    @commands.hybrid_command(name="embed_show", description="Show a saved embed")
    @app_commands.describe(name="Name of the embed to display")
    async def embed_show(self, ctx, name: str):
        result = database.fetch("SELECT data FROM embeds WHERE name = ?", (name,))
        if not result:
            return await ctx.send("Embed not found.")
        data = eval(result[0][0])  # stored as str(dict)
        embed = discord.Embed(title=data.get("title"), description=data.get("description"), color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="embed_edit", description="Edit the contents of a saved embed")
    @app_commands.describe(name="Name of the embed", new_content="New embed description")
    async def embed_edit(self, ctx, name: str, *, new_content: str):
        result = database.fetch("SELECT id FROM embeds WHERE name = ?", (name,))
        if not result:
            return await ctx.send("Embed not found.")
        data = {"title": f"Embed: {name}", "description": new_content}
        database.execute("UPDATE embeds SET data = ? WHERE name = ?", (str(data), name))
        await ctx.send(f"✏️ Embed `{name}` updated.")

    @commands.hybrid_command(name="embed_delete", description="Delete a saved embed")
    @app_commands.describe(name="Name of the embed to delete")
    async def embed_delete(self, ctx, name: str):
        database.execute("DELETE FROM embeds WHERE name = ?", (name,))
        await ctx.send(f"🗑️ Embed `{name}` deleted.")

    @commands.hybrid_command(name="embed_list", description="List all saved embed names")
    async def embed_list(self, ctx):
        rows = database.fetch("SELECT name FROM embeds")
        if not rows:
            return await ctx.send("No embeds saved.")
        embed = discord.Embed(title="📂 Saved Embeds", description="Available embeds:", color=discord.Color.teal())
        for row in rows:
            embed.add_field(name=row[0], value=f"Use `/embed_show {row[0]}`", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EmbedTools(bot))
