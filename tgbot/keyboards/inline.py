from tgbot.filters.settings_buttons import ListOfButtons

test_keyboard_inl = ListOfButtons(text=['Перейти на ДО'], callback=['one_call'], align=[1],
                                  url=['https://moodle.btgp.ru/']).inline_keyboard

test_keyboard_inl_11 = ListOfButtons(text=['Перейти на ДО'], callback=['one_call'], align=[1]).inline_keyboard
