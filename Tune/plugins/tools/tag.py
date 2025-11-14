# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.

import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.errors import FloodWait
import re

from Tune import app

SPAM_CHATS = []

def clean_text(text: str) -> str:
    """
    Telegram Markdown V2 için tüm özel karakterleri kaçışlar.
    Nokta (.) ve ters slash (\) dahil koruma sağlar.
    """
    if not text:
        return ""

    # Önce ters eğik çizgileri kaçır
    text = text.replace("\\", "\\\\")
    
    special_chars = r"_*[]()~`>#+-=|{}.!."

    escaped = ""
    for char in text:
        if char in special_chars:
            escaped += "\\" + char
        else:
            escaped += char

    return escaped


async def is_admin(chat_id, user_id):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    return user_id in admin_ids


async def process_members(chat_id, members, text=None, replied=None):
    tagged_members = 0
    usernum = 0
    usertxt = ""

    for member in members:
        if chat_id not in SPAM_CHATS:
            break

        if member.user.is_deleted or member.user.is_bot:
            continue

        tagged_members += 1
        usernum += 1

        # 🔵 YENİ: Sadece ETİKET OLARAK mention üret
        if member.user.username:
            # Username varsa direkt @etiket
            usertxt += f"@{member.user.username} "
        else:
            # Username yoksa isimle mention
            name = clean_text(member.user.first_name or "Kullanıcı")
            usertxt += f"[{name}](tg://user?id={member.user.id}) "

        if usernum == 5:
            try:
                if replied:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    await app.send_message(
                        chat_id,
                        f"{text}\n{usertxt}",
                        disable_web_page_preview=True,
                        parse_mode=ParseMode.MARKDOWN
                    )

                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""

            except FloodWait as e:
                await asyncio.sleep(e.value + 2)
            except Exception as e:
                await app.send_message(chat_id, f"Etiketleme sırasında hata: {str(e)}")
                continue

    if usernum > 0 and chat_id in SPAM_CHATS:
        try:
            if replied:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await app.send_message(
                    chat_id,
                    f"{text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.MARKDOWN
                )

        except Exception as e:
            await app.send_message(chat_id, f"Son part gönderilirken hata: {str(e)}")

    return tagged_members



@app.on_message(
    filters.command(["all", "allmention", "mentionall", "tagall", "utag"], prefixes=["/", "@"])
)
async def tag_all_users(_, message):
    admin = await is_admin(message.chat.id, message.from_user.id)
    if not admin:
        return await message.reply_text("Bu komutu yalnızca yöneticiler kullanabilir.")

    if message.chat.id in SPAM_CHATS:
        return await message.reply_text("Etiketleme zaten çalışıyor. Durdurmak için /cancel yazın.")

    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        return await message.reply_text("Herkesi etiketlemek için metin yazın veya mesaja yanıt verin.")

    try:
        members = [m async for m in app.get_chat_members(message.chat.id)]
        total_members = len(members)

        SPAM_CHATS.append(message.chat.id)

        text = None
        if not replied:
            text = clean_text(message.text.split(None, 1)[1])

        tagged_members = await process_members(
            message.chat.id, members, text=text, replied=replied
        )

        summary_msg = f"""
✅ Etiketleme tamamlandı!

Toplam üye: {total_members}
Etiketlenen: {tagged_members}
"""
        await app.send_message(message.chat.id, summary_msg)

    except FloodWait as e:
        await asyncio.sleep(e.value)

    except Exception as e:
        await app.send_message(message.chat.id, f"Hata: {str(e)}")

    finally:
        try:
            SPAM_CHATS.remove(message.chat.id)
        except:
            pass



@app.on_message(
    filters.command(["admintag", "adminmention", "admins", "report"], prefixes=["/", "@"])
)
async def tag_all_admins(_, message):
    admin = await is_admin(message.chat.id, message.from_user.id)
    if not admin:
        return await message.reply_text("Bu komutu yalnızca yöneticiler kullanabilir.")

    if message.chat.id in SPAM_CHATS:
        return await message.reply_text("Etiketleme zaten çalışıyor. /cancel yazın.")

    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        return await message.reply_text("Yöneticileri etiketlemek için metin yazın veya mesaja yanıt verin.")

    try:
        members = [
            m async for m in app.get_chat_members(
                message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            )
        ]
        total_admins = len(members)

        SPAM_CHATS.append(message.chat.id)

        text = None
        if not replied:
            text = clean_text(message.text.split(None, 1)[1])

        tagged_admins = await process_members(
            message.chat.id, members, text=text, replied=replied
        )

        summary_msg = f"""
✅ Yönetici etiketleme tamamlandı!

Toplam yönetici: {total_admins}
Etiketlenen: {tagged_admins}
"""
        await app.send_message(message.chat.id, summary_msg)

    except FloodWait as e:
        await asyncio.sleep(e.value)

    except Exception as e:
        await app.send_message(message.chat.id, f"Hata: {str(e)}")

    finally:
        try:
            SPAM_CHATS.remove(message.chat.id)
        except:
            pass



@app.on_message(
    filters.command(
        ["stopmention", "cancel", "cancelmention", "offmention", "mentionoff", "cancelall"],
        prefixes=["/", "@"],
    )
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    admin = await is_admin(chat_id, message.from_user.id)

    if not admin:
        return await message.reply_text("Bu komutu yalnızca yöneticiler kullanabilir.")

    if chat_id in SPAM_CHATS:
        SPAM_CHATS.remove(chat_id)
        return await message.reply_text("Etiketleme durduruldu!")
    else:
        return await message.reply_text("Şu anda çalışan bir etiketleme yok.")