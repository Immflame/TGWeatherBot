from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ACCUWEATHER_API_KEY = os.getenv('ACCUWEATHER_API_KEY')