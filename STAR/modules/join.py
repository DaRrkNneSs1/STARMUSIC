import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, FloodWait

from STAR import app, ASSUSERNAME
from STAR.utils.decorators import sudo_users_only, errors
from STAR.utils.administrator import adminsOnly
from STAR.utils.filters import command
from STAR.tgcalls import client as USER


@app.on_message(
    command(["انضم", "ادخل", "نضم"]) & ~filters.private & ~filters.bot
)
@errors
async def addchannel(client, message):
    if message.sender_chat:
        return await message.reply_text(
            "عايزه **راجل** ههه امزح لازم تكون ادمن"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    chid = message.chat.id
    try:
        invite_link = await message.chat.export_invite_link()
        if "+" in invite_link:
            kontol = (invite_link.replace("+", "")).split("t.me/")[1]
            link_bokep = f"https://t.me/joinchat/{kontol}"
    except:
        await message.reply_text(
            "**- ازاي اضيفة وانا مش مشرف؟**",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = f"{ASSUSERNAME}"

    try:
        await USER.join_chat(link_bokep)
    except UserAlreadyParticipant:
        await message.reply_text(
            f" **{user.first_name} - موجود بالفعل **",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f" __**- المساعد ({user.first_name}) فشل في الانضمام اكتب تحديث وارجع اكتب انضم."
            f"\n\n- تأكد ان الحساب المساعد مش محظور من المجموعه {user.first_name}",
        )
        return


@USER.on_message(filters.group & command(["غادر", "اطلع", "برا"]))
async def rem(USER, message):
    if message.sender_chat:
        return await message.reply_text(
            "عايزه **راجل** ههه امزح لازم تكون ادمن"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    try:
        await USER.send_message(
            message.chat.id,
            "انا غلطان اني جيت اصلاً المره الجايه كلمو المطور عشان يجيبني",
        )
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "خخخ مخلاص طالع </b>"
        )

        return


@app.on_message(command(["userbotleaveall", "leaveall"]))
@sudo_users_only
async def bye(client, message):
    left = 0
    sleep_time = 0.1
    lol = await message.reply("**Assistant leaving all groups**\n\n`Processing...`")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            await asyncio.sleep(sleep_time)
            left += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await lol.edit(f"🏃‍♂️ `Assistant leaving...`\n\n» **Left:** {left} chats.")
