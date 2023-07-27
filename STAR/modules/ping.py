import time
from datetime import datetime

import psutil
from STAR import Music_START_TIME, app
from STAR.utils.time import get_readable_time
from pyrogram import filters
from STAR.utils.filters import command

from STAR.utils.filters import command, other_filters


async def bot_sys_stats():
    bot_uptime = int(time.time() - Music_START_TIME)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
- وقت التشغيل : {get_readable_time((bot_uptime))}
الذاكرة: {cpu}%
الرام: {mem}%
المساحة: {disk}%
"""
    return stats


@app.on_message(command("بينج"))
async def ping(_, message):
    uptime = await bot_sys_stats()
    start = datetime.now()
    response = await message.reply_text("- ثوان")
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit(
        f"**- بينج البوت**\n {resp} مللي ثانية"
    )
