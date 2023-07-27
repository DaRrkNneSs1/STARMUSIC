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

from STAR.config import BOT_USERNAME
from STAR.config import BOT_NAME
from STAR.config import UPDATE
from STAR.config import OWNER_USERNAME

@Client.on_message(
    command(["صاحب البار","المطور"])
    & filters.group
    & ~filters.edited
)
async def yas(client, message):
    usr = await client.get_chat("OWNER_USERNAME")
    name = usr.first_name
    photo = await client.download_media(usr.photo.big_file_id)
    await message.reply_photo(photo,       caption=f"    ⋆ 𝑺𝒐𝒖𝒓𝒄𝒆 𝑺𝒕𝒂𝒓 ⋆ **\n\n‍ ⤹ DeV . :{name}\n ⤹ UsEr . :@{usr.username}\n ⤹ Id . :{usr.id}\n ⤹ Bio . :{usr.bio}\n\n ⤹ DeV ChanneL. @{UPDATE} **", 
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        name, url=f"https://t.me/{usr.username}")
                ],
            ]
        ),
    )
    
   
