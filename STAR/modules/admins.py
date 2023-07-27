from asyncio import QueueEmpty

from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

from pyrogram import Client, filters
from pyrogram.types import Message

from STAR import app
from STAR.config import que
from STAR.database.queue import (
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from STAR.tgcalls import calls

from STAR.utils.filters import command, other_filters
from STAR.utils.decorators import sudo_users_only
from STAR.tgcalls.queues import clear, get, is_empty, put, task_done


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


from STAR.utils.administrator import adminsOnly



@app.on_message(command(["تحديث", f"اعاده تشغيل"]) & other_filters)

async def update_admin(client, message: Message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ تم اعادة **تشغيل البوت** !\n✅ وتم **تحديث** قائمة **المشرفين.**"
    )








@app.on_message(command(["اسكت"]) & other_filters)
async def pause(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "عايزه **راجل** ههه امزح لازم تكون ادمن"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(
            "كله تحت الكنترول مفيش حاجه شغاله"
        )
    elif not await is_music_playing(message.chat.id):
        return await message.reply_text(
            "كله تحت الكنترول مفيش حاجه شغاله"
        )
    await music_off(chat_id)
    await calls.pytgcalls.pause_stream(chat_id)
    await message.reply_text(
        f"هسكت عشان خاطر الراجل المحترم دا : {checking}"
    )


@app.on_message(command(["كمل"]) & other_filters)
async def resume(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "عايزه **راجل** ههه امزح لازم تكون ادمن"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(
            "لا مفيش حاجه تتكمل"
        )
    elif await is_music_playing(chat_id):
        return await message.reply_text(
            "لا مفيش حاجه تتكمل"
        )
    else:
        await music_on(chat_id)
        await calls.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            f"هكمل عشان خاطر الراجل المحترم دا : {checking}"
        )


@app.on_message(command(["ايقاف"]) & other_filters)
async def stop(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "عايزه **راجل** ههه امزح لازم تكون ادمن"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await calls.pytgcalls.leave_group_call(chat_id)
        await message.reply_text(
            f"وقفت عشان خاطر الراجل المحترم دا : {checking}"
        )
    else:
        return await message.reply_text(
            "انت بتسمع حاجه احنا مش سامعينها"
        )


@app.on_message(command(["تخطي"]) & other_filters)
async def skip(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "عايزه **راجل** ههه امزح لازم تكون ادمن"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    chat_title = message.chat.title
    if not await is_active_chat(chat_id):
        await message.reply_text("مفيش حاجه اتخطاها ، يارب اتخطاه هو كمان")
    else:
        task_done(chat_id)
        if is_empty(chat_id):
            await remove_active_chat(chat_id)
            await message.reply_text(
                " __**- مفيش حاجة فقائمة الانتظار**__\n\n**•** `تم مغادرة حساب المساعد`"
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await calls.pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        get(chat_id)["file"],
                    ),
                ),
            )
            await message.reply_text(
                f"يارب اتخطاه زي مالراجل دا اتخطى : {checking}"
            )


@app.on_message(command(["تنظيف"]))
async def stop_cmd(_, message):
    if message.sender_chat:
        return await message.reply_text(
            " عايزه **راجل** ههه امزح لازم تكون ادمن"
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    chat_id = message.chat.id
    checking = message.from_user.mention
    try:
        clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)
    try:
        await calls.pytgcalls.leave_group_call(chat_id)
    except:
        pass
    await message.reply_text(
        f"✅ __تم التنظيف بنجاح **{message.chat.title}**__\n│\n╰ بواسطة {checking}"
    )
