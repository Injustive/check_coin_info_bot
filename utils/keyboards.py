from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить', callback_data='add'),
        ],
        [
            InlineKeyboardButton(text='Информация по монете', callback_data='info'),
        ],
        [
            InlineKeyboardButton(text='Удалить', callback_data='delete')
        ]
    ]
)


def create_coins_list_kb(coins: list, opp: str):
    """Создает клавиатуру из списка монет + callback в зависимости от операции"""

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=coin.upper(), callback_data=f'{opp}_{coin}')] for coin in coins
        ]
    )

    return kb

