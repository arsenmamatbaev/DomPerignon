from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from core.GaleryObject import GaleryObject
from core.keyboards.admins import admin_keyboard, file_type_keyboard, quite
from core.database import DBConnection
from core.States import AdminsStates


async def admin_start(message: Message, db: DBConnection, state: FSMContext):
    await message.answer('🌟<b>Добро пожаловать в админ панель бота</b>\n'
                         'Чтобы выйти в пользовательский интерфейс отправьте боту команду /start',
                         reply_markup=admin_keyboard)
    await state.set_state(AdminsStates.admin_menu_state)
    await message.delete()


async def admin_menu(call: CallbackQuery, state: FSMContext, db: DBConnection):
    await call.answer()
    if call.data == 'mail':
        await call.message.answer('Пришлите файл для рассылки(фото или видео)',
                                  reply_markup=quite)
        await state.set_state(AdminsStates.mailing_file_state)
    elif call.data == 'add_file':
        await call.message.answer('<b>Отправьте файл</b><i>(фото/видео)</i> <b>которое хотите добавить</b>',
                                  reply_markup=quite)
        await state.set_state(AdminsStates.file_state)
    elif call.data == 'delete_file':
        galery = await db.get_galery
        for obj in galery:
            kb_choice = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Удалить файл',
                                                                                    callback_data=obj.file_name)]])
            if obj.file_type == 'photo':
                await call.message.answer_photo(photo=obj.file_id,
                                                caption=obj.file_name,
                                                reply_markup=kb_choice)
            else:
                await call.message.answer_video(video=obj.file_id,
                                                caption=obj.file_name,
                                                reply_markup=kb_choice)
        await state.set_state(AdminsStates.file_delete_state)
    await call.message.delete()


async def mailing_file(message: Message, db: DBConnection, state: FSMContext):
    if message.photo:
        await state.update_data({"file_type": "photo", "file_id": message.photo[-1].file_id})
    elif message.video:
        await state.update_data({"file_type": "video", "file_id": message.video.file_id})
    else:
        await message.answer('Видео или фото!',
                             reply_markup=quite)
        return
    await message.answer('Теперь пришлите текст рассылки',
                         reply_markup=quite)
    await state.set_state(AdminsStates.mailing_text_state)


async def mailing_text(message: Message, db: DBConnection, state: FSMContext, bot: Bot):
    await message.answer('Начинаю операцию рассылки, она может занять до 5 минут, ожидайте...')
    users = await db.get_users
    data = await state.get_data()
    send_user = 0
    if data['file_type'] == 'photo':
        for user in users:
            try:
                await bot.send_photo(chat_id=user.user_id,
                                     photo=data['file_id'],
                                     caption=message.text)
                send_user += 1
            except Exception as e:
                send_user -= 1
    elif data['file_type'] == 'video':
        for user in users:
            try:
                await bot.send_video(chat_id=user.user_id,
                                     video=data['file_id'],
                                     caption=message.text)
                send_user += 1
            except Exception as e:
                send_user -= 1
    await bot.send_message(chat_id=-4014679130,
                           text=f'Была произведена рассылка\nКолличество получателей: {send_user}')
    await message.answer('Рассылка завершена, подробности в группах с отчетами!')
    await message.answer('🌟<b>Добро пожаловать в админ панель бота</b>\n'
                         'Чтобы выйти в пользовательский интерфейс отправьте боту команду /start',
                         reply_markup=admin_keyboard)
    await state.set_state(AdminsStates.admin_menu_state)


async def delete_file_handler(call: CallbackQuery, state: FSMContext, db: DBConnection):
    galery = await db.get_galery_obj(call.data)
    if galery:
        await db.delete_galery(galery_file=galery)
        await call.message.answer("Удаление прошло успешно")
        await call.message.answer('🌟<b>Добро пожаловать в админ панель бота</b>\n'
                                  'Чтобы выйти в пользовательский интерфейс отправьте боту команду /start',
                                  reply_markup=admin_keyboard)
        await state.set_state(AdminsStates.admin_menu_state)
        await call.message.delete()


# Добавление файлов в галерею
async def file_handler(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data({'file_type': 'photo', 'file_id': message.photo[-1].file_id})
    elif message.video:
        await state.update_data({'file_type': 'video', 'file_id': message.video.file_id})
    await message.answer(
        '<b>Пришлите название для файла</b><i>(это нужно для управления файлом в дальнейшем для удаления)</i>',
        reply_markup=quite)
    await state.set_state(AdminsStates.file_name_state)
    await message.delete()


async def file_name_handler(message: Message, state: FSMContext, db: DBConnection):
    data = await state.get_data()
    galery = GaleryObject(
        file_name=message.text,
        file_type=data['file_type'],
        file_id=data['file_id']
    )
    await db.new_galery(galery=galery)
    await message.answer('Файл успешно добавлен в галерею')
    await message.answer('🌟<b>Добро пожаловать в админ панель бота</b>\n'
                         'Чтобы выйти в пользовательский интерфейс отправьте боту команду /start',
                         reply_markup=admin_keyboard)
    await state.set_state(AdminsStates.admin_menu_state)
# Конец блока(добавление файла в галерею)


async def admin_quite(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('🌟<b>Добро пожаловать в админ панель бота</b>\n'
                              'Чтобы выйти в пользовательский интерфейс отправьте боту команду /start',
                              reply_markup=admin_keyboard)
    await state.set_state(AdminsStates.admin_menu_state)
    await call.message.delete()

