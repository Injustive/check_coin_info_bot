from utils.emojis import *
from utils.keyboards import *
from errors import *
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from loader import dp
from fsm import *
from manage_db import add_coin_to_db, check_coins, delete_coin_from_db
from coin_info import Coin

@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""

    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()

    msg = f"Привет!{EMOJI_HELLO} Я бот для просмотра информации по Coinmarketcap монетам." \
          "\nВыбери операцию ниже, чтобы начать"

    await message.answer(
        f'{msg} {EMOJI_DOWN_ARROW*3}',
        reply_markup=main_keyboard
    )


@dp.callback_query_handler(text="add", state='*')
async def add_coin(call: types.CallbackQuery):
    """Приглашание к вводу монеты + проверка на макс количество"""

    state = dp.current_state(user=call.from_user.id)
    await state.reset_state()

    await call.answer()
    await call.message.answer(f'Введите название монеты. Пример(BTC, ETH, DOT, TWT):{EMOJI_DOWN_ARROW*3}')
    await AddCoin.waiting_for_coin_name.set()


@dp.message_handler(state=AddCoin.waiting_for_coin_name, content_types=types.ContentTypes.TEXT)
async def coin_name_set(message: types.Message, state: FSMContext):
    """Добавление монеты в БД по названию, если она есть на CoinMarketCap"""

    coin_info = Coin(message.text.upper())

    try:
        await coin_info.get_coin_stat()
        response = await add_coin_to_db(message.from_user.id, message.text.lower())
        await message.answer(response, reply_markup=main_keyboard)
        await state.finish()
    except GetDataFailError:
        await message.answer(f"Этой монеты нет на CoinMarketCap, введите другую монету{EMOJI_CROSS_MARK}",
                             parse_mode='Markdown')


@dp.callback_query_handler(text="info", state='*')
async def info_my_coin(call: types.CallbackQuery):
    """Выбор монеты из списка монет пользователя"""

    await call.answer()

    state = dp.current_state(user=call.from_user.id)
    await state.reset_state()

    try:
        coins = await check_coins(call.from_user.id)
    except NoCoinsDataError:
        return await call.message.answer(f"У вас нет монет. Сначала добавьте монеты{EMOJI_CROSS_MARK}",
                                  reply_markup=main_keyboard)

    await call.message.answer(f'Выберите монету из списка ниже{EMOJI_DOWN_ARROW*3}:',
                              reply_markup=create_coins_list_kb(coins, 'check_info'))
    await CoinInfo.waiting_for_coin_name.set()


@dp.callback_query_handler(text="delete", state='*')
async def delete_coin(call: types.CallbackQuery):
    """Выбор монеты для удаления"""

    await call.answer()

    state = dp.current_state(user=call.from_user.id)
    await state.reset_state()

    try:
        coins = await check_coins(call.from_user.id)
    except NoCoinsDataError:
        return await call.message.answer(f"У вас нет монет. Сначала добавьте монеты{EMOJI_CROSS_MARK}",
                                  reply_markup=main_keyboard)

    await call.message.answer(f'Выберите монету из списка ниже, чтобы удалить{EMOJI_DOWN_ARROW * 3}:',
                              reply_markup=create_coins_list_kb(coins, 'delete_coin'))
    await DeleteCoin.waiting_for_coin_name.set()


@dp.callback_query_handler(state=DeleteCoin.waiting_for_coin_name)
async def get_coin_info(call: types.CallbackQuery, state: FSMContext):
    """Удаление монеты"""

    await call.answer()
    msg_coin = call.data.replace('delete_coin_', '')

    try:
        await check_coins(call.from_user.id)
        response = await delete_coin_from_db(call.from_user.id, msg_coin.lower())
        await call.message.answer(response, reply_markup=main_keyboard)
    except NoCoinsDataError:
        await call.message.answer(f"У вас уже нет этой монеты!{EMOJI_CROSS_MARK}", reply_markup=main_keyboard)
    await state.finish()


@dp.callback_query_handler(state=CoinInfo.waiting_for_coin_name)
async def get_coin_info(call: types.CallbackQuery):
    """Возвращение статистики монеты"""

    await call.answer()
    msg_coin = call.data.replace('check_info_', '')
    coin = Coin(msg_coin.upper())

    try:
        coins = await check_coins(call.from_user.id)
        response = await coin.coin_stat_message()
        await call.message.answer(response, reply_markup=create_coins_list_kb(coins, 'check_info'),
                                  parse_mode="Markdown")
    except GetDataFailError:
        await call.message.answer(f'Возникли проблемы с получением данных для этой монеты...{EMOJI_CROSS_MARK}',
                                  reply_markup=main_keyboard)
    except NoCoinsDataError:
        await call.message.answer(f"У вас уже нет этой монеты!{EMOJI_CROSS_MARK}", reply_markup=main_keyboard)


@dp.inline_handler()
async def inline_coin_info(inline_query: InlineQuery):
    """Инлайн режим для бота"""

    query = inline_query.query
    results = []

    try:
        coins = [coin for coin in await check_coins(inline_query.from_user.id) if query.lower() in coin]
        results = [InlineQueryResultArticle(
            id=coin,
            title=coin.upper(),
            input_message_content=InputTextMessageContent(
                await Coin(coin.upper()).coin_stat_message(),
                parse_mode="Markdown")
        )
            for coin in coins]

        switch_message = f"Перейти к боту {EMOJI_RIGHT_ARROW}"

        if not coins:
            switch_message = f"Не найдено. Добавить {EMOJI_RIGHT_ARROW}"
    except NoCoinsDataError:
        switch_message = f'У вас нет монет. Добавить {EMOJI_RIGHT_ARROW}'

    await inline_query.answer(
        results=results,
        cache_time=120,
        is_personal=True,
        switch_pm_text=switch_message,
        switch_pm_parameter='to_bot'
    )
