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


@Client.on_message(command(["جراف", "تلجراف"]))
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("- رد على صورة حتى احولها رابط تلجراف .")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4"),
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.reply("اي الي باعتة دا يسطا !!")
        return
    download_location = await client.download_media(
        message=message.reply_to_message,
        file_name="root/downloads/",
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply(message, text=document)
    else:
        await message.reply(f"**- تم تحويل الصورة الى رابط تليجراف بنجاح :\n\nhttps://telegra.ph{response[0]}**", disable_web_page_preview=False)
    finally:
        os.remove(download_location)

# ====== TELEGRAPH ======



@Client.on_message(
    filters.command(["id"])
)
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(
            f"<code>{user_id}</code>",
            quote=True
        )

    elif chat_type in ["group", "supergroup"]:
        _id = ""
        _id += (
            "<b>Chat ID</b>: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>Replied User ID</b>: "
                f"<code>{message.reply_to_message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b>: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        else:
            _id += (
                "<b>User ID</b>: "
                f"<code>{message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b>: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        await message.reply_text(
            _id,
            quote=True
        )



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


