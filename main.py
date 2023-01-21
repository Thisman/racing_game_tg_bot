import sys
import time

from aiogram import Bot, Dispatcher, executor, types

from modules.player import Player
from modules.game import Game
from modules.commands import START_COMMAND, RULES_COMMAND, \
    HELP_COMMAND, INFO_COMMAND, REGISTER_PLAYER_COMMAND, \
    REGISTER_GAME_COMMAND, JOIN_GAME_COMMAND, \
    LEAVE_GAME_COMMAND, START_GAME_COMMAND, \
    STOP_GAME_COMMAND
from modules.error import GameError, ERROR_UNEXPECTED, \
    ERROR_BOT_TOKEN_NOT_EXIST, ERROR_PLAYER_NOT_EXIST, \
    ERROR_GAME_NOT_EXIST, ERROR_PLAYER_ALREADY_IN_GAME, \
    ERROR_PLAYER_NOT_IN_GAME, ERROR_NOT_ENOUGH_PLAYER_BANK, \
    ERROR_GAME_NOT_ENOUGH_PLAYERS

from renderers.bot_renderer import BotRenderer
from renderers.player_renderer import PlayerRenderer
from renderers.game_renderer import GameRenderer

if(len(sys.argv) == 1):
    print(ERROR_BOT_TOKEN_NOT_EXIST)
    exit(1)

API_TOKEN = sys.argv[1]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=[START_COMMAND])
async def start(message: types.Message):
    await message.reply(
        BotRenderer.render_start_tpl(),
        parse_mode=types.ParseMode.HTML
    )

@dp.message_handler(commands=[HELP_COMMAND])
async def help(message: types.Message):
    await message.reply(
        BotRenderer.render_help_tpl(),
        parse_mode=types.ParseMode.HTML
    )

@dp.message_handler(commands=[INFO_COMMAND])
async def info(message: types.Message):
    try:
        player = Player.load(message.from_id)
        game = Game.load(message.chat.id)

        await message.reply(
            BotRenderer.render_info_tpl(player, game),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            BotRenderer.render_error_tpl(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            BotRenderer.render_error_tpl(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=[RULES_COMMAND])
async def rules(message: types.Message):
    try:
        await message.reply(
            BotRenderer.render_rules_tpl(),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            BotRenderer.render_error_tpl(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            BotRenderer.render_error_tpl(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=[REGISTER_PLAYER_COMMAND])
async def register_player(message: types.Message):
    try:
        new_player = Player.register(message.from_user)

        await message.reply(
            PlayerRenderer.render_register_success_tpl(new_player),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            BotRenderer.render_error_tpl(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            BotRenderer.render_error_tpl(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=[REGISTER_GAME_COMMAND])
async def register_game(message: types.Message):
    try:
        if(Game.get_stared_game(message.chat.id) is not None):
            return

        Game.register(message.chat.id)

        await message.reply(
            GameRenderer.render_register_success_tpl(),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            BotRenderer.render_error_tpl(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            BotRenderer.render_error_tpl(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=[
    JOIN_GAME_COMMAND + '_0',
    JOIN_GAME_COMMAND + '_1',
    JOIN_GAME_COMMAND + '_2',
    JOIN_GAME_COMMAND + '_3',
    JOIN_GAME_COMMAND + '_4',
])
async def join_game(message: types.Message):
    try:
        if(Game.get_stared_game(message.chat.id) is not None):
            return

        player = Player.load(message.from_id)
        if (player is None):
            raise GameError(ERROR_PLAYER_NOT_EXIST)
        
        if (player.is_enough_bank() is False):
            raise GameError(ERROR_NOT_ENOUGH_PLAYER_BANK)

        game = Game.load(message.chat.id)
        if (game is None or game.is_ready() is False):
            raise GameError(ERROR_GAME_NOT_EXIST)

        if (game.is_player_in_game(player) is True):
            raise GameError(ERROR_PLAYER_ALREADY_IN_GAME)

        command = message.text
        if ('@' in message.text):
            command = message.text.split('@')[0]

        command = command.split('_')
        horse_id = int(command[2])

        game.join(player, horse_id)
        game.save()

        await message.reply(
            GameRenderer.render_player_join_success_tpl(player, horse_id),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            BotRenderer.render_error_tpl(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            BotRenderer.render_error_tpl(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=[LEAVE_GAME_COMMAND])
async def leave_game(message: types.Message):
    try:
        if(Game.get_stared_game(message.chat.id) is not None):
            return

        player = Player.load(message.from_id)
        if (player is None):
            raise GameError(ERROR_PLAYER_NOT_EXIST)

        game = Game.load(message.chat.id)
        if (game is None or game.is_ready() is False):
            raise GameError(ERROR_GAME_NOT_EXIST)

        if (game.is_player_in_game(player) is False):
            raise GameError(ERROR_PLAYER_NOT_IN_GAME)

        game.leave(player)
        game.save()

        await message.reply(
            GameRenderer.render_player_leave_success__plt(player),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            BotRenderer.render_error_tpl(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            BotRenderer.render_error_tpl(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=[START_GAME_COMMAND])
async def start_game(message: types.Message):
    try:
        if(Game.get_stared_game(message.chat.id) is not None):
            return

        game = Game.load(message.chat.id)
        if (game is None or game.is_ready() is False):
            raise GameError(ERROR_GAME_NOT_EXIST)

        if (len(game.get_participators()) == 0):
            raise GameError(ERROR_GAME_NOT_ENOUGH_PLAYERS)

        rounds = game.start()
        game.save()

        game_message = await message.reply(
            GameRenderer.render_game_start_tpl(game.get_horses()),
            parse_mode=types.ParseMode.HTML,
        )

        for round in rounds():
            time.sleep(1.5)
            await game_message.edit_text(
                GameRenderer.render_game_round_tpl(round),
                parse_mode=types.ParseMode.HTML,
            )
        
        game.stop()
        game.save()

        winner_horses_ids = map(lambda data: data['id'], game.get_winner_horses())
        winner_players = []
        for [participator, bet] in game.get_participators():
            player = Player.load(participator)
            if (player is None):
                pass

            if (bet in winner_horses_ids):
                player.set_bank(player.get_bank() + 10)
                winner_players += [player]
            else:
                player.set_bank(player.get_bank() - 10)
            player.save()

        await game_message.edit_text(
            GameRenderer.render_game_end_tpl(game.get_horses(), winner_players),
            parse_mode=types.ParseMode.HTML,
        )
        pass
    except GameError as error:
        await message.reply(
            BotRenderer.render_error_tpl(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            BotRenderer.render_error_tpl(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=[STOP_GAME_COMMAND])
async def stop_game(message: types.Message):
    try:
        if(Game.get_stared_game(message.chat.id) is not None):
            return

        game = Game.load(message.chat.id)
        if (game is None or game.is_ready() is False):
            raise GameError(ERROR_GAME_NOT_EXIST)

        game.stop()
        game.save()

        await message.reply(
            GameRenderer.render_stop_tpl(),
            parse_mode=types.ParseMode.HTML
        )
    except GameError as error:
        await message.reply(
            BotRenderer.render_error_tpl(error),
            parse_mode=types.ParseMode.HTML
        )
    except Exception as error:
        print(error)
        await message.reply(
            BotRenderer.render_error_tpl(ERROR_UNEXPECTED),
            parse_mode=types.ParseMode.HTML
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
