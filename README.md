## Оглавление

#### **Проект работает на версии Python 3.8.x - 3.10.x. На версиях выше или ниже работоспособность не гарантируется.**

- [maintemplate](#maintemplate)
    - [systemd](#systemd)
        - [tgbot.service](#tgbot.service)
    - [tgbot](#tgbot)
        - _[filters](#filters)_
            - [admin.py](#admin.py)
            - [button_filter.py](#button_filter.py)
            - [logger.py](#logger.py)
            - [settings_button.py](#settings_button.py)
        - _[handlers](#handlers)_
            - [admin.py](#admin.py)
            - [echo.py](#echo.py)
            - [user.py](#user.py)
        - _[keyboard](#keyboard)_
            - [inline.py](#inline.py)
            - [reply.py](#reply.py)
        - _[middleware](#middleware)_
            - [db.py](#db.py)
            - [throttling.py](#throttling.py)
        - _[misc](#misc)_
            - [set_bot_commands.py](#tgbot)
            - [state.py](#state.py)
        - _[models](#models)_
            - [database.db](#database.db)
            - [users.py](#users.py)
        - _[services](#services)_
        - [config.py](#config.py)
    - [env.dist](#env.dist)
    - [gitignore](#gitignore)
    - [bot.py](#bot.py)
    - [README.md](#README.md)
    - [requirements.txt](#requirements.txt)

## maintemplate

____
Вся структура бота находится в основной папке, папку можно называть как угодно, главное чтобы она была названа на
английском языке с использованием маленьких букв.
Внутри проекта хранятся следующие необходимые для работы папки и файлы.
В каждой подпапке tgbot хранятся `__init__.py` файлы, они нужны для определения каталога, как каталога python
директории.
Проект написан без использования глобальных переменных, если они присутствуют, пожалуйста сообщите мне, спасибо.

____
[:arrow_up:Оглавление](#Оглавление)
____

## systemd

Systemd - система инициализации которая управляет службами в операционной системе Linux.
На данный момент Systemd присутствует в таких дистрибутивах как Debian, Ubuntu, Linux Mint, Manjaro и во многих других.
С помощью Systemd можно создавать свои так называемые Unit (Юнит), тем самым автоматизировав необходимый процесс.
Сам же юнит можно назвать скриптом, выполняющим определенные действия, если конечно прописать в него эти действия.
Источник и
примеры: [Ссылка](https://cyber-x.ru/%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%B5%D0%BC-systemd-%D1%8E%D0%BD%D0%B8%D1%82-unit-%D0%BD%D0%B0-%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80%D0%B5-telegram-%D0%B1%D0%BE%D1%82%D0%B0/)

____
[:arrow_up:Оглавление](#Оглавление)
____

## tgbot.service

Пример файла:

```
[Unit]
Description=Company Bot         # Описание проекта
After=network.target            # Настройки конечной цели соединения

[Service]
User=tgbot                      # Пользователь
Group=tgbot                     # Группа
Type=simple                     # Тип
WorkingDirectory=/opt/tgbot     # Рабочая директория
ExecStart=/opt/tgbot/venv/bin/python bot.py # Стартовый файл
Restart=always                  # Режим рестарта

[Install]
WantedBy=multi-user.target      # Режим использования (мульти-режим)
```

Источник: [Ссылка Habr](https://habr.com/ru/company/southbridge/blog/255845/)

____
[:arrow_up:Оглавление](#Оглавление)
____

## tgbot

Основная папка содержащая в себе большую часть настроек для работы с ботом.
В ней хранятся подпапки для лучшего понимания функций и задач каждого файла.

____
[:arrow_up:Оглавление](#Оглавление)
____

## filters

Папка фильтры содержит в себе фильтрацию информации по заданным пользователем алгоритмам.
В данной папке прописаны фильтры для:

1. Отлавливания сообщений только для админа;
2. Отлавливания нажатий на кнопки;
3. Логгирование для дебага кода и удобства вывода ошибок;
4. Настройка кнопок для удобного прописывания клавиатуры внутри бота.

____
[:arrow_up:Оглавление](#Оглавление)
____

## admin.py

```
import typing
from aiogram.dispatcher.filters import BoundFilter
from tgbot.config import Config

class AdminFilter(BoundFilter):             # Админ класс наследованный от BoundFilter
    key = 'is_admin'                        # Ключ по которому будем определять админа

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin            # В данном случае is_admin является bool значением (True or False)

    async def check(self, obj):             # Проверка пользователя на админа
        if self.is_admin is None:
            return False                    # Если айди не совпал, возвращаем False
        config: Config = obj.bot.get('config')     # Берём из конфигурации айди админа
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin  # Если он совпадает возвращается True
```

____
[:arrow_up:Оглавление](#Оглавление)
____

## button_filter.py

Данный фильтр используется для прописывания в register_inline_handler() нажатия на кнопку.
Выглядит это следующим образом, есть inline кнопка с `callback - test_inl`, нажатие на неё нужно отследить,
код будет выглядеть так:

```
register_inline(dp: Dispatcher):
    dp.register_inline_handler(Button('test_inl')
```

____
[:arrow_up:Оглавление](#Оглавление)
____

## logger.py

Логгирование прописано с использованием библиотеки `loguru` и встроенной python библиотеки `logging`.
Оно запускается в главном файле bot.py с помощью функции `await setup_logger()`.
Библиотека loguru облегчает отлов ошибок и просмотр информации о работе кода.


____
[:arrow_up:Оглавление](#Оглавление)
____

## settings_button.py

Настройка клавиатуры нужна для простого создания больших клавиатур, за место старого способа прописывания клавиатуры,
будет лучше использовать `class ListOfButtons`, который имеет параметры `text` - текст кнопки,
`callback` - для инлайн кнопок способ отловить нажатие и `align` - количество кнопок в строке.

____
[:arrow_up:Оглавление](#Оглавление)
____

## handlers

Папка содержащая основные функции для отлова сообщений. При отправке сообщения бот получает информацию от пользователя
и чтобы решить что с ней делать, нужно сообщение обработать, а за это как раз отвечает handler (обработчик).
В данной папке необходимо хранить только обработчики сообщений, будь то текстовые сообщения или нажатие на кнопки.

____
[:arrow_up:Оглавление](#Оглавление)
____

## admin.py

```
from aiogram import Dispatcher
from aiogram.types import Message

async def admin_start(message: Message):        # Если фильтрация на админа прошла успешно
    await message.reply("Hello, admin!")        # Бот отправит сообщение только админу

# Регистрация хендлеров передаётся в главный стартовый файл bot.py
def register_admin(dp: Dispatcher):             # В если админ=True, тогда сообщение попадёт по адрессу
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
```

____
[:arrow_up:Оглавление](#Оглавление)
____

## echo.py

Эхо хендлер принимает сообщения любого типа и отвечает на них заданным пользователем алгоритмом, только в случае если
данное сообщение не попало в другие хендлеры и не прошло особую фильтрацию. Для корректной работы эхо хендлера,
в основном файле bot.py функцию регистрации эхо хендлера нужно прописать ниже основных функций хендлеров.

____
[:arrow_up:Оглавление](#Оглавление)
____

## user.py

Данный файл прописан для примерного понимания прописывания функций и их регистрации в hendler'ах.
Файл содержит примеры:

1. Сброс машино-состояния `await state.reset_state(with_data=True)`;
2. Отправки простого текстового сообщения, на сообщение пользователя по команде - `/start` с клавиатурой;
3. Фиксирования пользователя в состоянии ответа на второе сообщение, то есть следующее сообщение 100% попадает
   в следующий заданный хендлер;
4. Следующий хендлер отвечает на второе сообщение пользователя, фиксация состояния пользователя прописывается в
   строчке регистрации `dp.register_message_handler(user_two, state=Test.first_state)`;
5. Далее прописан метод удаления клавиатуры для пользователя;
6. Строчкой ниже отправка ответа с удалённой клавиатурой, за удаление отвечает фрагмент `reply_markup=reply_markup`;
7. `await state.finish()` выводит пользователя из машино-состояния;
8. Последний хендлер принимает сообщение содержащее изображения, это регулируется типом сообщения которое ждёт функция,
   в регистрации хендлера прописывается тип - `content_types=types.ContentTypes.PHOTO`.

Финальный вид регистрации выглядит так:

```
def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(user_two, state=Test.first_state)
    dp.register_message_handler(user_photo, content_types=types.ContentTypes.PHOTO)
```

____
[:arrow_up:Оглавление](#Оглавление)
____

## keyboard

Папка keyboard содержит в себе два вида клавиатуры, которые поддерживает телеграм. Это inline клавиатура, которая
находится в тексте и имеет особые параметры нажатия. И обычная текстовая клавиатура reply.

## inline.py и reply.py

Файл содержит в себе одну кнопку, разработанную для примера. Кнопка содержит в себе параметры унаследованные от
фильтра - settings_button.py. Для начала необходимо добавить класс с нужными параметрами кнопки, в котором содержатся
параметры:

1. text - Текст, который будет отображаться в кнопке.
2. callback - Обязательно должен быть такого же размера, как и text. Отвечает за нажатие на кнопку, если это
   inline клавиатура, но в reply так же должно быть одинаковое количество. Callback'и задаются по принципу: Как кнопка
   названа, так и называем callback прибавляя в конце "callback" - `text="Привет", callback="hello_call"`.
3. И align это количество кнопок в строке, нужно разбивать логически, если кнопок к примеру 10,
   то в первый рад можно разместить 4 кнопки, во второй ряд тоже 4 и в последний 2. Или если у нас 6 кнопок,
   align будет равен `[3, 3]`, то есть будет два ряда по 3 кнопки.

____
[:arrow_up:Оглавление](#Оглавление)
____

## middleware

Middleware - это папка содержащая в себе модули, которые отвечают за пре-обработку входящих запросов от пользователей.
Может содержать файлы связанные с базой данных, если они отвечают за первоначальную обработку пользователя.
Смысл middleware в том, что когда пользователь присылает сообщение боту, мы с помощью первоначальной обработки,
можем определять id пользователя и прочие параметры, после чего решать как ответить пользователю или что ответить.

## db.py

Файл был создан на случай использования базы данных. В данном случае информационной нагрузки не несёт.

## throttling.py

Тротлинг отвечает за обработку количества входящих сообщений, чтобы бот не реагировал на спам или пользователю
выдавалось временное ограничение на отправку сообщений. Сделан для фильтрации спама, проще говоря это система
анти-спам.

____
[:arrow_up:Оглавление](#Оглавление)
____

## misc

Папка miscellaneous, содержит в себе различные файлы и модули, которые не подходят для других подпапок.

## set_bot_commands.py

В данном файле содержатся параметры, для создания кнопок-команд в телеграм боте. Это команды по типу - `/start`
или `/help`. С помощью `types.BotCommand` внутри aiogram'а, можно задать команду и описание для пользователя,
что эта команда значит - `types.BotCommand("start", "⚡️Запустить бота")`.

## state.py

Внутри файла прописываются:

1. Класс стадии, например: Опрос, он содержит в себе 3 вопроса. По этому мы создаём данный класс, наследуя у
   `StatesGroup`.
2. И вопросы. Пример: `first_state = State()`. Стадий внутри одного класса может быть столько, сколько необходимо
   для задачи.

____
[:arrow_up:Оглавление](#Оглавление)
____

## models

Папка моделей отвечает различные модели баз данных, например в данной папке есть модель пользователей.
Для примера была задействована лёгкая база данных SQLite3. Все запросы в примере выполнены
под данную архитектуру.

## database.db

Непосредственно файл содержащий данные о пользователях. Сама база данных.

## users.py

В файле пользователей, прописано подключение к базе данных - `con = sqlite3.connect(file_path)` и добавление столбиков
с данными о пользователях.

____
[:arrow_up:Оглавление](#Оглавление)
____

## services

Папка может содержать в себе различные сторонние сервисы, к примеру `Dockerfile` или другие файлы Docker'а.

____
[:arrow_up:Оглавление](#Оглавление)
____

## config.py

Файл конфигурации создан для считывания данных по типу - `BOT_TOKEN`, для работы с ботом из скрытого файла `.env`.
Данный файл скрыт и для него создан файл конфигурации из соображений конфиденциальности. Потому, что токен
подключения к боту или пароли от базы данных, в случае неверного хранения их в разработанном проекте
могут попасть в руки мошенников, чего допускать категорически нельзя. Для этого создан отдельный файл, который
не загружается на github или подобный облачный сервис и расшифровывается отдельным конфигом.
Для работы с `.env` файлом подгружается модуль `environs`. Конфиг имеет несколько стадий:

1. Создание `@dataclass`, в котором хранятся данные для разных задач, будь то подключение к боту и его данные,
   заканчивая данными подключения к базе данных. Создаётся класс названый так, чтобы понимать для какого сервиса
   он создан. Пример: `class TgBot:`, содержит в себе строку с данными и их типом - `token: str`.
2. Далее создаётся функция - `load_config()`, для инициализации файла и распределения переменных со значениями.
3. После чего идёт возврат данных в расшифрованном виде с помощью главного класса `Config`, в котором хранятся
   классы различных созданных нами сервисов.

____
[:arrow_up:Оглавление](#Оглавление)
____

## env.dist

Для корректной работы данного файла, необходимо для начала убрать расширение `.dist`, вид файла должен быть
только `.env`.
Внутри файла содержатся различные конфиденциальные данные, такие как подключение к
боту - `BOT_TOKEN`, или адрес базы данных - `DB_HOST`.
Если в файле что-то добавляется, эти данные необходимо обработать через файл `config.py`. Добавив классы сервиса
для которого добавились данные и его параметры, это пароли, логины и т.д.
____
[:arrow_up:Оглавление](#Оглавление)
____

## gitignore

Файл предназначен для игнорирования указанных пользователем файлов и папок, для того чтобы они не попали на github
или подобный облачный ресурс. Он же отвечает за то, чтобы файл `.env` не попал вместе с проектом в облачный ресурс.

____
[:arrow_up:Оглавление](#Оглавление)
____

## bot.py

Самый объёмный файл, содержащий настройки и обработки всех действий бота. С его помощью происходит объединение всех
файлов и функций, в один единый файл, который в итоге необходимо запускать для того, чтобы бот корректно работал.
В нём происходит импорт и регистрирование необходимых модулей:

```
def register_all_middlewares(dp):
    dp.setup_middleware(ThrottlingMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)

    register_echo(dp)
```

Порядок регистрации нарушать нельзя. Или смысл модулей пропадёт. Регистрация хендлеров для корректной работы
должна быть выполнена выше чем `register_echo(dp)`. В противном случае echo будет перехватывать все сообщения
пользователя.

Далее создаётся основная функция `main()`, которая будет содержать все настройки, хендлеры и т.д.
Строчка `asyncio.run(main())`, запускает в цикле данную функцию и бот работает постоянно, обрабатывая входящие запросы.

____
[:arrow_up:Оглавление](#Оглавление)
____

## README.md

Данный файл служит описанием всего проекта. В нём содержатся описания файлов и папок, общей структуры проекта.
____
[:arrow_up:Оглавление](#Оглавление)
____

## requirements.txt

В этом файле собраны все необходимые для функционирования проекта модули и их версии для корректной работы.
Для его установки нужно прописать в консоль, в уже развёрнутом виртуальном окружении проекта
`pip install requirements.txt`. Если всё выполнено правильно, проект будет работать корректно.

____
[:arrow_up:Оглавление](#Оглавление)
____

## Заключение

Данное руководство полностью описывает проект и его функционал. В случае если что-то не понятно или не раскрыто, просьба
написать на почту sonetrue1@gmail.com с подробным объяснением непонятного вам момента. В дальнейшем планируется
улучшение
проекта и расширение его функционала.

## Спасибо!