import aiohttp
import json
import os
from errors import GetDataFailError
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


async def connect_to_cmc(coin: str) -> dict:
    """Подключение к CoinMarketCap"""

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=' + coin
    session_options = {
            "headers": {
              'Accepts': 'application/json',
              'X-CMC_PRO_API_KEY': os.environ.get("COINMARKETCAP_API_KEY", "")
            },
        }

    async with aiohttp.ClientSession(**session_options) as session:
        async with session.get(url) as response:
            status = response.status
            if not status == 200:
                raise GetDataFailError

            html = await response.text()
            data = json.loads(html)
            return data
