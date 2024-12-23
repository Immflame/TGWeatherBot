from aiogram import types
from aiogram.dispatcher import Dispatcher


async def start_handler(message: types.Message):
    """Команда /start"""
    await message.answer(
        "Я бот для прогноза погоды\n"
        "Помощь: /help"
    )


async def help_handler(message: types.Message):
    """Команда /help"""
    await message.answer(
        "Я могу дать прогноз погоды для вашего маршрута\n"
        "Запросить прогноз: /weather\n"
    )


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(help_handler, commands=["help"])

