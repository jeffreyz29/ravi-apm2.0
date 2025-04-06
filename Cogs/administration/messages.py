import discord
from discord.ext import commands
from discord import app_commands

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.sticky_messages = {}  # {channel_id: message_content}

    @commands.hybrid_command(name="sticky", description="Set, remove, or list sticky messages.")
    @app_commands.describe(action="set/remove/list", channel="Target channel", message="Sticky message")
    async def sticky(self, ctx, action: str, channel: discord.TextChannel = None, *, message: str = None):
        action = action.lower()

        if action == "set":
            if not channel or not message:
                return await ctx.send("Usage: .sticky set <channel> <message>")
            self.sticky_messages[channel.id] = message
            await ctx.send(f"📌 Sticky message set for {channel.mention}")

        elif action == "remove":
            if not channel:
                return await ctx.send("Usage: .sticky remove <channel>")
            removed = self.sticky_messages.pop(channel.id, None)
            if removed:
                await ctx.send(f"🗑️ Sticky message removed from {channel.mention}")
            else:
                await ctx.send("No sticky message found for that channel.")

        elif action == "list":
            if not self.sticky_messages:
                return await ctx.send("No sticky messages set.")
            embed = discord.Embed(title="📌 Sticky Messages", color=discord.Color.blurple())
            for cid, msg in self.sticky_messages.items():
                ch = self.bot.get_channel(cid)
                name = ch.mention if ch else f"Channel ID {cid}"
                embed.add_field(name=name, value=msg, inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send("Invalid action. Use `set`, `remove`, or `list`.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and not message.author.bot:
            sticky = self.sticky_messages.get(message.channel.id)
            if sticky:
                async for msg in message.channel.history(limit=10):
                    if msg.author.id == self.bot.user.id and msg.content == sticky:
                        return
                await message.channel.send(sticky)


    @commands.hybrid_command(name="edit", description="Edit a bot's own message")
    @app_commands.describe(channel="Channel of the message", msg_id="ID of the message", new_content="New content")
    async def edit(self, ctx, channel: discord.TextChannel, msg_id: int, *, new_content: str):
        try:
            msg = await channel.fetch_message(msg_id)
            if msg.author.id == self.bot.user.id:
                await msg.edit(content=new_content)
                await ctx.send("Message edited.")
            else:
                await ctx.send("That message wasn't sent by me.")
        except Exception as e:
            await ctx.send(f"Failed to edit message: {e}")



import json
import os

    def load_stickies(self):
        os.makedirs('data', exist_ok=True)
        path = 'data/stickies.json'
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump({}, f)
        with open(path, 'r') as f:
            return json.load(f)

    def save_stickies(self, data):
        with open('data/stickies.json', 'w') as f:
            json.dump(data, f, indent=4)

    @commands.hybrid_group(name='sticky', description='Manage sticky messages')
    async def sticky(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Use a subcommand: set, remove, list')

    @sticky.command(name='set')
    async def sticky_set(self, ctx, channel: discord.TextChannel, *, message: str):
        stickies = self.load_stickies()
        g_id = str(ctx.guild.id)
        c_id = str(channel.id)

        if g_id not in stickies:
            stickies[g_id] = {}

        msg = await channel.send(message)
        stickies[g_id][c_id] = {"message": message, "last_message_id": msg.id}
        self.save_stickies(stickies)
        await ctx.send(f"📌 Sticky message set in {channel.mention}.")

    @sticky.command(name='remove')
    async def sticky_remove(self, ctx, channel: discord.TextChannel):
        stickies = self.load_stickies()
        g_id = str(ctx.guild.id)
        c_id = str(channel.id)

        if g_id in stickies and c_id in stickies[g_id]:
            del stickies[g_id][c_id]
            self.save_stickies(stickies)
            await ctx.send(f"🧹 Sticky message removed from {channel.mention}.")
        else:
            await ctx.send("No sticky message found for that channel.")

    @sticky.command(name='list')
    async def sticky_list(self, ctx):
        stickies = self.load_stickies()
        g_id = str(ctx.guild.id)
        if g_id not in stickies or not stickies[g_id]:
            await ctx.send("No sticky messages configured in this server.")
            return

        embed = discord.Embed(title="Sticky Messages", color=discord.Color.blurple())
        for cid, entry in stickies[g_id].items():
            ch = self.bot.get_channel(int(cid))
            embed.add_field(name=f"#{ch}", value=entry["message"][:100], inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot:
            return

        stickies = self.load_stickies()
        g_id = str(message.guild.id)
        c_id = str(message.channel.id)

        if g_id in stickies and c_id in stickies[g_id]:
            try:
                last_id = stickies[g_id][c_id]["last_message_id"]
                old = await message.channel.fetch_message(last_id)
                await old.delete()
            except:
                pass  # message may have already been deleted

            new_msg = await message.channel.send(stickies[g_id][c_id]["message"])
            stickies[g_id][c_id]["last_message_id"] = new_msg.id
            self.save_stickies(stickies)


async def setup(bot):
    await bot.add_cog(Messages(bot))

