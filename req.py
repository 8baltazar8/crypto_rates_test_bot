import aiohttp
import json
import schemas
import pydantic

async def get_crypto_rates(cur_list=['bitcoin', 'ethereum', 'binancecoin']):
    params = {'ids': ','.join(cur_list),
              'vs_currencies': 'usd'}

    async with aiohttp.ClientSession() as session:
        # URL for CoinGecko API to fetch data for Bitcoin, Ethereum, and Binance Coin

        url = 'https://api.coingecko.com/api/v3/simple/price'

        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data# pydantic.TypeAdapter(schemas.CryptoData).validate_python(**data) # json.dumps(data, indent=4, ensure_ascii=False)
            else:
                print("Failed to retrieve data")
                return {}
