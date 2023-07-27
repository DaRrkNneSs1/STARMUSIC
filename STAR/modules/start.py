import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, UserNotParticipant
from pytgcalls import (__version__ as pytover)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from STAR.utils.filters import command


from STAR.config import BOT_USERNAME
from STAR.config import START_PIC
from STAR.config import BOT_NAME
from STAR.config import UPDATE
from STAR.config import OWNER_USERNAME



@Client.on_message(command("/start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_PIC}",
        caption=f""" ‹ مرحبا بك عزيزي في بوت **{BOT_NAME}**
        
- اضغط على زر ‹ الاوامر › لمعرفة الأوامر ›

- اضغط على زر ‹ الدعم › للتواصل مع المطورين ›""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "‹ الدعم ›", callback_data="cbabout"),
                ],
                [
                    InlineKeyboardButton(
                        "‹ الاوامر ›", callback_data="cbevery")
                ],
                [
                    InlineKeyboardButton(
                        "‹ اضفني الى مجموعتك ›", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
           ]
        ),
    )



@Client.on_message(
    command(["المطور","مطور"])
    & filters.group
    & ~filters.edited
)
async def huhh(client, message):
    usr = await client.get_chat("OWNER_USERNAME")
    name = usr.first_name
    photo = await app.download_media(usr.photo.big_file_id)
    await message.reply_photo(photo,       caption=f"""⋆ 𝑺𝒐𝒖𝒓𝒄𝒆 𝑺𝒕𝒂𝒓 ⋆ **\n\n‍ ⤹ DeV . :{name}\n ⤹ UsEr . :@{usr.username}\n ⤹ Id . :{usr.id}\n ⤹ Bio . :{usr.bio}\n\n ⤹ DeV ChanneL. @{UPDATE} **""", 
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        name, url=f"https://t.me/{usr.username}")
                ],
            ]
        ),
)



@Client.on_message(
    command(["سورس","السورس","star","مطوريين","المطوريين","مطورين","المطورين","مطورين السورس","صاحب السورس","مطور السورس"])
    & ~filters.edited
)
async def huhh(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://graph.org/file/05897feb515bc6f479625.jpg",
        caption=f"""⤹ 𝘛𝘏𝘌 𝘉𝘌𝘚𝘛 𝘚𝘖𝘜𝘙𝘊𝘌 𝘖𝘕 𝘛𝘌𝘓𝘌𝘎𝘙𝘈𝘔 ⤸""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⤹ DeV RoWeS ⤸", url=f"https://t.me/R7_OX"), 
                
                    InlineKeyboardButton(
                        "⤹ DeV SiMo ⤸", url=f"https://t.me/DaRrKNneSs_1"),
                ],[
                    InlineKeyboardButton(
                        "⋆ 𝑺𝒐𝒖𝒓𝒄𝒆 𝑺𝒕𝒂𝒓 ⋆", url=f"https://t.me/S0URCE_STAR"),
                ],

            ]

        ),

)
