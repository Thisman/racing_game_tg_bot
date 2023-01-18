import sys
import time
import random

from aiogram import Bot, Dispatcher, executor, types

from player import register_player, get_player
from game import command_create_game, command_end_game, command_join_to_game, \
    command_leave_from_game, command_spin_in_game, get_process_game, \
    GAME_SPIN_FINISHED_STATUS, GAME_SPIN_START_STATUS, \
    GAME_SPIN_PROCESS_STATUS
from error import GameError, ERROR_UNEXPECTED, \
    ERROR_BOT_TOKEN_NOT_EXIST
from game import get_active_game
import templates as tpl

if(len(sys.argv) == 1):
    print(ERROR_BOT_TOKEN_NOT_EXIST)
    exit(1)

API_TOKEN = sys.argv[1]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        tpl.get_start_template_str(),
        parse_mode=types.ParseMode.HTML
    )

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply(
        tpl.get_help_template_str(),
        parse_mode=types.ParseMode.HTML
    )

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    try:
        player = get_player(message.from_id)
        game = get_active_game(message.chat.id)
        await message.reply(tpl.get_info_template_str(player, game))
    except GameError as error:
        await message.reply(
            tpl.get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            tpl.get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    try:
        await message.reply(
            tpl.get_rule_tempalte_str(),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            tpl.get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            tpl.get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    try:
        register_player(message.from_user)
        player = get_player(message.from_id)
        await message.reply(
            tpl.get_player_register_template_str(player),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            tpl.get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            tpl.get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    try:
        if(get_process_game(message.chat.id) is not None):
            return

        player = get_player(message.from_id)
        command_create_game(player, message.chat.id)
        await message.reply(tpl.get_game_create_tempalte_str())
    except GameError as error:
        await message.reply(
            tpl.get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            tpl.get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    try:
        if(get_process_game(message.chat.id) is not None):
            return

        player = get_player(message.from_id)
        command_join_to_game(player, message.chat.id)
        await message.reply(
            tpl.get_player_join_template_str(player),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            tpl.get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            tpl.get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['leave'])
async def leave(message: types.Message):
    try:
        if(get_process_game(message.chat.id) is not None):
            return

        player = get_player(message.from_id)
        command_leave_from_game(player, message.chat.id)
        await message.reply(
            tpl.get_player_leave_template_str(player),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            tpl.get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            tpl.get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['spin'])
async def spin(message: types.Message):
    try:
        if(get_process_game(message.chat.id) is not None):
            return

        player = get_player(message.from_id)
        results = command_spin_in_game(player, message.chat.id)
        randomize_ordered_results = random.sample(results, k=len(results))

        game_process_message = await message.reply(
            tpl.get_game_results_template_str(results, [], GAME_SPIN_START_STATUS),
            parse_mode=types.ParseMode.HTML
        )
        time.sleep(1)
        for index, _ in enumerate(results):
            print(index)
            await game_process_message.edit_text(
                tpl.get_game_results_template_str(results, randomize_ordered_results[0: index], GAME_SPIN_PROCESS_STATUS),
                parse_mode=types.ParseMode.HTML
            )
            time.sleep(1)

        await game_process_message.edit_text(
            tpl.get_game_results_template_str(results, randomize_ordered_results, GAME_SPIN_FINISHED_STATUS),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            tpl.get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            tpl.get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    try:
        if(get_process_game(message.chat.id) is not None):
            return

        command_end_game(message.chat.id)
        await message.reply(
            tpl.get_stop_game_template_str(),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            tpl.get_error_template_str(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            tpl.get_error_template_str(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
