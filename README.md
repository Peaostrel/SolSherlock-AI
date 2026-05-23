# 🤖 Solana AI Analyst Telegram Bot

An autonomous AI-powered assistant built for the **Solana Ecosystem** that provides instant, deep on-chain financial audits and risk assessments for any Solana token. 

Built entirely with Python, leveraging real-time DEX pool data from **DexScreener API** and advanced intelligence from **Google Gemini 1.5 Flash API**.

> [!NOTE]
> Designed and submitted for the **Superteam Agentic Engineering Grants**. Zero capital required, 100% open-source!

---

## 🌟 Key Features

* 📊 **Instant On-chain Data Retrieval:** Fetch real-time price, 24h trading volume, locked liquidity, FDV, price change intervals (5m, 1h, 6h, 24h), and transaction ratios (buys vs sells) directly from DEX pools.
* 🧠 **AI-Powered Deep Risk Assessment:** Transform raw on-chain telemetry into an investment report assessing wash trading signs, market sentiment, buy/sell pressure, and liquidity ratios.
* 🛑 **Risk Score Engine:** Automatically computes a proprietary **Risk Score (0-100)** to alert traders about low liquidity, high volatility, and pump-and-dump setups.
* 💬 **Clean Interactive UI:** Premium Telegram interface with fast callback menus, markdown reporting, and real-time process feedback.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** [Aiogram v3](https://github.com/aiogram/aiogram) (Modern, fully asynchronous Telegram Bot framework)
* **HTTP Client:** [Httpx](https://github.com/encode/httpx) (Fast async requests)
* **Solana Telemetry:** DexScreener Public API
* **Intelligence:** Google Gemini 1.5 Flash (via direct high-performance HTTP endpoints)

---

## 📐 System Architecture

```
                                +------------------------+
                                |  Solana Trader (User)  |
                                +-----------+------------+
                                            |
                                      Sends Token Mint
                                            |
                                            v
                                +-----------+------------+
                                |   Telegram Bot Core    |
                                +-----------+------------+
                                            |
                         +------------------+------------------+
                         |                                     |
               Queries DEX metrics                   Sends Metrics & Prompt
                         |                                     |
                         v                                     v
             +-----------+-----------+             +-----------+-----------+
             |   DexScreener API     |             |   Google Gemini API   |
             +-----------------------+             +-----------------------+
```

---

## 🚀 Getting Started

### 1. Clone the repository
Extract the project code to your local machine:
```bash
git clone <your-repository-url>
cd solana-ai-analyst
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment variables
Create a `.env` file in the root folder of the project:
```env
TELEGRAM_BOT_TOKEN="your_telegram_bot_token_from_botfather"
GEMINI_API_KEY="your_google_gemini_api_key"
```

### 4. Run the bot
```bash
python bot.py
```

---

## 🎯 Verification & Showcase

### Try it in Telegram:
1. Start the bot with `/start`.
2. Click the quick button for popular tokens (like WIF or BONK) or paste any Solana token address (e.g. `EKpQGSJtjMFqKZ9KQGWjzD4Ww75ypm1PkxWALJmqpump`).
3. View the beautifully structured analysis!
