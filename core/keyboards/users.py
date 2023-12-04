from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Заказать'
        )
    ],
    [
        KeyboardButton(
            text='Галерея'
        )
    ]
], resize_keyboard=True)


get_contact_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📞Оставить контакт', request_contact=True)]
], resize_keyboard=True)

