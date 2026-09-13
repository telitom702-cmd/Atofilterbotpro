import os
import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ForceReply
)
from pyrogram.errors import MessageNotModified

from database.users_chats_db import db

logger = logging.getLogger(__name__)

THUMBNAIL_DIR = "thumbnails"
VIDEO_DIR = "downloads"
os.makedirs(THUMBNAIL_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

def get_thumb_path(user_id):
    return os.path.join(THUMBNAIL_DIR, f"{user_id}.jpg")

def get_video_path(user_id, message_id):
    return os.path.join(VIDEO_DIR, f"{user_id}_{message_id}.mp4")

def thumbnail_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🏞️ SET NEW THUMBNAIL", callback_data="set_new_thumb"),
                InlineKeyboardButton("🗑️ DELETE", callback_data="deleteThumbnail")
            ]
        ]
    )

# ডাটাবেস ক্লিন সিস্টেম ফাংশন
async def is_waiting_for_thumb(user_id):
    user_data = await db.get_user(user_id)
    return user_data.get("waiting_for_thumb", False) if user_data else False

async def set_waiting_for_thumb(user_id, status):
    await db.update_user({"id": user_id, "waiting_for_thumb": status})

async def show_thumbnail_menu(bot, chat_id, user_id):
    thumbnail = await db.get_thumbnail(user_id)

    if thumbnail:
        text = "**আপনার থাম্বনেইল আগে থেকেই সেট করা আছে! ✅**"
        try:
            await bot.send_photo(chat_id=chat_id, photo=thumbnail, caption=text, reply_markup=thumbnail_buttons())
        except Exception as e:
            logger.error(f"Thumbnail preview error: {e}")
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=thumbnail_buttons())
    else:
        text = "**আপনার কোনো কাস্টম থাম্বনেইল সেট করা নেই ❌**"
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏞️ SET THUMBNAIL", callback_data="set_new_thumb")]])
        )

@Client.on_message(filters.command("setthumb"))
async def thumbnail_menu(bot, update):
    await show_thumbnail_menu(bot, update.chat.id, update.from_user.id)

@Client.on_message(filters.command("viewthumb"))
async def view_thumbnail(bot, update):
    user_id = update.from_user.id
    thumbnail = await db.get_thumbnail(user_id)
    if not thumbnail:
        await update.reply_text("❌ আপনার কোনো থাম্বনেইল সেট করা নেই।")
        return
    try:
        await bot.send_photo(chat_id=update.chat.id, photo=thumbnail, caption="🖼️ **আপনার বর্তমান থাম্বনেইল**")
    except Exception as e:
        await update.reply_text("⚠️ থাম্বনেইল দেখাতে সমস্যা হয়েছে।")

@Client.on_message(filters.command("delthumb"))
async def delete_thumbnail_command(bot, update):
    user_id = update.from_user.id
    await db.set_thumbnail(user_id, thumbnail=None)
    await set_waiting_for_thumb(user_id, False) # ক্লিন
    await update.reply_text("🗑️ **আপনার কাস্টম থাম্বনেইল সফলভাবে ডিলিট করা হয়েছে!** ✅")

@Client.on_callback_query(filters.regex(r"^(set_new_thumb|deleteThumbnail)$"))
async def thumb_callback(bot, query):
    user_id = query.from_user.id

    if query.data == "set_new_thumb":
        await set_waiting_for_thumb(user_id, True) # সেট করা হলো
        try:
            await query.message.edit_text("**নতুন থাম্বনেইল সেট করতে একটি ছবি (Photo) পাঠান ⏳**")
        except MessageNotModified:
            pass
        await query.answer("ছবির জন্য অপেক্ষা করছি...", show_alert=False)

    elif query.data == "deleteThumbnail":
        await db.set_thumbnail(user_id, thumbnail=None)
        await set_waiting_for_thumb(user_id, False) # ক্লিন
        try:
            await query.message.edit_text("**আপনার কাস্টম থাম্বনেইল সফলভাবে ডিলিট করা হয়েছে!** 🗑️✅")
        except MessageNotModified:
            pass
        await query.answer("থাম্বনেইল ডিলিট হয়েছে!", show_alert=False)

@Client.on_message(filters.photo)
async def save_thumbnail_photo(bot, message):
    user_id = message.from_user.id

    if not await is_waiting_for_thumb(user_id):
        return

    try:
        download_location = get_thumb_path(user_id)
        if os.path.exists(download_location):
            os.remove(download_location)

        await message.download(file_name=download_location)
        thumbnail_file_id = message.photo.file_id

        await db.set_thumbnail(user_id, thumbnail=thumbnail_file_id)
        await set_waiting_for_thumb(user_id, False) # কাজ শেষ, সিস্টেম ক্লিন করে দেওয়া হলো

        await message.reply_text("🎉 **আপনার থাম্বনেইল সফলভাবে সেট করা হয়েছে!** ✅", quote=True)
    except Exception as e:
        logger.exception(f"Save thumbnail error: {e}")
        await message.reply_text("❌ **থাম্বনেইল সেভ করতে সমস্যা হয়েছে।**", quote=True)

@Client.on_message(filters.video | (filters.document & filters.video))
async def handle_video_upload(bot, message: Message):
    user_id = message.from_user.id

    # ইউজার যদি থাম্বনেইল দেওয়ার অবস্থায় থাকে, তবে ভিডিও গ্রহণযোগ্য নয়
    if await is_waiting_for_thumb(user_id):
        await message.reply_text("⚠️ আমি থাম্বনেইলের জন্য ছবির অপেক্ষায় আছি। ভিডিও পাঠাবেন না।\nঅথবা আপনার থাম্বনেইল সেট করা হয়ে গেছে।")
        # সিস্টেম ক্লিন করে দেওয়া হলো, যাতে পরের বার ভিডিও কাজ করে
        await set_waiting_for_thumb(user_id, False)
        return

    thumbnail_file_id = await db.get_thumbnail(user_id)
    
    # থাম্বনেইল না থাকলে নরমাল ভিডিও পাঠিয়ে দিবে
    if not thumbnail_file_id:
        return

    status_msg = await message.reply_text("⏳ **কাস্টম থাম্বনেইল সহ প্রসেস করা হচ্ছে...**")
    video_path = get_video_path(user_id, message.id)

    try:
        await status_msg.edit_text("⬇️ ভিডিও ডাউনলোড হচ্ছে...")
        await message.download(file_name=video_path)

        await status_msg.edit_text("⬆️ থাম্বনেইল সহ আপলোড করা হচ্ছে...")
        await message.reply_video(
            video=video_path,
            thumb=thumbnail_file_id,
            caption=message.caption or "",
            duration=message.video.duration if message.video else None,
            width=message.video.width if message.video else 1280,
            height=message.video.height if message.video else 720,
        )
        await status_msg.edit_text("✅ **ভিডিও সফলভাবে কাস্টম থাম্বনেইল সহ আপলোড করা হয়েছে!**")

    except Exception as e:
        logger.exception(f"Video upload error: {e}")
        await status_msg.edit_text("❌ **ভিডিও প্রসেস করতে সমস্যা হয়েছে!**")
    finally:
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
            except:
                pass
