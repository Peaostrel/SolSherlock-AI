import httpx
from typing import Dict, Optional

class SolanaClient:
    def __init__(self):
        self.dexscreener_url = "https://api.dexscreener.com/latest/dex/tokens"

    async def get_token_data(self, token_address: str) -> Optional[Dict]:
        """
        Получает детальные ончейн-данные о токене по его адресу в сети Solana.
        Использует бесплатный DexScreener API.
        """
        url = f"{self.dexscreener_url}/{token_address}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                if response.status_code != 200:
                    print(f"[ERROR] DexScreener returned status {response.status_code}")
                    return None
                
                data = response.json()
                pairs = data.get("pairs", [])
                if not pairs:
                    return None
                
                # Фильтруем пары, берем наиболее ликвидную пару на Solana (обычно Raydium или Orca)
                solana_pairs = [p for p in pairs if p.get("chainId") == "solana"]
                if not solana_pairs:
                    # Если нет пар на Solana, берем первую доступную
                    pair = pairs[0]
                else:
                    # Сортируем по ликвидности и берем максимальную
                    pair = max(solana_pairs, key=lambda x: float(x.get("liquidity", {}).get("usd", 0) or 0))
                
                # Формируем чистый структурированный ответ
                info = pair.get("info", {})
                return {
                    "name": pair.get("baseToken", {}).get("name", "Unknown"),
                    "symbol": pair.get("baseToken", {}).get("symbol", "Unknown"),
                    "address": token_address,
                    "price_usd": pair.get("priceUsd", "0.0"),
                    "price_native": pair.get("priceNative", "0.0"),
                    "quote_symbol": pair.get("quoteToken", {}).get("symbol", "USDC"),
                    "dex": pair.get("dexId", "Unknown"),
                    "volume_24h": pair.get("volume", {}).get("h24", 0),
                    "liquidity_usd": pair.get("liquidity", {}).get("usd", 0),
                    "fdv": pair.get("fdv", 0),
                    "price_change": {
                        "m5": pair.get("priceChange", {}).get("m5", 0),
                        "h1": pair.get("priceChange", {}).get("h1", 0),
                        "h6": pair.get("priceChange", {}).get("h6", 0),
                        "h24": pair.get("priceChange", {}).get("h24", 0),
                    },
                    "transactions_24h": {
                        "buys": pair.get("txns", {}).get("h24", {}).get("buys", 0),
                        "sells": pair.get("txns", {}).get("h24", {}).get("sells", 0),
                    },
                    "links": info.get("websites", []) + info.get("socials", [])
                }
            except Exception as e:
                print(f"[ERROR] Exception during DexScreener API call: {e}")
                return None
