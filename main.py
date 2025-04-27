# ملف main.py

import discord
from discord.ext import commands, tasks
import traceback
import asyncio
import os

# ===== إعدادات البوت =====
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # التوكن من متغير بيئة
PREFIX = "!"
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ===== كلاس التحكم =====
class PlayerManager:
    def __init__(self):
        self.voice_clients = {}  
        self.stay_in_channels = set()  

player = PlayerManager()

# ===== كلاس ريتم لمنع التكرار =====
class RateLimiter:
    def __init__(self):
        self.cooldowns = {}
        self.global_cooldown = 2

    async def wait_before_command(self, ctx):
        now = asyncio.get_event_loop().time()
        user_id = ctx.author.id
        if user_id in self.cooldowns:
            remaining = self.cooldowns[user_id] - now
            if remaining > 0:
                await asyncio.sleep(remaining)
        self.cooldowns[user_id] = now + self.global_cooldown

    def set_global_cooldown(self, seconds):
        self.global_cooldown = seconds

rate_limiter = RateLimiter()

# ===== دالة للحفاظ على البوت شغال (فارغة حالياً) =====
def keep_alive():
    pass

# ===== أوامر البوت =====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    adjust_rate_limit.start()
