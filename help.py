import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="?", intents=intents)

@bot.command()
async def help(ctx, *, arg=None):
    if arg:
        error_embed = discord.Embed(
            title="❌ Incorrect Syntax",
            description="You used the `?help` command incorrectly.\n\n**Correct Usage:** `?help`",
            color=discord.Color.red()
        )
        error_embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/1106964431285522592/1107045489792254072/IMG_5756.jpg?width=1134&height=1112"
        )

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Config ⚙️", url="https://ravi-docs.gitbook.io/ravi-documentation/"))
        view.add_item(discord.ui.Button(label="Support 📁", url="https://discord.gg/gv2vjKqZP7"))
        view.add_item(discord.ui.Button(label="Invite 💌", url="https://bit.ly/raviticket"))
        view.add_item(discord.ui.Button(label="Policy 📋", url="https://ravi-docs.gitbook.io/ravi-documentation/privacy-policy"))

        return await ctx.reply(embed=error_embed, view=view, allowed_mentions=discord.AllowedMentions.none())

    embed = discord.Embed(
        title="📚 Ravi 2.0 Help Menu",
        description=(
            "Welcome to **Ravi 2.0**!\nHere’s a categorized list of commands.\nUse `?guide` for tutorials and walkthroughs.\n\n"
            "**Prefix:** `?` *(not customizable)*\n"
            "Visit our [Documentation](https://ravi-docs.gitbook.io/) for full details."
        ),
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/1106964431285522592/1107045489792254072/IMG_5756.jpg?width=1134&height=1112"
    )

    embed.add_field(name="🛠️ Management", value="`createchannel`, `removechannel`, `editchannel`, `create-embed`, `c-image`", inline=False)
    embed.add_field(name="👋 Welcome / Leave", value="`set-welcome-channel`, `set-welcome-msg`, `set-autorole`, `disable-welcome`, etc.", inline=False)
    embed.add_field(name="💡 Suggestions", value="`setsuggestions`, `suggest`, `setsuggestionchannel`", inline=False)
    embed.add_field(name="🎫 Tickets", value="`enable-tickets`, `new`, `close`, `add-user`, `remove-user`, etc.", inline=False)
    embed.add_field(name="📋 APMS", value="`setpmod`, `setamod`, `add-pm`, `remove-pm`, etc.", inline=False)
    embed.add_field(name="🧰 Utilities", value="`ping`, `stats`, `afk`, `quote`, `whois`, `calc`, etc.", inline=False)
    embed.add_field(name="👑 Developer Only", value="`eval`, `shutdown`, `restart`, `blst-user`, `setpresence`, etc.", inline=False)

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Invite 💌", url="https://bit.ly/raviticket"))
    view.add_item(discord.ui.Button(label="Support 📁", url="https://discord.gg/gv2vjKqZP7"))
    view.add_item(discord.ui.Button(label="Config ⚙️", url="https://ravi-docs.gitbook.io/ravi-documentation/"))
    view.add_item(discord.ui.Button(label="Policy 📋", url="https://ravi-docs.gitbook.io/ravi-documentation/privacy-policy"))
    view.add_item(discord.ui.Button(label="Help Desk", url="https://ravibot.zohodesk.com", emoji="<:ravi_arrow_dns:912078897858883605>"))

    await ctx.reply(embed=embed, view=view, allowed_mentions=discord.AllowedMentions.none())

# Run the bot with an environment-safe token variable
bot.run(os.getenv("DISCORD_TOKEN"))


