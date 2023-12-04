import logging
import asyncpg
from typing import List, Union
from datetime import datetime
from core.GaleryObject import GaleryObject
from core.UserObject import User, DataUser


class DBConnection:
    """ Класс подключения к базе данных """
    def __init__(self,
                 connection: asyncpg.Connection) -> None:
        """
        Создает объект класса DBConnection
        :param connection: asyncpg.Connection
        """
        self.__connection = connection
        logging.info('Подключение к базе данных прошло успешно')

    async def create_tables(self) -> None:
        """
        Создает необходимые таблицы в базе данных
        :return: None
        """
        users_table = (
                "CREATE TABLE IF NOT EXISTS users("
                "id SERIAL PRIMARY KEY,"
                "user_id BIGINT UNIQUE NOT NULL,"
                "name VARCHAR(250) NOT NULL,"
                "username VARCHAR(50),"
                "updated_at VARCHAR(50) DEFAULT ' ',"
                "register_date VARCHAR(50));"
        )
        await self.__connection.execute(users_table)
        files_table = ("CREATE TABLE IF NOT EXISTS galery("
                       "id SERIAL PRIMARY KEY,"
                       "name VARCHAR(100),"
                       "file_type VARCHAR(50),"
                       "file_id VARCHAR(300));")
        await self.__connection.execute(files_table)
        admins_table = ("CREATE TABLE IF NOT EXISTS admins("
                        "id SERIAL PRIMARY KEY,"
                        "user_id BIGINT UNIQUE,"
                        "name VARCHAR(250),"
                        "username VARCHAR(50));")
        await self.__connection.execute(admins_table)

    async def create_or_update(self,
                               user: User) -> DataUser:
        """
        Добавляет в базу нового пользователя
        :param user: объект класса User
        :return: DataUser
        """
        now_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        query = ("INSERT INTO users (user_id, name, username, register_date) "
                 f"VALUES ({user.user_id}, '{user.name}', '{user.username}', '{now_date}') "
                 f"ON CONFLICT (user_id) DO UPDATE SET updated_at = '{now_date}'")
        await self.__connection.execute(query)
        return DataUser(
            user_id=user.user_id,
            name=user.name,
            username=user.username,
            updated_at=now_date,
            register_date=now_date
        )

    async def new_galery(self,
                         galery: GaleryObject) -> None:
        """
        Добавляет новый файл в галерею
        :param galery: класс GaleryObject
        :return: None
        """
        query = ("INSERT INTO galery (name, file_type, file_id) "
                 f"VALUES ('{galery.file_name}', '{galery.file_type}', '{galery.file_id}')")
        await self.__connection.execute(query)

    @property
    async def get_galery(self) -> List[GaleryObject]:
        query = "SELECT * FROM galery;"
        galery_objects = await self.__connection.fetch(query)
        return_galery = []
        for galery_object in galery_objects:
            return_galery.append(
                GaleryObject(
                    file_name=galery_object['name'],
                    file_type=galery_object['file_type'],
                    file_id=galery_object['file_id']
                )
            )
        return return_galery

    async def get_galery_obj(self,
                             file_name: str) -> Union[GaleryObject, bool]:
        query = f"SELECT * FROM galery WHERE name = '{file_name}';"
        gobj = await self.__connection.fetch(query)
        if gobj:
            return GaleryObject(
                file_name=gobj[0]['name'],
                file_type=gobj[0]['file_type'],
                file_id=gobj[0]['file_id']
            )
        return False

    async def delete_galery(self,
                            galery_file: GaleryObject):
        query = f"DELETE FROM galery WHERE name = '{galery_file.file_name}'"
        await self.__connection.execute(query)

    @property
    async def get_admins(self) -> Union[List[User], User]:
        query = "SELECT * FROM admins;"
        admins = await self.__connection.fetch(query)
        return_admins: list = []
        for admin in admins:
            return_admins.append(
                User(user_id=admin['user_id'],
                     name=admin['name'],
                     username=admin['username'])
            )
        return return_admins

    @property
    async def get_users(self) -> List[User]:
        query = "SELECT * FROM users;"
        users = await self.__connection.fetch(query)
        return_users = []
        for us in users:
            return_users.append(
                User(
                    user_id=us['user_id'],
                    name=us['name'],
                    username=us['username']
                )
            )
        return return_users


class DataBase:
    def __init__(self,
                 host: str = '127.0.0.1',
                 port: int = 5432,
                 user: str = 'postgres',
                 password: str = 'postgres') -> None:
        """
        Создает объект класса DataBase
        :param host: Хост базы данных
        :param port: Порт базы данных
        :param user: Пользователь базы данных
        :param password: Пароль от базы данных
        """
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password

    @property
    async def connect(self) -> DBConnection:
        connection = await asyncpg.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password
        )

        return DBConnection(
            connection=connection
        )

