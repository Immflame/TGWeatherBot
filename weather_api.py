import aiohttp
from config import ACCUWEATHER_API_KEY


class WeatherAPI:
    def __init__(self):
        self.api_key = ACCUWEATHER_API_KEY
        self.base_url = "http://dataservice.accuweather.com"

    async def get_location_key(self, location: str) -> str | None:
        """Получить ключ местоположения по имени города."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/locations/v1/search"
            params = {
                "apikey": self.api_key,
                "q": location,
            }
            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if data:
                        return data[0]["Key"]
                    else:
                        return None
            except aiohttp.ClientError as e:
                print(f"Ошибка получения ключа места: {e}")
                return None

    async def get_forecast(self, location_key: str, days: int = 1) -> dict | None:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/forecasts/v1/daily/{days}day/{location_key}"
            params = {
                "apikey": self.api_key,
                "language": "ru-ru",
                "metric": "true",
            }

            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data
            except aiohttp.ClientError as e:
                print(f"Ошибка получения прогноза: {e}")
                return None

    async def fetch_weather_for_route(self, locations: list[str], days: int):
        """Ппрогноз погоды для списка мест"""
        results = {}
        for location in locations:
            location_key = await self.get_location_key(location)
            if location_key:
                forecast = await self.get_forecast(location_key, days)
                if forecast:
                    results[location] = forecast
                else:
                     results[location] = "Не удалось получить прогноз для этого места"
            else:
                results[location] = "Не удалось определить место"

        return results

    def format_forecast_text(self, forecasts: dict):
        formatted_text = ""
        for location, forecast_data in forecasts.items():
            formatted_text += f"Погода для {location}:\n\n"
            if isinstance(forecast_data, str):
                formatted_text += f"    {forecast_data}\n\n"
                continue
            for daily_forecast in forecast_data["DailyForecasts"]:
                formatted_text += (
                    f"    Дата: {daily_forecast['Date'][:10]}\n"
                    f"    День:\n"
                    f"        Температура: {daily_forecast['Temperature']['Maximum']['Value']}°C (макс), {daily_forecast['Temperature']['Minimum']['Value']}°C (мин)\n"
                    f"        Осадки: {daily_forecast['Day']['HasPrecipitation']}\n"
                    f"    Ночь:\n"
                    f"        Осадки: {daily_forecast['Night']['HasPrecipitation']}\n\n"
                )

        return formatted_text
