# Authored By Certified Coders — v1.2 (2025-11-14)
import time
from pyrogram.types import InlineKeyboardButton
from Tune.utils.formatters import time_to_seconds
from Tune import app
from config import SUPPORT_CHANNEL

LAST_UPDATE_TIME = {}


def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}"
            )
        ],
    ]


def should_update_progress(chat_id):
    now = time.time()
    last = LAST_UPDATE_TIME.get(chat_id, 0)
    if now - last >= 6:
        LAST_UPDATE_TIME[chat_id] = now
        return True
    return False


def stream_markup_timer(_, chat_id, played, dur):
    if not should_update_progress(chat_id):
        return None

    return [
        [
            InlineKeyboardButton(
                text="➕ Beni Grubuna Ekle",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="🩵 Kanal",
                url=SUPPORT_CHANNEL,
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
            ),
        ],
    ]


def stream_markup(_, chat_id):
    return [
        [
            InlineKeyboardButton(
                text="➕ Beni Grubuna Ekle",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="🩵 Kanal",
                url=SUPPORT_CHANNEL,
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
            ),
        ],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"TuneViaPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"TuneViaPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}"
            ),
        ],
    ]


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}"
            )
        ],
    ]


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    short_query = query[:20]
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="●",
                callback_data=f"slider B|{query_type}|{short_query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {short_query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"slider F|{query_type}|{short_query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]