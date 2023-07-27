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




@Client.on_message(command(["ا", "ايدي"]))
async def who_is(client, message):
    """انتظر لحظه !"""
    status_message = await message.reply_text(
        "انتظر لحظه !"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("no valid user_id / message specified")
        return
    
    first_name = from_user.first_name or ""
    last_name = from_user.last_name or ""
    username = from_user.username or ""
    
    message_out_str = (
        "<b>⋆ 𝑺𝒐𝒖𝒓𝒄𝒆 𝑺𝒕𝒂𝒓 ⋆</b>\n\n"
        f"<b>• Name : <a href='tg://user?id={from_user.id}'>{first_name}</a></b>\n"
        f"<b>• ID :</b> <code>{from_user.id}</code>\n"
        f"<b>• User :</b> @{username}\n"
        f"<b>• Bio :</b> {usr.bio}
        f"<b>Is Deleted:</b> True\n" if from_user.is_deleted else ""
        f"<b>Is Verified:</b> True" if from_user.is_verified else ""
        f"<b>Is Scam:</b> True" if from_user.is_scam else ""
        # f"<b>Is Fake:</b> True" if from_user.is_fake else "
    )

    if message.chat.type in ["supergroup", "channel"]:
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "<b>• Lastseen :</b> <code>"
                f"{joined_date}"
                "</code>\n"
                "-"
            )
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            caption=message_out_str,
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:
        await message.reply_text(
            text=message_out_str,
            quote=True,
            disable_notification=True
        )
    await status_message.delete()
