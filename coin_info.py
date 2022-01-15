from connect_to_coinmarketcap import connect_to_cmc
import asyncio
from utils.emojis import *

class Coin():
    """Отображение статистики по монете"""

    def __init__(self, coin):
        self.coin = coin

    async def get_coin_stat(self) -> dict:
        """Запрос к cmc. Возвращает статистику"""

        self.coin_stat = await connect_to_cmc(self.coin.lower())
        return self.coin_stat

    async def coin_stat_message(self) -> str:
        """Возвращает статистику монеты для бота"""

        def emoji_chart(value):  # Функция изменения emoji в зависимости от параметра
            return EMOJI_INCREASE if value > 0 else EMOJI_DECREASE

        coin_stat = await self.get_coin_stat()
        c_path = coin_stat['data'][self.coin.upper()]['quote']['USD']

        price = c_path['price']
        volume_24h = c_path['volume_24h']
        change_1h = c_path['percent_change_1h']
        change_24h = c_path['percent_change_24h']
        change_7d = c_path['percent_change_7d']

        full_info = f"""
        *{EMOJI_FIRE}Цена монеты {self.coin}: {price}${EMOJI_FIRE}
        {emoji_chart(volume_24h)}Обьем за 24 часа: {int(volume_24h)}${emoji_chart(volume_24h)}
        {emoji_chart(change_1h)}Изменение за 1 час: {change_1h:.4f}%{emoji_chart(change_1h)}
        {emoji_chart(change_24h)}Изменение за 24 часа: {change_24h:.4f}%{emoji_chart(change_24h)}
        {emoji_chart(change_7d)}Изменение за 7 дней: {change_7d:.4f}%{emoji_chart(change_7d)}*
        """.replace("    ", "")

        return full_info

