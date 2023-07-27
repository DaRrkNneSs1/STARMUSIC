import asyncio
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters, Client
from STAR import app
from STAR.config import OWNER_ID

@app.on_message(filters.command(['بوت','/start'], prefixes=""))
async def yas(client: Client, message: Message):
    me = await client.get_me()
    bot_username = me.username
    bot_name = me.first_name
    star = message.from_user.mention
    button = InlineKeyboardButton("اضف البوت الي مجموعتك🏅", url=f"https://t.me/{bot_username}?startgroup=true")
    keyboard = InlineKeyboardMarkup([[button]])
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if user_id == 5749137933:
             rank = "**‹ مـالك الـسورس ›**"
        elif user_id == 830359032:
             rank = "**‹ مـالك الـسـورس ›**"
        elif user_id == OWNER_ID:
             rank = "‹ مـالك الـبوت ›"
        elif member.status == 'creator':
             rank = "**‹ مـالك الـبـار ›**"
        elif member.status == 'administrator':
             rank = "**‹ مـشـرف الـبـار ›**"
        else:
             rank = "**‹ لاسف انت عضو فقير ›**"
    except Exception as e:
        print(e)
        rank = "مش عرفنلو مله ده"
    async for photo in client.iter_profile_photos("me", limit=1):
                    await message.reply_photo(photo.file_id,       caption=f"""**نعم حبيبي :** {star} \n** انا اسمي  :** {bot_name} \n**رتبتك هي :** {rank}""", reply_markup=keyboard)


