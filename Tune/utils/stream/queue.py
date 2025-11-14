import asyncio
from typing import Union

from Tune.misc import db
from Tune.utils.formatters import check_duration, seconds_to_min
from config import autoclean, time_to_seconds


async def put_queue(
    chat_id: int,
    original_chat_id: int,
    file: str,
    title: str,
    duration: str,
    user: str,
    vidid: str,
    user_id: int,
    stream: str,
    forceplay: Union[bool, str] = None,
):
    """Sıraya yeni müzik/video ekler."""

    # Büyük harfe çeviri
    title = title.title()

    # Süreyi saniyeye çevir (3 saniye tolerans)
    try:
        duration_in_seconds = max(time_to_seconds(duration) - 3, 0)
    except:
        duration_in_seconds = 0

    put = {
        "title": title,
        "dur": duration,
        "streamtype": stream,
        "by": user,
        "user_id": user_id,
        "chat_id": original_chat_id,
        "file": file,
        "vidid": vidid,
        "seconds": duration_in_seconds,
        "played": 0,
    }

    # Forceplay → En üste koy
    if forceplay:
        if db.get(chat_id):
            db[chat_id].insert(0, put)
        else:
            db[chat_id] = [put]
    else:
        db.setdefault(chat_id, []).append(put)

    # Otomatik temizleme listesine ekle
    autoclean.append(file)


async def put_queue_index(
    chat_id: int,
    original_chat_id: int,
    file: str,
    title: str,
    duration: str,
    user: str,
    vidid: str,
    stream: str,
    forceplay: Union[bool, str] = None,
):
    """Index / m3u8 stream için sıraya ekler."""

    # Özel URL kontrolü
    if "20.212.146.162" in vidid:
        try:
            dur = await asyncio.get_event_loop().run_in_executor(
                None, check_duration, vidid
            )
            duration = seconds_to_min(dur)
        except:
            dur = 0
            duration = "ᴜʀʟ sᴛʀᴇᴀᴍ"
    else:
        dur = 0

    put = {
        "title": title,
        "dur": duration,
        "streamtype": stream,
        "by": user,
        "chat_id": original_chat_id,
        "file": file,
        "vidid": vidid,
        "seconds": dur,
        "played": 0,
    }

    # Forceplay → En üste koy
    if forceplay:
        if db.get(chat_id):
            db[chat_id].insert(0, put)
        else:
            db[chat_id] = [put]
    else:
        db.setdefault(chat_id, []).append(put)