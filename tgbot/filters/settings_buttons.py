import typing
from dataclasses import dataclass
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


@dataclass
class ListOfButtons:
    text: typing.List
    callback: typing.List = None
    url: typing.List = None
    align: typing.List[int] = None

    @property
    def inline_keyboard(self):
        return generate_inline_keyboard(self)

    @property
    def reply_keyboard(self):
        return generate_reply_keyboard(self)


def generate_inline_keyboard(args: ListOfButtons) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    if args.text and args.callback and not (len(args.text) == len(args.callback)):
        raise IndexError("All lists must be the same length!")

    if args.url and not (len(args.text) == len(args.url)):
        raise IndexError("All lists must be the same length!")

    if not args.align:
        for num, button in enumerate(args.text):
            if args.url and args.url[num]:
                keyboard.add(InlineKeyboardButton(text=str(button),
                                                  url=args.url[num]))
            else:
                keyboard.add(InlineKeyboardButton(text=str(button),
                                                  callback_data=str(args.callback[num])))
    else:
        count = 0
        for row_size in args.align:
            buttons = []
            if args.url:
                for text, callback_data, url in tuple(zip(args.text, args.callback, args.url))[count:count + row_size]:
                    if url:
                        buttons.append(InlineKeyboardButton(text=str(text), url=url))
                    else:
                        buttons.append(InlineKeyboardButton(text=str(text), callback_data=str(callback_data)))
            else:
                for text, callback_data in tuple(zip(args.text, args.callback))[count:count + row_size]:
                    buttons.append(InlineKeyboardButton(text=str(text), callback_data=str(callback_data)))
            keyboard.row(*buttons)
            count += row_size
    return keyboard


def generate_reply_keyboard(args: ListOfButtons) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    if not args.align:
        for num, button in enumerate(args.text):
            keyboard.add(KeyboardButton(text=str(button)))
    else:
        count = 0
        for row_size in args.align:
            keyboard.row(*[KeyboardButton(text=str(text)) for text in args.text[count:count + row_size]])
            count += row_size
    return keyboard
