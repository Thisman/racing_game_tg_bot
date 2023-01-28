import emoji

from modules.game import Game, GameTrack
from modules.player import Player
from modules.commands import START_GAME_COMMAND, \
    STOP_GAME_COMMAND, JOIN_GAME_COMMAND, LEAVE_GAME_COMMAND

ICONS = [
    emoji.emojize(":snail:", language='alias'),
    emoji.emojize(":rat:", language='alias'),
    emoji.emojize(":rooster:", language='alias'),
    emoji.emojize(":wolf:", language='alias'),
    emoji.emojize(":pig:", language='alias')
]

class GameRenderer:
    @staticmethod
    def render_register_success_tpl():
        return f'''
Создана новая игра!

Чтобы войти в игру, выполните одну из команд ниже
/{JOIN_GAME_COMMAND}_0 - поставить на {GameRenderer.render_track_icon(0)}
/{JOIN_GAME_COMMAND}_1 - поставить на {GameRenderer.render_track_icon(1)}
/{JOIN_GAME_COMMAND}_2 - поставить на {GameRenderer.render_track_icon(2)}
/{JOIN_GAME_COMMAND}_3 - поставить на {GameRenderer.render_track_icon(3)}
/{JOIN_GAME_COMMAND}_4 - поставить на {GameRenderer.render_track_icon(4)}

/{LEAVE_GAME_COMMAND} - покинуть игру
/{START_GAME_COMMAND} - начать игру
/{STOP_GAME_COMMAND}  - остановить и удалить игру
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
Есть активная игра, кол-во игроков: {players_len}
            '''

    @staticmethod
    def render_player_join_success_tpl(player: Player, track_id: int):
        return f'<i>Игрок {player.get_name()} поставил на участника {GameRenderer.render_track_icon(track_id)}</i>'

    @staticmethod
    def render_player_leave_success__plt(player: Player):
        return f'<i>Игрок {player.get_name()} покинул игру</i>'

    @staticmethod
    def render_stop_tpl():
        return '<i>Игра удалена!</i>'

    @staticmethod
    def render_game_start_tpl(round: list[GameTrack]):
        return f'''
Гонкa началaсь!

·············································{emoji.emojize(':crown:', language='alias')}
{GameRenderer.render_track_tpl(round[0])}
{GameRenderer.render_track_tpl(round[1])}
{GameRenderer.render_track_tpl(round[2])}
{GameRenderer.render_track_tpl(round[3])}
{GameRenderer.render_track_tpl(round[4])}
·············································{emoji.emojize(':crown:', language='alias')}
        '''

    @staticmethod
    def render_game_round_tpl(round: list[GameTrack]):
        return f'''
Впереди: {GameRenderer.render_leader_list_tpl(round)}

·············································{emoji.emojize(':crown:', language='alias')}
{GameRenderer.render_track_tpl(round[0])}
{GameRenderer.render_track_tpl(round[1])}
{GameRenderer.render_track_tpl(round[2])}
{GameRenderer.render_track_tpl(round[3])}
{GameRenderer.render_track_tpl(round[4])}
·············································{emoji.emojize(':crown:', language='alias')}
        '''

    @staticmethod
    def render_game_end_tpl(round: list[GameTrack], winners: list[Player]):
        return f'''
Победили: {GameRenderer.render_leader_list_tpl(round)}

·············································{emoji.emojize(':crown:', language='alias')}
{GameRenderer.render_track_tpl(round[0])}
{GameRenderer.render_track_tpl(round[1])}
{GameRenderer.render_track_tpl(round[2])}
{GameRenderer.render_track_tpl(round[3])}
{GameRenderer.render_track_tpl(round[4])}
·············································{emoji.emojize(':crown:', language='alias')}
        '''

    @staticmethod
    def render_track_icon(id) -> str:
        return ICONS[id]

    @staticmethod
    def render_track_tpl(track: GameTrack):
        return f'''{'·' * track['distance']}{GameRenderer.render_track_icon(track['id'])}'''

    @staticmethod
    def render_leader_list_tpl(round: list[GameTrack]):
        max_ditance = sorted(round, key=lambda track: track['distance'], reverse=True)[0]['distance']
        leaders = list(filter(lambda track: track['distance'] == max_ditance, round))
        return ' '.join(map(lambda track: GameRenderer.render_track_icon(track['id']), leaders))
