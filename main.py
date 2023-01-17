import sys
import time

from aiogram import Bot, Dispatcher, executor, types

from player import register_player, get_player
from game import command_create_game, command_end_game, command_join_to_game, \
    command_leave_from_game, command_spin_in_game
from error import GameError, ERROR_UNEXPECTED, \
    ERROR_PLAYER_NOT_EXIST, ERROR_BOT_TOKEN_NOT_EXIST
from game import get_active_game
from templates import get_help_template_str, get_info_template_str, \
    get_start_template_str, get_error_template_str, \
    get_game_create_tempalte_str, get_game_result_template_str, \
    get_player_register_template_str, get_player_join_template_str, \
    get_player_leave_template_str, get_stop_game_template_str, \
    get_player_spin_str, get_start_game_template_str

if(len(sys.argv) == 1):
    print(ERROR_BOT_TOKEN_NOT_EXIST)
    exit(1)

API_TOKEN = sys.argv[1]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        get_start_template_str(),
        parse_mode=types.ParseMode.HTML
    )

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply(get_help_template_str())

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    try:
        player = get_player(message.from_id)
        game = get_active_game(message.chat.id)
        await message.reply(get_info_template_str(player, game))
    except GameError as error:
        error_text = get_info_template_str(None, game) if error == ERROR_PLAYER_NOT_EXIST else get_error_template_str(error)
        await message.reply(
            get_error_template_str(error_text),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    try:
        register_player(message.from_user)
        player = get_player(message.from_id)
        await message.reply(
            get_player_register_template_str(player),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    try:
        player = get_player(message.from_id)
        command_create_game(player, message.chat.id)
        await message.reply(get_game_create_tempalte_str())
    except GameError as error:
        await message.reply(
            get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    try:
        player = get_player(message.from_id)
        command_join_to_game(player, message.chat.id)
        await message.reply(
            get_player_join_template_str(player),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['leave'])
async def leave(message: types.Message):
    try:
        player = get_player(message.from_id)
        command_leave_from_game(player, message.chat.id)
        await message.reply(
            get_player_leave_template_str(player),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['spin'])
async def spin(message: types.Message):
    try:
        player = get_player(message.from_id)
        results = command_spin_in_game(player, message.chat.id)
        game_process_message = await message.reply(
            get_start_game_template_str(),
            parse_mode=types.ParseMode.HTML
        )
        time.sleep(1)
        for data in results:
            await game_process_message.edit_text(
                get_player_spin_str(data),
                parse_mode=types.ParseMode.HTML
            )
            time.sleep(1)

        await game_process_message.edit_text(
            get_game_result_template_str(results),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await game_process_message.reply(
            get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await game_process_message.reply(
            get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    try:
        player = get_player(message.from_id)
        command_end_game(player, message.chat.id)
        await message.reply(
            get_stop_game_template_str(),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
