import httpx
from typing import Dict
from config import GEMINI_API_KEY

class AIAnalyst:
    def __init__(self):
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    async def analyze_token(self, token_data: Dict) -> str:
        """
        Отправляет собранные ончейн-данные о токене в Gemini ИИ и получает развернутый аналитический отчет.
        """
        if not GEMINI_API_KEY:
            return "⚠️ **Ошибка:** Ключ `GEMINI_API_KEY` не задан в конфигурации. ИИ-анализ недоступен."

        # Формируем читабельное представление ончейн-метрик для ИИ
        metrics_str = f"""
Токен: {token_data['name']} ({token_data['symbol']})
Адрес смарт-контракта: `{token_data['address']}`
Биржа / DEX: {token_data['dex'].upper()}
Текущая цена (USD): ${token_data['price_usd']}
Капитализация (FDV): ${token_data['fdv']:,}
Ликвидность в пуле: ${token_data['liquidity_usd']:,}
Объем торгов за 24 часа: ${token_data['volume_24h']:,}

Изменение цены:
- за 5 минут: {token_data['price_change']['m5']}%
- за 1 час: {token_data['price_change']['h1']}%
- за 6 часов: {token_data['price_change']['h6']}%
- за 24 часа: {token_data['price_change']['h24']}%

Статистика торгов за 24 часа:
- Покупок: {token_data['transactions_24h']['buys']:,}
- Продаж: {token_data['transactions_24h']['sells']:,}
"""

        prompt = f"""
Ты — профессиональный финансовый аналитик, специализирующийся на мемкоинах и DeFi-токенах в сети Solana. 
Твоя задача — сделать честный, структурированный и глубокий технический аудит токена на основе предоставленных ончейн-метрик.

Вот метрики токена:
{metrics_str}

Пожалуйста, составь аналитический отчет по следующим разделам (используй Markdown и Emojis):
1. 📊 **Общий обзор и динамика цены**: Проанализируй движение цены за 24 часа и локальные тренды (5м, 1ч, 6ч).
2. 🌊 **Анализ ликвидности и объемов**:
   - Оцени соотношение ликвидности к капитализации (FDV). Достаточно ли ликвидности для безопасных торгов?
   - Оцени соотношение 24h объема к ликвидности (высокий ли оборот?).
3. ⚖️ **Активность покупателей и продавцов**: Проанализируй количество покупок и продаж. Кто доминирует? Есть ли признаки искусственной накрутки (wash trading) или массового дампа?
4. 🛑 **Оценка рисков и вердикт**:
   - Выяви главные красные флаги (например, слишком низкая ликвидность, аномальные скачки цены, дисбаланс продаж).
   - Выстави токену **Risk Score** от 0 до 100 (где 0 — абсолютно безопасно, 100 — максимальный риск скама/дампа). Объясни оценку.
   - Дай краткий, емкий финальный совет инвестору.

Пиши на русском языке, в уверенном, экспертном, но доступном стиле. Делай акцент на безопасность капитала.
"""

        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        url = f"{self.api_url}?key={GEMINI_API_KEY}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30.0)
                if response.status_code != 200:
                    return f"⚠️ **Ошибка ИИ-генерации:** Сервер вернул код {response.status_code}. Проверь валидность API ключа."
                
                res_data = response.json()
                # Извлекаем сгенерированный текст из структуры ответа Gemini
                candidates = res_data.get("candidates", [])
                if candidates:
                    content = candidates[0].get("content", {})
                    parts = content.get("parts", [])
                    if parts:
                        return parts[0].get("text", "Не удалось прочитать ответ ИИ.")
                
                return "⚠️ **Ошибка ИИ:** Пустой ответ от модели."
            except Exception as e:
                return f"⚠️ **Ошибка при запросе к ИИ-модели:** {e}"
