
from player import PlayerData
from game import GameData, GameResult


def get_start_template_str():
    return '''
Бот для проведения простой игры

<b>Правила</b>:
1. Каждому участнику случайно выбирается число
2. Побеждают те участники, которые получили большее число
3. Стоимость игры 10 баллов
4. Приз - общий банк поделенный между всеми победителями

Автор: @tablescable
Ссылка на проект: https://github.com/Thisman/spin_game_tg_bot
    '''

def get_help_template_str():
    return '''
Основные команды
/info - общая информация

/register - создать игрока
/create - создать новую игру
/join - вступить в активную игру
/leave - покинуть активную игру
/spin - запустить игру
/stop - удалить активную игру
    '''

def get_info_game_template_str(game: GameData):
    return f'''
{f'Нет активной игры' if game is None else f'Есть активная игра, кол-во игроков {len(game["players"])}'}
{'' if game is None else f'Банк игры {len(game["players"]) * 10}'}
    '''

def get_info_template_str(player: PlayerData | None, game: GameData):
    if (player is not None):
        return f'''
Текущий банк игрока {player["name"]} - {player["bank"]}
{get_info_game_template_str(game)}
        '''
    else:
        return get_info_game_template_str(game)

def get_game_create_tempalte_str():
    return '''
Создана новая игра

Для участия в игре используйте команду /join
Для начала игры используйте команду /spin
Для окончания игры используйте команду /stop
    '''

def get_game_result_template_str(results: GameResult):
    result_table_str = '\n'.join(map(get_player_spin_str, results))
    winners_name = ','.join(map(lambda data: data['player']['name'], filter(lambda data: data['is_winner'], results)))
    return f'''
Игра окончена
<b>Победители</b>: {winners_name}

Таблица игры: 
{result_table_str}
    '''

def get_error_template_str(error):
    return f'<i>{error}</i>'

def get_player_register_template_str(player: PlayerData):
    return f'<i>Зарегистрирован новый игрок {player["name"]}!</i>'

def get_player_join_template_str(player: PlayerData):
    return f'<i>Игрок {player["name"]} вошел в игру!</i>'
    
def get_player_leave_template_str(player: PlayerData):
    return f'<i>Игрок {player["name"]} покинул игру</i>'

def get_stop_game_template_str():
    return '<i>Активная игра в чате остановлена!</i>'

def get_start_game_template_str():
    return '<i>Игра начинается!</i>'

def get_player_spin_str(data: GameResult):
    return f'Игрок: {data["player"]["name"]} выкинул {data["value"]}'
