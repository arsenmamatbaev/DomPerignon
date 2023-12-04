from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from core.database import DBConnection
from core.States import States
from core.keyboards.users import start_keyboard, get_contact_keyboard


async def main_menu(message: Message, db: DBConnection, state: FSMContext):
    if message.text == 'Заказать':
        await message.answer('📲<b>Оставьте нам свой контакт чтобы мы могли связаться с вами</b>',
                             reply_markup=get_contact_keyboard)
        await state.set_state(States.contact_state)
    elif message.text == 'Галерея':
        media_list = []
        galery = await db.get_galery
        for obj in galery:
            if obj.file_type == 'photo':
                media_list.append(
                    InputMediaPhoto(media=obj.file_id)
                )
            else:
                media_list.append(
                    InputMediaVideo(media=obj.file_id)
                )
            if len(media_list) == 10:
                await message.answer_media_group(media_list)
                media_list.clear()
        await message.answer_media_group(media_list)


async def get_contact(message: Message, db: DBConnection, state: FSMContext, bot: Bot):
    if message.contact:
        await message.answer('✨<b>Ваша заявка принята, мы свяжемся с вами в ближайшее время</b>',
                             reply_markup=start_keyboard)
        await bot.send_contact(chat_id=-4014679130,
                               phone_number=message.contact.phone_number,
                               first_name=message.contact.first_name)
        await state.set_state(States.main_menu_state)

