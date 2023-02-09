import asyncio
import aiohttp
import arrow


async def fetch_data(session, url):
    """Получаем данные"""
    async with session.get(url) as response:
        content = await response.json()
        stamp = arrow.now().timestamp()
        return stamp, float(content['price'])


async def main():
    async with aiohttp.ClientSession() as session:
        s1 = arrow.now().timestamp()
        """Добавляем данные в список, указывая необходимое нам количество запросов"""
        prices_info = []
        for _ in range(0, 10):
            api_url = 'https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT'
            prices_info.append(asyncio.ensure_future(fetch_data(session=session, url=api_url)))

        all_prices = await asyncio.gather(*prices_info)

        """Делаем проверку, чтобы количество записей в словаре было за последний час"""
        now_time = arrow.now().timestamp()
        if (now_time - all_prices[0][0]) > 3600:
            all_prices.pop(0)

        """Получаем самую высокую цену за час и актуальную цену"""
        _list = []
        for elem in all_prices:
            _list.append(elem[1])

        highest_price = max(_list)
        current_price = _list[len(_list) - 1]

        """Делаем проверку на разницу цен"""
        if current_price <= (highest_price * 0.99):
            print(f'Цена упала на 1%. Текущая цена — {current_price}, максимальная — {highest_price}')

        """Указываем в консоли время выполения каждого списка из запросов"""
        print("--- %s seconds ---" % (arrow.now().timestamp() - s1))


while True:
    asyncio.run(main())
