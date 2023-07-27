import aiofiles
import ffmpeg
import asyncio
import os
import shutil
import psutil
import subprocess
import requests
import aiohttp
import yt_dlp

from os import path
from typing import Union
from asyncio import QueueEmpty
from PIL import Image, ImageFont, ImageDraw
from typing import Callable

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    Voice,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant

from STAR.tgcalls import calls, queues
from STAR.tgcalls.calls import client as ASS_ACC
from STAR.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from STAR import app
import STAR.tgcalls
from STAR.tgcalls import youtube
from STAR.tgcalls.youtube import download
from STAR.tgcalls import convert as cconvert
from STAR.config import (
    DURATION_LIMIT,
    que,
    SUDO_USERS,
    BOT_ID,
    ASSNAME,
    ASSUSERNAME,
    ASSID,
    SUPPORT,
    UPDATE,
    BOT_USERNAME,
)
from STAR.utils.filters import command
from STAR.utils.filters import command, other_filters
from STAR.utils.decorators import errors, sudo_users_only
from STAR.utils.administrator import adminsOnly
from STAR.utils.errors import DurationLimitError
from STAR.utils.gets import get_url, get_file_name
from STAR.modules.admins import member_permissions


# plus
chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
flex = {}


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("SR/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("SR/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    command(["الموسيقى", f"musicplayer@{BOT_USERNAME}"])
    & ~filters.edited
    & ~filters.bot
    & ~filters.private
)
async def hfmm(_, message):
    global DISABLED_GROUPS
    if message.sender_chat:
        return await message.reply_text(
            "عايزه **راجل** ههه امزح لازم تكون ادمن"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    try:
        user_id = message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text("لتشغيل البوت اكتب الموسيقى on لاطفاء البوت اكتب الموسيقى off يرجى ملاحظة ان الامر للمطورين فقط")
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status in ["ON", "on", "On"]:
        lel = await message.reply("`انتظر قليلا ..`")
        if message.chat.id not in DISABLED_GROUPS:
            await lel.edit(
                f" __- البوت فعلا مطفي**{message.chat.title}**__"
            )
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f" __- تم تشغيل البوت بنجاح **{message.chat.title}**__"
        )

    elif status in ["OFF", "off", "Off"]:
        lel = await message.reply("__' انتظر قليلا ...'__")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit(
                f" __- تم تشغيل بنجاح **{message.chat.title}**__"
            )
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f" __- تم اطفاء البوت بنجاح**{message.chat.title}**__"
        )
    else:
        await message.reply_text("لتشغيل البوت اكتب الموسيقى on لاطفاء البوت اكتب الموسيقى off يرجى ملاحظة ان الامر للمطورين فقط")


