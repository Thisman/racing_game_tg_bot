from modules.game import Game
from modules.player import Player
from modules.commands import START_GAME_COMMAND, \
    STOP_GAME_COMMAND, JOIN_GAME_COMMAND

class GameRenderer:
    @staticmethod
    def render_register_success_tpl():
        return f'''
Создана новая игра!

/{JOIN_GAME_COMMAND} - Войти в игру
/{START_GAME_COMMAND} - Начать игру
/{STOP_GAME_COMMAND} - Закончить игру
        '''

    @staticmethod
    def render_info_tpl(game: Game | None):
        if (game is None or game.is_finished()):
            return '''
Нет активной игры
            '''
        else:
            players_len = len(game.get_players())
            return f'''
Есть активная игра, кол-во игроков {players_len}
Банк игры {players_len * 10}
            '''

    @staticmethod
    def render_player_join_success_tpl(player: Player):
        return f'<i>Игрок {player.get_name()} вошел в игру!</i>'

    @staticmethod
    def render_player_leave_success__plt(player: Player):
        return f'<i>Игрок {player.get_name()} покинул игру</i>'

    @staticmethod
    def render_stop_tpl():
        return '<i>Игра закончилась!</i>'
