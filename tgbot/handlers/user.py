from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import test_keyboard
from tgbot.misc.states import Test


async def user_start(message: Message, state: FSMContext):
    # Сброс всех состояний.
    await state.reset_state(with_data=True)
    # Ответ пользователю с тестовой клавиатурой.
    await message.answer("Пример первого хендлера который начинает цикл обработки сообщений",
                         reply_markup=test_keyboard)
    await Test.first_state.set()


async def user_two(message: Message, state: FSMContext):
    # Пример удаления кнопок и окончания машиносостояния.
    reply_markup = types.ReplyKeyboardRemove()
    await message.answer(f'✅Пример кнопок\n'
                         f'И переноса текста внутри кода.', reply_markup=reply_markup)
    await state.update_data(number_auto=message.text)
    await state.finish()


async def user_photo(message: Message):
    await message.answer(f'✅Фото загружено\n'
                         f'Пример принятия фотографии')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(user_two, state=Test.first_state)
    dp.register_message_handler(user_photo, content_types=types.ContentTypes.PHOTO)
