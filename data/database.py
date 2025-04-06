import sqlite3
import os

DB_PATH = "data/ravi.db"
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def setup():
    # Tags Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        tag_id TEXT,
        content TEXT,
        created_by INTEGER
    )
    """)

    # Reminders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        remind_at INTEGER
    )
    """)

    # DM Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dm_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT,
        timestamp TEXT
    )
    """)

    # Tickets Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        channel_id INTEGER,
        opener_id INTEGER,
        status TEXT,
        created_at TEXT
    )
    """)

    # Embeds Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        data TEXT,
        created_by INTEGER
    )
    """)

    # Auto Roles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS autoroles (
        guild_id INTEGER PRIMARY KEY,
        role_ids TEXT
    )
    """)

    # Guild Config Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guild_config (
        guild_id INTEGER PRIMARY KEY,
        prefix TEXT DEFAULT '.',
        language TEXT DEFAULT 'en',
        welcome_channel_id INTEGER,
        leave_channel_id INTEGER
    )
    """)

    # Invite Whitelist Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invite_whitelist (
        guild_id INTEGER,
        category_id INTEGER,
        channel_id INTEGER,
        PRIMARY KEY (guild_id, category_id, channel_id)
    )
    """)

    # Boost / Bye Config Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS boost_config (
        guild_id INTEGER PRIMARY KEY,
        boost_message TEXT,
        boost_channel_id INTEGER,
        bye_message TEXT,
        bye_channel_id INTEGER
    )
    """)

    # Command Usage Stats Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS command_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        guild_id INTEGER,
        command TEXT,
        used_at TEXT
    )
    """)

    conn.commit()

def insert(query, values):
    cursor.execute(query, values)
    conn.commit()

def fetch(query, values=()):
    cursor.execute(query, values)
    return cursor.fetchall()

def execute(query, values=()):
    cursor.execute(query, values)
    conn.commit()

setup()
