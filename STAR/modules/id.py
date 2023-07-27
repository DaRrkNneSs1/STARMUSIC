import os
import asyncio
import time
import shlex
import requests
from datetime import datetime
from STAR.utils.filters import command

from STAR.utils.filters import command, other_filters
from pyrogram.errors import UserNotParticipant
from STAR.utils.extract_user import extract_user, last_online
from telegraph import upload_file
from typing import Callable, Coroutine, Dict, List, Tuple, Union
from json import JSONDecodeError
from pyrogram import Client, filters
from STAR.config import BOT_USERNAME

iddof = []
@Client.on_message(
    command(["قفل الايدي","تعطيل الايدي"])
    & filters.group
    & ~filters.edited
)
async def iddlock(client, message):
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in ["creator", "administrator"]:
      if message.chat.id in iddof:
        return await message.reply_text("تم معطل من قبل🔒")
      iddof.append(message.chat.id)
      return await message.reply_text("تم تعطيل الايدي بنجاح ✅🔒")
   else:
      return await message.reply_text("عايزه **راجل** ههه امزح لازم تكون ادمن")

@Client.on_message(
    command(["فتح الايدي","تفعيل الايدي"])
    & filters.group
    & ~filters.edited
)
async def iddopen(client, message):
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in ["creator", "administrator"]:
      if not message.chat.id in iddof:
        return await message.reply_text("الايدي مفعل من قبل ✅")
      iddof.remove(message.chat.id)
      return await message.reply_text("تم فتح الايدي بنجاح ✅🔓")
   else:
      return await message.reply_text("عايزه **راجل** ههه امزح لازم تكون ادمن")




@Client.on_message(
    command(["ايدي","id","ا"])
    & filters.group
    & ~filters.edited
)
async def iddd(client, message):
    if message.chat.id in iddof:
      return
    usr = await client.get_chat(message.from_user.id)
    name = usr.first_name
    photo = await client.download_media(usr.photo.big_file_id)
    await message.reply_photo(photo,       caption=f"""⤹ NaMe. : {message.from_user.mention}\n ⤹ UseR. : @{message.from_user.username}\n ⤹ Id. : `{message.from_user.id}`\n ⤹ Bio. :{usr.bio}\n ⤹ ChaT: {message.chat.title}\n⤹ iD GrouP : `{message.chat.id}`""", 
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        name, url=f"https://t.me/{message.from_user.username}")
                ],
            ]
        ),
    )


