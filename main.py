import sys

from aiogram import Bot, Dispatcher, executor, types

from player import register_player
from game import create_game, end_game, join_to_game, \
    leave_from_game, spin_in_game

if(len(sys.argv) == 1):
    print('Не передан токен для авторизации')
    exit(1)

API_TOKEN = sys.argv[1]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('<i>Написать приветственный текст</i>')

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply('''
Основные команды
/info - информация о боте

/register - создать игрока
/create - создать новую игру
/join - вступить в активную игру
/leave - покинуть активную игру
/spin - запустить игру
/stop - удалить активную игру
    ''')

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await message.reply(
        '<i>Написать информацию о боте</i>',
        parse_mode=types.ParseMode.HTML
    )


@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    [is_success, error] = register_player(message.from_user)
    if (is_success is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            f'<i>Зарегистрирован новый игрок {message.from_user.full_name}</i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    [is_success, error] = create_game(message.from_user.id, message.chat.id)
    if (is_success is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            '<i>Создана новая игра. Для входа используйте команды /join, для окончания /stop</i>',
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    [is_success, error] = join_to_game(message.from_user.id, message.chat.id)
    if (is_success is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            f'<i>Игрок {message.from_user.full_name} вошел в игру</i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['leave'])
async def leave(message: types.Message):
    [is_success, error] = leave_from_game(message.from_user.id, message.chat.id)
    if (is_success is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            f'<i>Игрок {message.from_user.full_name} вышел из игры</i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['spin'])
async def spin(message: types.Message):
    await message.reply(
        '<i>Начинаю игру</i>',
        parse_mode=types.ParseMode.HTML
    )
    [result, error] = spin_in_game(message.from_user.id, message.chat.id)
    if (result is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            f'<i>Игра окончена\n{result} </i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    [is_success, error] = end_game(message.from_user.id, message.chat.id)
    if (is_success is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            '<i>Активная игра в чате остановлена</i>',
            parse_mode=types.ParseMode.HTML
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
