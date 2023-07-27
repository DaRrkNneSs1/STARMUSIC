from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from STAR.config import BOT_USERNAME
from STAR.config import START_PIC
from STAR.config import OWNER_ID
from STAR.config import ASSUSERNAME
from STAR.config import UPDATE
from STAR.config import SUPPORT
from STAR.config import OWNER_USERNAME
from STAR.config import BOT_NAME


@Client.on_callback_query(filters.regex("cbhome"))
async def cbhome(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""‹ مرحبا بك عزيزي في بوت **{BOT_NAME}**
        
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


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds_set(_, query: CallbackQuery):
        await query.answer("commands menu")
        await query.edit_message_text(
        f"""‹ مرحبا بك في قسم الاوامر  › [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) 

- يمكنك معرفة الاوامر عن طريق الازرار أدناه -""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("‹ اوامر المطورين ›", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("Everyone", callback_data="cbevery"),
                    InlineKeyboardButton("‹ اوامر المشرفين ›", callback_data="cbadmins"),
                ],[
                    InlineKeyboardButton("‹ رجوع ›", callback_data="cbhome")
                ],
            ]
        ),
    ) 


# اوامر الاعضاء !!
@Client.on_callback_query(filters.regex("cbevery"))
async def all_set(_, query: CallbackQuery):
    await query.answer("Everyone menu")
    await query.edit_message_text(
    f""" ‹ مرحبا بك في قسم الاوامر ›

- شغل | بالرد على ملف او اسم اغنية للتشغيل  .

- يوت | باسم الاغنية لتحميل اغنية من اليوتيوب .

- رابط | لحصول على رابط اغنية من يوتيوب .

- بينج | لفحص بنك البوت والسرعة الممكنه .

- جراف | لتحويل صورة الى رابط تليجراف .

- قناة المطور | @{UPDATE}""",
        reply_markup=InlineKeyboardMarkup(
            [
              [
                    InlineKeyboardButton(
                        "‹ اوامر المشرفين ›", callback_data="cbadmins"),
                    InlineKeyboardButton(
                        "‹ اوامر المطورين ›", callback_data="cbsudo")
                ],
              [InlineKeyboardButton("‹ رجوع ›", callback_data="cbhome")]]
        ),
    )


# اوامر المطورين !!
@Client.on_callback_query(filters.regex("cbsudo"))
async def sudo_set(_, query: CallbackQuery):
    await query.answer("sudo menu")
    await query.edit_message_text(
    f""" ‹ مرحبا بك في قسم اوامر المطورين ›

- الاحصائيات | لرؤية احصائيات البوت اخر شهر .

- ريستارت | اعادة تشغيل البوت وتحسين السرعة .

- اذاعة | لعمل اذاعة في المجموعات بدون تثبيت .

- اذاعة بالتثبيت | لعمل اذاعة لكل المجموعات مع التثبيت .

- المغادرة | لمغادرة حساب المساعد من المجموعات .

- قناة المطور | @{UPDATE}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("‹ رجوع ›", callback_data="cbevery")
                ],
            ]
        ),
    )


# اوامر المشرفين
@Client.on_callback_query(filters.regex("cbadmins"))
async def admin_set(_, query: CallbackQuery):
    await query.answer("admins menu")
    await query.edit_message_text(
    f""" ‹ مرحبا بك في قسم اوامر المشرفين ›

- ايقاف | ايقاف تشغيل الاغنية في المجموعة .

- تخطي | تخطي التالية الأغنية في المجموعة .

- اسكت | لإيقاف تشغيل الأغنية مؤقتا .

- كمل | استمرار التشغيل المتوقف مؤقتا .

- تنظيف | لتنظيف التشغيل وتحسين سرعة البوت .

- انضم | للانضمام حساب المساعد الى المجموعة .

- غادر | لمغادرة حساب المساعد المجموعة .

- قناة المطور | @{UPDATE}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("‹ رجوع ›", callback_data="cbevery")
                ],
            ]
        ),
    )


# Bot about & Information
@Client.on_callback_query(filters.regex("cbabout"))
async def about_set(_, query: CallbackQuery):
    await query.edit_message_text(
    f"""‹ مرحبا بك في قسم الدعم  › [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})

- يمكنك الانضمام والتواصل مع المطورين عن طريق الازرار أدناه""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("‹ جروب الدعم ›", url=f"https://t.me/{SUPPORT}"),
                    InlineKeyboardButton("‹ قناة المطور ›", url=f"https://t.me/{UPDATE}")
                ],[
                    InlineKeyboardButton("‹ مطور البوت ›", url=f"https://t.me/{OWNER_USERNAME}"),
                    InlineKeyboardButton("‹ حساب المساعد ›", url=f"https://t.me/{ASSUSERNAME}")
                ],[
                    InlineKeyboardButton("‹ السورس ›", url="https://t.me/S0URCE_STAR")
                ],[
                    InlineKeyboardButton("‹ رجوع ›", callback_data="cbhome")
                ],
            ]
        ),
    )


