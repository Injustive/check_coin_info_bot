from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddCoin(StatesGroup):
    waiting_for_coin_name = State()


class CoinInfo(StatesGroup):
    waiting_for_coin_name = State()


class DeleteCoin(StatesGroup):
    waiting_for_coin_name = State()
