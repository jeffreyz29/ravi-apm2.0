import discord
from database import database
import ast

async def get_embed_from_tag(tag: str) -> discord.Embed | None:
    if not tag.startswith("{embed:") or not tag.endswith("}"):
        return None
    name = tag[len("{embed:"):-1]
    result = database.fetch("SELECT data FROM embeds WHERE name = ?", (name,))
    if not result:
        return None
    try:
        data = ast.literal_eval(result[0][0])
        return discord.Embed(
            title=data.get("title", ""),
            description=data.get("description", ""),
            color=discord.Color.blurple()
        )
    except Exception:
        return None