@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
async def closed(_, query: CallbackQuery):
    from_user = query.from_user
    permissions = await member_permissions(query.message.chat.id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await query.answer(
            "معندكش الصلاحية دي\n"
            + f"السبب : {permission}",
            show_alert=True,
        )
    await query.message.delete()


# play
@Client.on_message(
    command(["شغل", f"تشغيل"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    user_id = message.from_user.id
    if message.sender_chat:
        return await message.reply_text(
            "عايزه **راجل** ههه امزح لازم تكون ادمن"
        )

    if message.chat.id in DISABLED_GROUPS:
        await message.reply(
            "**كلم المطور يشوفلك الحل او هزقه**"
        )
        return
    lel = await message.reply("‹ خلي عندك صبر ›")

    chid = message.chat.id

    c = await app.get_chat_member(message.chat.id, BOT_ID)
    if c.status != "administrator":
        await lel.edit(
            f"I need to be admin with some permissions:\n\n❌ **can_manage_voice_chats:** To manage voice chats\n❌ **can_delete_messages:** To delete music's searched waste\n❌ **can_invite_users**: For inviting assistant to chat"
        )
        return
    if not c.can_manage_voice_chats:
        await lel.edit(
            "- اديني الصلاحية دي عشان اقدر اشغل."
            + "\n- صلاحية الاتصال"
        )
        return
    if not c.can_delete_messages:
        await lel.edit(
            "- اديني الصلاحية دي عشان اقدر اشغل."
            + "\n- حذف رسائل"
        )
        return
    if not c.can_invite_users:
        await lel.edit(
            "- اديني الصلاحية دي عشان اقدر اشغل."
            + "\n- اضافة مستخدمين"
        )
        return

    try:
        b = await app.get_chat_member(message.chat.id, ASSID)
        if b.status == "kicked":
            await message.reply_text(
                f"الـ {ASSNAME} (@{ASSUSERNAME}) حساب المساعد محظور فك حظره اولا **{message.chat.title}**\n\n- بعدين اكتب انضم او ادخل"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ASS_ACC.join_chat(f"{message.chat.username}")
                await message.reply(
                    f"✅ **{ASSNAME} تم انضمام المساعد -**",
                )
                await remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_text(
                    f" __**- فشل الحساب المساعد في الانضمام والسبب *__\n\n**Reason**:{e}"
                )
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    kontol = (invite_link.replace("+", "")).split("t.me/")[1]
                    link_bokep = f"https://t.me/joinchat/{kontol}"
                await ASS_ACC.join_chat(link_bokep)
                await message.reply(
                    f"✅ **{ASSNAME} تم انضمام المساعد -**",
                )
                await remove_active_chat(message.chat.id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(
                    f" __**- فشل الحساب المساعد في الانضمام والسبب**__\n\n**Reason**:{e}"
                )

    await message.delete()
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        url = f"https://t.me/{UPDATE}"
        title = "Wa"
        thumb_name = "https://graph.org/file/ab6b8fa496fd7d8f75b0e.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("‹ تحكم اونلاين ›", callback_data="cbmenu"),
                ], 
                    
                [InlineKeyboardButton(text="‹ حذف ›", callback_data="cls")],
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await cconvert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("‹ تحكم اونلاين ›", callback_data="cbmenu"),
                    ],   
                        
                    [InlineKeyboardButton(text="‹ حذف ›", callback_data="cls")],
                ]
            )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://graph.org/file/ab6b8fa496fd7d8f75b0e.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="YouTube 🎬", url="https://youtube.com")]]
            )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://graph.org/file/ab6b8fa496fd7d8f75b0e.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="YouTube 🎬", url="https://youtube.com")]]
            )
        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❌ Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.edit(
                                f"‹ خلي عندك صبر ›"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"‹ خلي عندك صبر ›"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"‹ خلي عندك صبر ›"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"‹ خلي عندك صبر ›"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.edit(
                    f"‹ خلي عندك صبر ›"
                )
                print(f"[{url_suffix}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, url, my_hook)
        file_path = await cconvert(x)
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "‹ الرد على ملف صوتي او اعطاء شيء للبحث ›"
            )
        await lel.edit("‹ خلي عندك صبر ›")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("‹ خلي عندك صبر ›")
        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "- لم يتم العثور على الأغنية اكتب اسمها الكامل ."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("‹ تحكم اونلاين ›", callback_data="cbmenu"),
                ],
                    
                [InlineKeyboardButton(text="‹ حذف ›", callback_data="cls")],
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❌ Videos longer than {DURATION_LIMIT} minutes aren't allowed to play!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.edit(
                                f"‹ خلي عندك صبر ›"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"‹ خلي عندك صبر ›"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"‹خلي عندك صبر ›"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"‹ خلي عندك صبر ›"
                            )
                        print(
                            f"[{url_suffix}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.edit(
                    f"‹ تم التشغيل ›"
                )
                print(f"[{url_suffix}] Downloaded| Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, url, my_hook)
        file_path = await cconvert(x)

    if await is_active_chat(message.chat.id):
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="https://graph.org/file/15dd5ca3978e826ffc726.jpg",
            caption="**⤹ تم الاضافة الي قائمة التشغيل . **\n\n**⤹ معلومات التشغيل** [⤹ اضغط هنا ]({})**\n\n**- تم التشغيل بواسطة : {}**\n**⤹ قائمة التشغيل  : {}**".format(
                url,
                message.from_user.mention(),
                position,
            ),
            reply_markup=keyboard,
        )
    else:
        try:
            await calls.pytgcalls.join_group_call(
                message.chat.id,
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception:
            return await lel.edit(
                "- ازاي اشغل وانتو مش فاتحين المكالمة ."
            )

        await music_on(message.chat.id)
        await add_active_chat(message.chat.id)
        await message.reply_photo(
            photo="https://graph.org/file/15dd5ca3978e826ffc726.jpg",
            reply_markup=keyboard,
            caption="**⤹ يتم التشغيل الآن .** \n\n **⤹ معلومات الاغنية** .[ اضغط هنا ]({})\n\n**- تم التشغيل بواسطة : {}**\n- اسم الجروب : {}**".format(
                url, message.from_user.mention(), message.chat.title
            ),
        )

    os.remove("https://graph.org/file/ab6b8fa496fd7d8f75b0e.jpg")
    return await lel.delete()
        


                 
                                
   
                
