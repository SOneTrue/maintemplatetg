from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def bot_echo(message: types.Message, state: FSMContext):
    text = [
        f'⛔️ Хендлер отвечающий на любое сообщение\n'
        f'Если сообщение не было отфильтрованною другим хендлером.'
    ]

    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    text = [
        f'⛔️ Хендлер отвечающий на любое сообщение\n'
        f'Если сообщение не было отфильтрованною другим хендлером.'
    ]
    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    # Тип данных принимаемый хендлером любой!
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
