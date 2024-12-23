from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_forecast_duration_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("На 1 день", callback_data="forecast_1"),
        InlineKeyboardButton("На 3 дня", callback_data="forecast_3"),
        InlineKeyboardButton("На 5 дней", callback_data="forecast_5"),
    )
    return keyboard
