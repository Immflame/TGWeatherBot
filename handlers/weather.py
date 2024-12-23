from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from weather_api import WeatherAPI
from inline import create_forecast_duration_keyboard


class WeatherState(StatesGroup):
    waiting_for_start_location = State()
    waiting_for_end_location = State()
    waiting_for_intermediate_locations = State()
    waiting_for_forecast_duration = State()


async def weather_handler(message: types.Message):
    """Команда /weather"""
    await message.answer(
        "Укажите начальную точку(город или место):"
    )
    await WeatherState.waiting_for_start_location.set()


async def start_location_handler(message: types.Message, state: FSMContext):
    """Получение начальной точки"""
    await state.update_data(start_location=message.text)
    await message.answer("Теперь введите конечную точку:")
    await WeatherState.waiting_for_end_location.set()


async def end_location_handler(message: types.Message, state: FSMContext):
    """Получение конечной точки"""
    await state.update_data(end_location=message.text)
    await message.answer(
        "Хотите добавить промежуточные точки? (да/нет)\n"
        "Если нет, отправьте 'нет', и мы перейдем к выбору интервала."
    )
    await WeatherState.waiting_for_intermediate_locations.set()


async def intermediate_locations_handler(
    message: types.Message, state: FSMContext
):
    """Промежуточные точки"""
    user_data = await state.get_data()
    if message.text.lower() == "нет":
        await message.answer(
            "Выберие на сколько дней сделать прогноз:",
            reply_markup=create_forecast_duration_keyboard(),
        )
        await WeatherState.waiting_for_forecast_duration.set()
    else:
        await state.update_data(intermediate_locations=message.text.split(", "))
        await message.answer(
            "Выберите на сколько дней сделать прогноз:",
            reply_markup=create_forecast_duration_keyboard(),
        )
        await WeatherState.waiting_for_forecast_duration.set()


async def forecast_duration_handler(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """Выбор врмени прогноза"""
    duration = int(callback_query.data.split("_")[1])

    await state.update_data(forecast_duration=duration)
    user_data = await state.get_data()
    start_location = user_data["start_location"]
    end_location = user_data["end_location"]
    intermediate_locations = user_data.get("intermediate_locations", [])

    locations = [start_location, end_location]
    if intermediate_locations:
        locations.extend(intermediate_locations)

    weather_api = WeatherAPI()
    forecast_results = await weather_api.fetch_weather_for_route(
        locations=locations, days=duration
    )
    formatted_text = weather_api.format_forecast_text(forecast_results)
    await callback_query.message.answer(formatted_text, parse_mode="HTML")
    await state.finish()


def register_weather_handlers(dp: Dispatcher):
    dp.register_message_handler(weather_handler, commands=["weather"], state="*")
    dp.register_message_handler(
        start_location_handler, state=WeatherState.waiting_for_start_location
    )
    dp.register_message_handler(
        end_location_handler, state=WeatherState.waiting_for_end_location
    )
    dp.register_message_handler(
        intermediate_locations_handler,
        state=WeatherState.waiting_for_intermediate_locations,
    )
    dp.register_callback_query_handler(
        forecast_duration_handler, state=WeatherState.waiting_for_forecast_duration
    )

