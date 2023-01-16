import sys

from aiogram import Bot, Dispatcher, executor, types

from player import register_player, get_player
from game import command_create_game, command_end_game, command_join_to_game, \
    command_leave_from_game, command_spin_in_game
from error import GameError, ERROR_UNEXPECTED, \
    ERROR_PLAYER_NOT_EXIST
from game import get_active_game

if(len(sys.argv) == 1):
    print('Не передан токен для авторизации')
    exit(1)

API_TOKEN = sys.argv[1]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('''
Бот для проведения простой игры
Каждому участнику случайно выбирается число
Побеждает тот участник, который получил большее число

Автор: @tablescable
Ссылка на проект: https://github.com/Thisman/spin_game_tg_bot
    ''')

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
    try:
        player = get_player(message.from_id)
        game = get_active_game(message.chat.id)
        active_game_status = f'Нет активной игры' if game is None else f'Есть активная игра, кол-во игроков {len(game["players"])}'
        active_game_bank = '' if game is None else f'Банк игры {len(game["players"]) * 10}'
        await message.reply(f'''
Текущий банк игрока {player["name"]} - {player["bank"]}

{active_game_status}
{active_game_bank}
        ''')
    except GameError as error:
        if (error == ERROR_PLAYER_NOT_EXIST):
            active_game_status = f'Нет активной игры' if game is None else f'Есть активная игра, кол-во игроков {len(game["players"])}'
            active_game_bank = '' if game is None else f'Банк игры {len(game["players"]) * 10}'
            await message.reply(f'''
{active_game_status}
{active_game_bank}
            ''')
        else:
            await message.reply(
                f'<i>{error}</i>',
                parse_mode=types.ParseMode.HTML
            )
    except Exception as error:
        print(error)
        await message.reply(
            f'<i>{ERROR_UNEXPECTED}</i>',
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    try:
        register_player(message.from_user)
        player = get_player(message.from_id)
        await message.reply(
            f'<i>Зарегистрирован новый игрок {player["name"]}</i>',
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            f'<i>{ERROR_UNEXPECTED}</i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    try:
        player = get_player(message.from_id)
        command_create_game(player, message.chat.id)
        await message.reply('''
Создана новая игра

Для участия в игре используйте команду /join
Для начала игры используйте команду /spin
Для окончания игры используйте команду /stop
            ''')
    except GameError as error:
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            f'<i>{ERROR_UNEXPECTED}</i>',
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    try:
        player = get_player(message.from_id)
        command_join_to_game(player, message.chat.id)
        await message.reply(
            f'<i>Игрок {player["name"]} вошел в игру</i>',
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            f'<i>{ERROR_UNEXPECTED}</i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['leave'])
async def leave(message: types.Message):
    try:
        player = get_player(message.from_id)
        command_leave_from_game(player, message.chat.id)
        await message.reply(
            f'<i>Игрок {player["name"]} вышел из игры</i>',
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            f'<i>{ERROR_UNEXPECTED}</i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['spin'])
async def spin(message: types.Message):
    await message.reply(
        '<i>Начинаю игру</i>',
        parse_mode=types.ParseMode.HTML
    )
    try:
        player = get_player(message.from_id)
        results = command_spin_in_game(player, message.chat.id)
        result_table_str = '\n'.join(map(lambda data: f'Игрок: {data["player"]["name"]} - {data["value"]}', results))
        winners_name = ','.join(map(lambda data: data['player']['name'], filter(lambda data: data['is_winner'], results)))
        await message.reply(f'''
Игра окончена
Побелители: {winners_name}
Таблица игры: 
{result_table_str}
        ''')
    except GameError as error:
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            f'<i>{ERROR_UNEXPECTED}</i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    try:
        player = get_player(message.from_id)
        command_end_game(player, message.chat.id)
        await message.reply(
            '<i>Активная игра в чате остановлена</i>',
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            f'<i>{ERROR_UNEXPECTED}</i>',
            parse_mode=types.ParseMode.HTML
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
