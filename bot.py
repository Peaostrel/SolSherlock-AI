import asyncio
import logging
import re
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TELEGRAM_BOT_TOKEN
from solana_client import SolanaClient
from ai_analyst import AIAnalyst

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)

# Инициализируем бота и диспетчер
bot = Bot(token=TELEGRAM_BOT_TOKEN, default_properties=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

solana_client = SolanaClient()
ai_analyst = AIAnalyst()

# Регулярное выражение для проверки адреса Solana
SOLANA_ADDRESS_REGEX = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

@dp.message(CommandStart())
async def start_handler(message: Message):
    """
    Обработчик команды /start.
    """
    welcome_text = (
        "🤖 **Привет! Я ИИ-Аналитик сети Solana.**\n\n"
        "Я могу провести мгновенный ончейн-аудит и глубокий финансовый анализ любого токена в сети Solana.\n\n"
        "📈 **Что я анализирую:**\n"
        "• Динамику цены и объемы торгов\n"
        "• Глубину ликвидности и капитализацию\n"
        "• Активность крупных игроков и ботов\n"
        "• Скрытые риски и вероятность скама\n\n"
        "📥 **Отправь мне адрес контракта (mint address) любого токена Solana**, и я начну анализ!"
    )
    
    # Кнопки быстрого старта с популярными токенами
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🐶 DOGWIFHAT (WIF)", callback_data="analyze_EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"),
        ],
        [
            InlineKeyboardButton(text="🔥 BONK", callback_data="analyze_DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"),
        ]
    ])
    
    await message.answer(welcome_text, reply_markup=keyboard)

@dp.message(Command("help"))
async def help_handler(message: Message):
    """
    Обработчик команды /help.
    """
    help_text = (
        "📖 **Инструкция по использованию:**\n\n"
        "1. Скопируй адрес контракта (mint address) токена в Solana.\n"
        "   _Пример: EKpQGSJtjMFqKZ9KQGWjzD4Ww75ypm1PkxWALJmqpump (WIF)_\n"
        "2. Просто отправь этот адрес мне в чат.\n"
        "3. Дождись завершения анализа (обычно это занимает около 5-10 секунд).\n\n"
        "💡 Я использую в реальном времени ончейн-данные с **DexScreener API** и аналитику на базе **Gemini 1.5 Flash**."
    )
    await message.answer(help_text)

@dp.callback_query(F.data.startswith("analyze_"))
async def callback_analyze(callback_query):
    """
    Обработчик быстрого клика по кнопкам популярных токенов.
    """
    token_address = callback_query.data.split("_")[1]
    await callback_query.answer("Запускаю анализ...")
    await handle_token_analysis(callback_query.message, token_address)

@dp.message()
async def message_handler(message: Message):
    """
    Основной обработчик текстовых сообщений. Проверяет адрес и запускает аудит.
    """
    text = message.text.strip() if message.text else ""
    
    if not SOLANA_ADDRESS_REGEX.match(text):
        await message.answer(
            "⚠️ **Некорректный адрес Solana.**\n\n"
            "Пожалуйста, убедись, что ты отправил правильный адрес смарт-контракта (32-44 символа, base58).\n"
            "Например: `EKpQGSJtjMFqKZ9KQGWjzD4Ww75ypm1PkxWALJmqpump`"
        )
        return

    await handle_token_analysis(message, text)

async def handle_token_analysis(message: Message, token_address: str):
    """
    Общая функция проведения анализа токена.
    """
    status_message = await message.answer("⏳ **Получаю ончейн-данные с Solana DEX пулов...**")
    
    try:
        # 1. Получаем данные с Solana API
        token_data = await solana_client.get_token_data(token_address)
        if not token_data:
            await status_message.edit_text(
                "❌ **Токен не найден.**\n\n"
                "Не удалось найти активные торговые пары для этого адреса на биржах Solana (Raydium, Orca и др.).\n"
                "Убедись, что токен уже торгуется и адрес указан верно."
            )
            return
        
        # 2. Обновляем статус
        await status_message.edit_text(f"🧠 **Токен {token_data['name']} ({token_data['symbol']}) найден! Анализирую ИИ-моделью...**")
        
        # 3. Отправляем в ИИ для анализа
        report = await ai_analyst.analyze_token(token_data)
        
        # 4. Удаляем временный статус и выводим отчет
        await status_message.delete()
        
        # Если отчет слишком большой для одного сообщения Telegram (лимит 4096), делим его
        if len(report) > 4000:
            parts = [report[i:i+4000] for i in range(0, len(report), 4000)]
            for part in parts:
                await message.answer(part)
        else:
            await message.answer(report)
            
    except Exception as e:
        logger.error(f"Error during token analysis: {e}")
        await status_message.edit_text(f"⚠️ **Произошла ошибка при анализе:** {str(e)}")

async def main():
    logger.info("Starting Solana AI Analyst Bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is missing! Exiting...")
        sys.exit(1)
    asyncio.run(main())
