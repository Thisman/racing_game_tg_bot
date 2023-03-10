from aiogram import types

from modules.commands import REGISTER_PLAYER_COMMAND, \
    NEW_GAME_COMMAND, LEAVE_GAME_COMMAND, STOP_GAME_COMMAND

ERROR_UNEXPECTED = 'Произошла ошибка!\nПопробуйте снова!'

ERROR_REGISTER_PLAYER = 'Не получилось создать игрока!\nПопробуйте еще раз!'
ERROR_PLAYER_ALREADY_EXIST = 'Игрок уже зарегистрирован!'
ERROR_PLAYER_NOT_EXIST = f'Игрок не зарегистрирован.\nДля регистрации выполните команду /{REGISTER_PLAYER_COMMAND}'
ERROR_PLAYER_ALREADY_IN_GAME = f'Игрок уже участвует в игре!\nЧтобы выйти, выполните команду /{LEAVE_GAME_COMMAND}'
ERROR_PLAYER_NOT_IN_GAME = f'Игрок уже не участвует в игре!'

ERROR_REGISTER_GAME = 'Не получилось создать игру!\nПопробуйте еще раз!'
ERROR_GAME_ALREADY_EXIST = f'Игра уже создана!\nЧтобы остановить ее, выполните команду /{STOP_GAME_COMMAND}'
ERROR_READY_GAME_NOT_EXIST = f'Нет открытой игры!\nЧтобы запустить игру, выполните команду /{NEW_GAME_COMMAND}'
ERROR_GAME_NOT_ENOUGH_PLAYERS = 'Нельзя начинать игру без игроков!'
ERROR_NOT_ENOUGH_PLAYER_BANK = 'Недостаточно средств для игры!'

ERROR_BOT_TOKEN_NOT_EXIST = 'Не передан токен для авторизации бота!'

class GameError(Exception):
    pass
