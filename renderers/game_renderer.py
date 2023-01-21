import emoji

from modules.game import Game, GameHorse
from modules.player import Player
from modules.commands import START_GAME_COMMAND, \
    STOP_GAME_COMMAND, JOIN_GAME_COMMAND, LEAVE_GAME_COMMAND

ICONS = [
    emoji.emojize(":cat:", language='alias'),
    emoji.emojize(":hamster:", language='alias'),
    emoji.emojize(":horse:", language='alias'),
    emoji.emojize(":wolf:", language='alias'),
    emoji.emojize(":sheep:", language='alias')
]

class GameRenderer:
    @staticmethod
    def render_register_success_tpl():
        return f'''
Создана новая игра!

Чтобы поставить ставку, выполните одну из команд ниже
/{JOIN_GAME_COMMAND}_0 - поставить на {GameRenderer.render_horse_icon(0)}
/{JOIN_GAME_COMMAND}_1 - поставить на {GameRenderer.render_horse_icon(1)}
/{JOIN_GAME_COMMAND}_2 - поставить на {GameRenderer.render_horse_icon(2)}
/{JOIN_GAME_COMMAND}_3 - поставить на {GameRenderer.render_horse_icon(3)}
/{JOIN_GAME_COMMAND}_4 - поставить на {GameRenderer.render_horse_icon(4)}

Чтобы покинуть игру, выполните команду /{LEAVE_GAME_COMMAND}
Чтобы начать игру, выполните команду /{START_GAME_COMMAND}
Чтобы закончить игру, выполните команду /{STOP_GAME_COMMAND}
        '''

    @staticmethod
    def render_info_tpl(game: Game | None):
        if (game is None or game.is_finished()):
            return '''
Нет активной игры
            '''
        else:
            players_len = len(game.get_participators())
            return f'''
Есть активная игра, кол-во игроков {players_len}
Банк игры {players_len * 10}
            '''

    @staticmethod
    def render_player_join_success_tpl(player: Player, horse_id: int):
        return f'<i>Игрок {player.get_name()} поставил на участника {GameRenderer.render_horse_icon(horse_id)}!</i>'

    @staticmethod
    def render_player_leave_success__plt(player: Player):
        return f'<i>Игрок {player.get_name()} покинул игру</i>'

    @staticmethod
    def render_stop_tpl():
        return '<i>Игра удалена!</i>'

    @staticmethod
    def render_game_start_tpl(round: list[GameHorse]):
        return f'''
Гонкa началaсь!

·············································{emoji.emojize(':crown:', language='alias')}
{GameRenderer.render_horse_tpl(round[0])}
{GameRenderer.render_horse_tpl(round[1])}
{GameRenderer.render_horse_tpl(round[2])}
{GameRenderer.render_horse_tpl(round[3])}
{GameRenderer.render_horse_tpl(round[4])}
·············································{emoji.emojize(':crown:', language='alias')}
        '''

    @staticmethod
    def render_game_round_tpl(round: list[GameHorse]):
        return f'''
Впереди: {GameRenderer.render_leader_list_tpl(round)}

·············································{emoji.emojize(':crown:', language='alias')}
{GameRenderer.render_horse_tpl(round[0])}
{GameRenderer.render_horse_tpl(round[1])}
{GameRenderer.render_horse_tpl(round[2])}
{GameRenderer.render_horse_tpl(round[3])}
{GameRenderer.render_horse_tpl(round[4])}
·············································{emoji.emojize(':crown:', language='alias')}
        '''

    @staticmethod
    def render_game_end_tpl(round: list[GameHorse], winners: list[Player]):
        return f'''
Победили: {GameRenderer.render_leader_list_tpl(round)}

·············································{emoji.emojize(':crown:', language='alias')}
{GameRenderer.render_horse_tpl(round[0])}
{GameRenderer.render_horse_tpl(round[1])}
{GameRenderer.render_horse_tpl(round[2])}
{GameRenderer.render_horse_tpl(round[3])}
{GameRenderer.render_horse_tpl(round[4])}
·············································{emoji.emojize(':crown:', language='alias')}
        '''

    @staticmethod
    def render_horse_icon(id) -> str:
        return ICONS[id]

    @staticmethod
    def render_horse_tpl(horse: GameHorse):
        return f'''{'·' * horse['distance']}{GameRenderer.render_horse_icon(horse['id'])}'''

    @staticmethod
    def render_leader_list_tpl(round: list[GameHorse]):
        max_ditance = sorted(round, key=lambda horse: horse['distance'], reverse=True)[0]['distance']
        leaders = list(filter(lambda horse: horse['distance'] == max_ditance, round))
        return ' '.join(map(lambda horse: GameRenderer.render_horse_icon(horse['id']), leaders))
