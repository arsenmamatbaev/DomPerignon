from aiogram.filters import BaseFilter
from aiogram.types import Message
from core.database import DBConnection


class IsAdmin(BaseFilter):

    async def __call__(self, message: Message, db: DBConnection):
        admins = await db.get_admins
        for admin in admins:
            if admin.user_id == message.from_user.id:
                return True
        return False

