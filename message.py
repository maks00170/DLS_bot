from aiogram import types


def start_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="Перенести стиль", callback_data="button_style")
        
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def style_images():
    buttons = [
        types.InlineKeyboardButton(text="Главное меню", callback_data="menu")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def algo_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="Перенести стиль", callback_data="button_style"),
        types.InlineKeyboardButton(text="Главное меню", callback_data="menu")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


start_message = ("Привет! \n"
                 "Я Бот-стилизатор DLS.\n\n"
                 "Ты можешь отправить мне 2 фотографии: с первой фотографии я заберу стиль и "
                 "перенесу его на вторую фотографию.\n"
                )

menu_message = ("Напомню, что я умею делать:\n\n"
                "Я умею переносить стиль одной фотографии на другую\n\n"
                "Если я неправильно работаю, перезапусти меня командой /start")
