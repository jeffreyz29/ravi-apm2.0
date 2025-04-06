# Ravi 2.0 Discord Bot

**Ravi 2.0** is a powerful and modular Discord bot designed for flexibility, scalability, and user experience.  
Built with `discord.py`, Ravi 2.0 supports both prefix and slash commands, and organizes features into clean, structured cogs.

📖 **Documentation:**  
➡️ [ravi-docs.gitbook.io/ravi-documentation](https://ravi-docs.gitbook.io/ravi-documentation)

---

## ✨ Core Features

- ⚙️ Slash + Prefix hybrid command support
- 🔧 Fully modular cog loading
- 🎫 Advanced ticket system with admin config, tag system, limits, support roles, and transcripts
- 🖐️ Welcome/leave message management
- 🧱 Embed tools for reusing/editing embeds in tickets and welcome flows
- 🎯 Sticky message manager
- 📌 Pin, quote, tag utilities
- 🔍 User and server info commands (`whois`, `serverinfo`, `botinfo`)
- 🧠 Dev-only cog: restart, shutdown, eval, inspect, blacklist, set presence/activity/avatar/banner
- 📋 Command logging + event logging for devs
- 🛠 Invite checker system by category and ID

---

## 📁 Project Structure

```
ravi/
├── bot.py                      # Loads config, sets presence, loads extensions
├── main.py / keep_alive.py     # Optional for hosting / uptime management
├── requirements.txt
├── data/
│   ├── config.json             # Global bot settings (presence, avatar, banner, default prefix)
│   ├── blacklisted_guilds.json
│   ├── prefixes.json           # Per-guild prefixes (managed by prefix system)
├── cogs/
│   ├── administration/
│   │   ├── whois.py
│   │   ├── serverinfo.py
│   │   ├── botinfo.py
│   │   ├── pin.py
│   │   ├── tag.py
│   │   ├── quote.py
│   │   ├── slowmode.py
│   ├── moderation/             # prune, delete, etc.
│   ├── ticketing/              # full-featured ticket manager
│   ├── utility/                # sticky messages, tools
│   ├── dev/                    # developer-only cogs (devtools, command logger, guild logger)
```

---

## 🚀 Setup Guide

1. Install Python dependencies
```bash
pip install -r requirements.txt
```

2. Set your bot token in `bot.py` or use a `.env` for better security

3. Run the bot
```bash
python bot.py
```

---

## ⚙️ Configuration

`data/config.json` example:
```json
{
  "default_prefix": ".",
  "bot": {
    "avatar_url": "https://cdn.example.com/avatar.png",
    "banner_url": "https://cdn.example.com/banner.png",
    "presence": {
      "status": "online",
      "activity": {
        "type": "playing",
        "text": "with code"
      }
    }
  }
}
```

---

## 📌 Quick Notes

- Use `.sticky`, `.quote`, `.tag`, `.pin`, `.unpin` from admin utilities
- All admin/utility/mod logs are separated into modular cog files
- Use `.blacklist`, `.unblacklist`, `.inspectguild`, and `.eval` responsibly (dev-only)

---

> Made for modular growth — built with ❤️ by Ravi 2.0 Devs
