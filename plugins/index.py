from pyrogram.errors import FloodWait
from pyrogram.types import ChatPrivileges # যদি অন্য কোথাও লাগে

# আরও কিছু মিডিয়া টাইপ যোগ করা হলো যেগুলো আগে স্কিপ হতো
SUPPORTED_MEDIA_TYPES = [
    enums.MessageMediaType.VIDEO,
    enums.MessageMediaType.AUDIO,
    enums.MessageMediaType.DOCUMENT,
    enums.MessageMediaType.ANIMATION, # GIF বা ছোট ভিডিও
    enums.MessageMediaType.PHOTO       # ছবি (যদি আপনি index করতে চান)
]

async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    BATCH_SIZE = 100  # ২০০ এর বদলে ১০০ রাখা হলো FloodWait এড়াতে
    start_time = time.time()

    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False
            total_messages = lst_msg_id
            total_fetch = lst_msg_id - current
            
            if total_messages <= 0 or total_fetch <= 0:
                await msg.edit(
                    "🚫 No Messages To Index.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close', callback_data='close_data')]])
                )
                return
                
            batches = ceil(total_messages / BATCH_SIZE)
            batch_times = []
            
            await msg.edit(
                f"📊 Indexing Starting......\n"
                f"💬 Total Messages: <code>{total_messages}</code>\n"
                f"📋 Total Fetch: <code> {total_fetch}</code>\n"
                f"⏰ Elapsed: <code>{get_readable_time(time.time() - start_time)}</code>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Cancel', callback_data='index_cancel')]])
            )
            
            for batch in range(batches):
                if temp.CANCEL:
                    break
                    
                batch_start = time.time()
                start_id = current + 1
                end_id = min(current + BATCH_SIZE, lst_msg_id)
                message_ids = list(range(start_id, end_id + 1))
                
                try:
                    # FloodWait হ্যান্ডেল করার জন্য চেক
                    messages = await bot.get_messages(chat, message_ids)
                    if not isinstance(messages, list):
                        messages = [messages]
                except FloodWait as e:
                    logger.warning(f"FloodWait of {e.value} seconds. Sleeping...")
                    await asyncio.sleep(e.value + 1)
                    # ঘুম থেকে উঠে আবার চেষ্টা করা
                    try:
                        messages = await bot.get_messages(chat, message_ids)
                        if not isinstance(messages, list):
                            messages = [messages]
                    except Exception as e:
                        logger.error(f"Failed to fetch batch after FloodWait: {e}")
                        errors += len(message_ids)
                        current += len(message_ids)
                        continue
                except Exception as e:
                    logger.error(f"Error fetching messages: {e}")
                    errors += len(message_ids)
                    current += len(message_ids)
                    continue
                    
                save_tasks = []
                for message in messages:
                    current += 1
                    try:
                        if message.empty:
                            deleted += 1
                            continue
                        elif not message.media:
                            no_media += 1
                            continue
                        elif message.media not in SUPPORTED_MEDIA_TYPES:
                            unsupported += 1
                            continue
                            
                        media = getattr(message, message.media.value, None)
                        if not media:
                            unsupported += 1
                            continue
                            
                        media.file_type = message.media.value
                        media.caption = message.caption
                        save_tasks.append(save_file(media))

                    except Exception:
                        errors += 1
                        continue
                        
                if save_tasks:
                    results = await asyncio.gather(*save_tasks, return_exceptions=True)
                    for result in results:
                        if isinstance(result, Exception):
                            errors += 1
                        else:
                            # ডাটাবেস রেসপন্স অনুযায়ী লজিক
                            ok, code = result
                            if ok:
                                total_files += 1
                            elif code == 0:
                                duplicate += 1
                            elif code == 2:
                                errors += 1
                                
                batch_time = time.time() - batch_start
                batch_times.append(batch_time)
                elapsed = time.time() - start_time
                progress = current - temp.CURRENT
                percentage = (progress / total_fetch) * 100
                avg_batch_time = sum(batch_times) / len(batch_times) if batch_times else 1
                eta = (total_fetch - progress) / BATCH_SIZE * avg_batch_time
                progress_bar = get_progress_bar(int(percentage))
                
                await msg.edit(
                    f"📊 Indexing Progress 📦 Batch {batch + 1}/{batches}\n"
                    f"{progress_bar} <code>{percentage:.1f}%</code>\n\n"
                    f"Total Messages: <code>{total_messages}</code>\n"
                    f"Total Fetched: <code>{total_fetch}</code>\n"
                    f"Fetched: <code>{current}</code>\n"
                    f"Saved: <code>{total_files}</code>\n"
                    f"Duplicates: <code>{duplicate}</code>\n"
                    f"Deleted: <code>{deleted}</code>\n"
                    f"Non-Media: <code>{no_media + unsupported}</code> (Unsupported: <code>{unsupported}</code>)\n"
                    f"Errors: <code>{errors}</code>\n"
                    f"⏱️ Elapsed: <code>{get_readable_time(elapsed)}</code>\n"
                    f"⏰ ETA: <code>{get_readable_time(eta)}</code>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Cancel', callback_data='index_cancel')]])
                )
                
            elapsed = time.time() - start_time
            await msg.edit(
                f"✅ Indexing Completed!\n"
                f"Total Messages: <code>{total_messages}</code>\n"
                f"Total Fetched: <code>{total_fetch}</code>\n"
                f"Fetched: <code>{current}</code>\n"
                f"Saved: <code>{total_files}</code>\n"
                f"Duplicates: <code>{duplicate}</code>\n"
                f"Deleted: <code>{deleted}</code>\n"
                f"Non-Media: <code>{no_media + unsupported}</code> (Unsupported: <code>{unsupported}</code>)\n"
                f"Errors: <code>{errors}</code>\n"
                f"⏱️ Elapsed: <code>{get_readable_time(elapsed)}</code>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close', callback_data='close_data')]])
            )
        except Exception as e:
            logger.exception(e)
            await msg.edit(
                f"❌ Error: <code>{e}</code>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close', callback_data='close_data')]])
            )
