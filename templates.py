import emoji

from player import PlayerData
from game import GameData, GameResult

from game import GAME_SPIN_FINISHED_STATUS, GAME_SPIN_START_STATUS, \
    GAME_SPIN_PROCESS_STATUS

# TODO: подумать, какой можно подход сделать для работы с шаблонами строк?

def get_start_template_str():
    return '''
Бот для проведения простой игры
/rules - Правила
/help - Команды 

Автор: @tablescable
Ссылка на проект: https://github.com/Thisman/spin_game_tg_bot
    '''

def get_rule_tempalte_str():
    return '''
<b>Правила</b>:
1. Каждому участнику случайно выбирается число
2. Побеждают те участники, которые получили большее число
3. Стоимость игры 10 баллов
4. Приз - общий банк поделенный между всеми победителями

Доступные команды /help
    '''

def get_help_template_str():
    return '''
<b>Основные команды</b>
/info- Информация о банке игрока и статусе игры
/register- Зарегистрировать игрока

/create - Создать новую игру
/join - Вступить в игру
/leave - Покинуть игру
/spin - Запустить игру
/stop - Остановить и удалить игру
    '''

def get_info_template_str(player: PlayerData, game: GameData):
    game_status_str = f'''
{f'Нет активной игры' if game is None else f'Есть активная игра, кол-во игроков {len(game["players"])}'}
{'' if game is None else f'Банк игры {len(game["players"]) * 10}'}
    '''

    player_status_str = f'''
Текущий банк игрока {player["name"]} - {player["bank"]}
    '''

    return f'''
{player_status_str}{game_status_str}
    '''


def get_error_template_str(error):
    return f'<i>{error}</i>'

def get_player_register_template_str(player: PlayerData):
    return f'<i>Зарегистрирован новый игрок {player["name"]}!</i>'


def get_game_create_tempalte_str():
    return '''
Создана новая игра!

/join - Войти в игру
/spin - Начать игру
/stop - Закончить игру
    '''

def get_player_spin_str(player: PlayerData, value: int | str):
    return f'{player["name"]} выкинул {value}'

def get_player_icon_str(winner: bool, finished: bool):
    if (finished is True and winner is True):
        return emoji.emojize(':tada:', language='alias')
    else:
        return ''

def get_game_spin_status_str(spin_status: str):
    if (spin_status == GAME_SPIN_START_STATUS):
        return 'Игра началась!'
    
    if (spin_status == GAME_SPIN_PROCESS_STATUS):
        return 'Рулетка крутится...'
    
    if (spin_status == GAME_SPIN_FINISHED_STATUS):
        return 'Игра окончена!'

def get_game_results_template_str(results: list[GameResult], randomized_results: list[GameResult], spin_status: str):
    result_table_str = ''
    is_spin_finished = spin_status == GAME_SPIN_FINISHED_STATUS
    for data in results:
        show_results = data in randomized_results
        if (show_results is True):
            result_table_str += f'\n{get_player_spin_str(data["player"], data["value"])} {get_player_icon_str(data["is_winner"], is_spin_finished)}'
        else:
            result_table_str += f'\n{get_player_spin_str(data["player"], "・・")}'

    return f'''
{get_game_spin_status_str(spin_status)}

Таблица игры: {result_table_str}
    '''

def get_player_join_template_str(player: PlayerData):
    return f'<i>Игрок {player["name"]} вошел в игру!</i>'
    
def get_player_leave_template_str(player: PlayerData):
    return f'<i>Игрок {player["name"]} покинул игру</i>'

def get_stop_game_template_str():
    return '<i>Игра закончилась!</i>'
