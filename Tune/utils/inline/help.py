from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Tune import app


def help_keyboard(_):
    buttons = []

    # 🔹 İlk 4 başlık (2'şer buton yan yana)
    for i in range(1, 5):
        if (i - 1) % 2 == 0:
            buttons.append([])
        buttons[-1].append(
            InlineKeyboardButton(
                text=_[f"H_B_{i}"],
                callback_data=f"help_callback hb{i}"
            )
        )

    # 🔹 Son 3 başlık (3'ü aynı satırda)
    buttons.append(
        [
            InlineKeyboardButton(
                text=_[f"H_B_5"],
                callback_data="help_callback hb5"
            ),
            InlineKeyboardButton(
                text=_[f"H_B_6"],
                callback_data="help_callback hb6"
            ),
            InlineKeyboardButton(
                text=_[f"H_B_7"],
                callback_data="help_callback hb7"
            ),
        ]
    )

    # 🔹 En alt satırda Menü ve Kapat
    buttons.append(
        [
            InlineKeyboardButton(
                text="🌊 Menü",
                callback_data="back_to_main"
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close"
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="open_help"
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close"
                ),
            ]
        ]
    )


def private_help_panel(_):
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?start=help"
            )
        ]
    ]