from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    # Задаём класс стейта и потом его стадии.
    first_state = State()