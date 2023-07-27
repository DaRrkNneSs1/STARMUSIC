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
    command(["رويس","rowes"])
    & filters.group
    & ~filters.edited
)
async def yas(client, message):
    usr = await client.get_chat("R7_OX")
    name = usr.first_name
    photo = await client.download_media(usr.photo.big_file_id)
    await message.reply_photo(photo,       caption=f"معلومات صاحب السورس :-\n⤹ NaMe :{name}\n ⤹ UsEr :@{usr.username}\n ⤹ Id :{usr.id}\n ⤹ BiO :{usr.bio}", 
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        name, url=f"https://t.me/{usr.username}")
                ],
            ]
        ),
    )