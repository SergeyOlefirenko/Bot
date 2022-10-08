
# Ссылка на Бот: t.me/Bobot_hw_Bot
# Ссылка на GIT:
from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite3
TOKEN = os.environ['token']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
users = {}

def create_users():
    connect = sqlite3.connect('chatUsers_database.db')
    cursor = connect.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS Users('
        'UserID integer primary key,'
        'Firstname text,'
        'Lastname text,'
        'Birthday text,'
        'Phone text,'
        'Mail text'
        ');'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS Messages('
        'UserID integer,'
        'MessageID integer primary key autoincrement,'
        'TextMessage text'
        ');'
    )
    connect.commit()
    cursor.close()


create_users()


def get_user_by_id(user_id):
    connect = sqlite3.connect('chatUsers_database.db')
    cursor = connect.cursor()
    request_in_db = f'SELECT * from Users where UserID = {user_id} '
    user = cursor.execute(request_in_db).fetchall()
    connect.commit()
    cursor.close()
    return user


def update_user_by_id(user_id, text_message):
    connect = sqlite3.connect('chatUsers_database.db')
    cursor = connect.cursor()
    request_in_db = f"UPDATE Users SET 'TextMessage' = {text_message} where UserID = {user_id}"
    cursor.execute(request_in_db)
    connect.commit()
    cursor.close()

def insert_user(user: dict):
    connect = sqlite3.connect('chatUsers_database.db')
    cursor = connect.cursor()
    request_in_db = f'INSERT INTO Users (UserID, Firstname, Lastname, Birthday,Phone, Mail) VALUES ("{user["UserID"]}",' \
                    f' "{str(user["Firstname"])}", "{str(user["Lastname"])}", "{str(user["Birthday"])}",' \
                    f'"{str(user["Phone"])}", "{str(user["Mail"])}");'
    cursor.execute(request_in_db)
    connect.commit()
    cursor.close()


def insert_message(message: dict):
    connect = sqlite3.connect('chatUsers_database.db')
    cursor = connect.cursor()
    request_in_db = f'INSERT INTO Messages (UserID, TextMessage) VALUES ("{message["UserID"]}",' \
                    f'"{str(message["TextMessage"])}");'
    cursor.execute(request_in_db)
    connect.commit()
    cursor.close()

@dp.message_handler()
async def recording(message: types.Message):
    print(message)
    user = get_user_by_id(message.from_user.id)
    if len(user) == 0:
        insert_user({"UserID": message.from_user.id, "Firstname": message.from_user.first_name,
                     "Lastname": message.from_user.last_name, "Birthday": None,
                     "Phone": None, "Mail": None})
    insert_message({"UserID": message.from_user.id, "TextMessage": message.text})
    print('\n', 'User ID:', message.from_user.id, '\n',
          'User name:', message.from_user.first_name,
          message.from_user.last_name, '\n',
          'Wrote:', message.text, '\n',
          'ChatID:', message.message_id)
    users.update({message.from_user.id: message.from_user.first_name})
    await message.answer(text = f'Ну все, брат, ты попал. Теперь и на тебя у нас досье:''\n'
                                f'UserID: {message.from_user.id}''\n'
                                f'User first name: {message.from_user.first_name}''\n'
                                f'User last name: {message.from_user.last_name}''\n'
                                f'ChatID: {message.message_id}')
    # await message.answer(message.text)
    # await message.reply(message.text)
    text = f'User {message.from_user.first_name} wrote {message.text}'
    for i in users.keys():
        if i != message.from_user.id:
            await bot.send_message(chat_id=i,
                                   text=text)


if __name__ == '__main__':
    executor.start_polling(dp)
