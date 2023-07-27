import asyncio

import os
import time
import requests
from pyrogram import filters
import random
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from STAR.filters import command
from random import  choice, randint

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


