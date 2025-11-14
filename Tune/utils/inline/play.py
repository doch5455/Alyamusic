import time
from pyrogram.types import InlineKeyboardButton
from Tune.utils.formatters import time_to_seconds
from Tune import app

LAST_UPDATE_TIME = {}


# ——————————————————————————————
# SADE PANEL (S_B_1 – S_B_2 – CLOSE)
# ——————————————————————————————
async def base_buttons(_):
    bot = await app.get_me()
    username = bot.username

    return [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],   # Beni Grubuna Ekle
                url=f"https://t.me/{username}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_2"],   # Kanal
                url=_["SUPPORT_CHANNEL"]
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],   # Kapat
                callback_data="close"
            )
        ]
    ]


# ——————————————————————————————
# PROGRESS SİSTEMİ ARTIK KULLANILMIYOR
# ——————————————————————————————
def should_update_progress(chat_id):
    return False   # TIMER KAPATILDI → BAR KULLANILMIYOR


# BAR TAMAMEN KALDIRILDI
def generate_progress_bar(played_sec, duration_sec):
    return ""


# ——————————————————————————————
# TRACK MARKUP
# ——————————————————————————————
async def track_markup(_, videoid, user_id, channel, fplay):
    return await base_buttons(_)


# ——————————————————————————————
# TIMER PANEL (BAR YOK)
# ——————————————————————————————
async def stream_markup_timer(_, chat_id, played, dur):
    return await base_buttons(_)


# ——————————————————————————————
# STREAM MARKUP (SADE)
# ——————————————————————————————
async def stream_markup(_, chat_id):
    return await base_buttons(_)


# ——————————————————————————————
# PLAYLIST MARKUP
# ——————————————————————————————
async def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return await base_buttons(_)


# ——————————————————————————————
# LIVESTREAM MARKUP
# ——————————————————————————————
async def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return await base_buttons(_)


# ——————————————————————————————
# SLIDER MARKUP (OK TUŞLARI SİLİNDİ)
# ——————————————————————————————
async def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    return await base_buttons(_)