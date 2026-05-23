import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Базовые проверки на запуск
if not TELEGRAM_BOT_TOKEN:
    print("[WARNING] TELEGRAM_BOT_TOKEN is not set in environment or .env file!")
if not GEMINI_API_KEY:
    print("[WARNING] GEMINI_API_KEY is not set in environment or .env file! AI features won't work.")
