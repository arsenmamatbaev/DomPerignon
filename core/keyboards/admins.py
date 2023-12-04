from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='📬Рассылка',
            callback_data='mail'
        )
    ],
    [
        InlineKeyboardButton(
            text='📁Добавить файл(галерея)',
            callback_data='add_file'
        )
    ],
    [
        InlineKeyboardButton(
            text='🗑Удалить файл(галерея)',
            callback_data='delete_file'
        )
    ]
])


file_type_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Фото',
            callback_data='photo'
        )
    ],
    [
        InlineKeyboardButton(
            text='Видео',
            callback_data='video'
        )
    ]
])


quite = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='🔙Отмена',
            callback_data='quite'
        )
    ]
])

