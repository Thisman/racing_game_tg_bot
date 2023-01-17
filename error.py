ERROR_UNEXPECTED = 'Произошла ошибка!\nПопробуйте снова!'
ERROR_COMMAND_NOT_IN_CHAT = 'Нельзя вызвать команду не в чате!'

ERROR_CREATE_PLAYER = 'Не получилось создать пользователя!\nПопробуйте еще раз'
ERROR_PLAYER_ALREADY_EXIST = 'Пользоветель уже существует!'
ERROR_PLAYER_NOT_EXIST = 'Игрок не зарегистрирован.\nДля регистрации выполните команду /register'
ERROR_PLAYER_ALREADY_IN_GAME = 'Игрок уже в игре!\nЧтобы выйти, выполните команду /leave'
ERROR_PLAYER_NOT_IN_GAME = 'Игрок не в игре!\nЧтобы войти, выполните команду /join'

ERROR_GAME_ALREADY_EXIST = 'В чате уже есть активная игра!\nЧтобы остановить ее, выполните команду /stop'
ERROR_GAME_NOT_EXIST = 'В чате нет активной игры!\nЧтобы запустить игру, выполните команду /create'
ERROR_GAME_NOT_ENOUGH_PLAYERS = 'Нельзя начинать игру с одним или меньше игроками!'

ERROR_BOT_TOKEN_NOT_EXIST = 'Не передан токен для авторизации бота!'

class GameError(Exception):
    pass
