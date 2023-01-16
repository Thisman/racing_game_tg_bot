ERROR_UNEXPECTED = 'Произошла ошибка! Попробуйте снова!'
ERROR_COMMAND_NOT_IN_CHAT = 'Нельзя вызвать команду не в чате!'

ERROR_CREATE_PLAYER = 'Не получилось создать пользователя! Попробуйте еще раз'
ERROR_PLAYER_ALREADY_EXIST = 'Пользоветель уже существует!'
ERROR_PLAYER_NOT_EXIST = 'Игрок не зарегистрирован. Для регистрации выполните команду /register'
ERROR_PLAYER_ALREADY_IN_GAME = 'Игрок уже в игре! Чтобы выйти, выполните команду /leave'
ERROR_PLAYER_NOT_IN_GAME = 'Игрок не в игре! Чтобы войти, выполните команду /join'
ERROR_PLAYER_NOT_ACCESS = 'Нет доступа для выполнения этой команды!'

ERROR_GAME_ALREADY_EXIST = 'В чате уже есть активная игра! Чтобы остановить ее, выполните команду /stop'
ERROR_GAME_NOT_EXIST = 'В чате нет активной игры! Чтобы запустить игру, выполните команду /create'
ERROR_GAME_NOT_ENOUGH_PLAYERS = 'Нельзя начинать игру с одним или меньше игроками!'

class GameError(Exception):
    pass
