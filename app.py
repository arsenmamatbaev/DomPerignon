import os
import asyncio
import logging
from dotenv.main import load_dotenv
""" Все импорты aiogram """
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command, StateFilter
""" Импорт filters """
from core.filters.IsAdmin import IsAdmin
""" Импорт middlewares """
from core.middlewares.dbmiddleware import DbMiddleware
""" Импорт handlers """
from core.handlers.users.bot_start import start
from core.handlers.users.bot_menu import main_menu, get_contact
from core.handlers.admins.admin import admin_start, admin_menu, file_handler, admin_quite, file_name_handler, delete_file_handler
from core.handlers.admins.admin import mailing_file, mailing_text
""" Другие импорты """
from core.database import DataBase, DBConnection
from core.States import States, AdminsStates


load_dotenv()

main_loop = asyncio.new_event_loop()
bot = Bot(os.getenv('API_KEY'),
          parse_mode='html')
dp = Dispatcher()
db = DataBase(password='555326')
connection: DBConnection


async def on_startup():
    global connection
    logging.basicConfig(level=logging.INFO)
    connection = await db.connect
    await connection.create_tables()
    dp.update.middleware.register(DbMiddleware(connection))  # Проброс базы данных в хэндлер


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    dp.message.register(start, CommandStart())  # Команда /start
    dp.message.register(get_contact, StateFilter(States.contact_state))
    dp.message.register(admin_start, IsAdmin(), Command(commands=['admin']))  # Команда /admin
    dp.message.register(main_menu, StateFilter(States.main_menu_state))
    dp.callback_query.register(admin_quite, F.data == 'quite')
    dp.callback_query.register(delete_file_handler, StateFilter(AdminsStates.file_delete_state))
    dp.callback_query.register(admin_menu, StateFilter(AdminsStates.admin_menu_state))
    dp.message.register(file_handler, StateFilter(AdminsStates.file_state))
    dp.message.register(file_name_handler, StateFilter(AdminsStates.file_name_state))
    dp.message.register(mailing_file, StateFilter(AdminsStates.mailing_file_state))
    dp.message.register(mailing_text, StateFilter(AdminsStates.mailing_text_state))
    # dp.message.register(test)
    await dp.start_polling(bot)


if __name__ == '__main__':
    main_loop.run_until_complete(main())
