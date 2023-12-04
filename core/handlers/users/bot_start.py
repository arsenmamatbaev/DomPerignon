from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.States import States
from core.keyboards.users import start_keyboard
from core.Files import start_photo
from core.messages import start_message
from core.UserObject import User
from core.database import DBConnection


async def start(message: Message, db: DBConnection, state: FSMContext):
    user = User(
        user_id=message.from_user.id,
        name=message.from_user.full_name,
        username=message.from_user.username
    )
    await db.create_or_update(user)
    await message.answer_photo(photo=start_photo,
                               caption=start_message,
                               reply_markup=start_keyboard)
    await state.set_state(States.main_menu_state)

