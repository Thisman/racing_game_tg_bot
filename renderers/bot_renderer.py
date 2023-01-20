from modules.player import Player
from modules.game import Game
from modules.commands import RULES_COMMAND, \
    HELP_COMMAND, INFO_COMMAND, REGISTER_PLAYER_COMMAND, \
    REGISTER_GAME_COMMAND, JOIN_GAME_COMMAND, \
    LEAVE_GAME_COMMAND, START_GAME_COMMAND, \
    STOP_GAME_COMMAND

from renderers.game_renderer import GameRenderer
from renderers.player_renderer import PlayerRenderer

class BotRenderer:
    @staticmethod
    def render_start_tpl():
        return f'''
Бот для проведения простой игры
/{RULES_COMMAND} - Правила
/{HELP_COMMAND} - Список команд
/{INFO_COMMAND} - Информация об игроке и статусе игры

Автор: @tablescable
Ссылка на проект: https://github.com/Thisman/spin_game_tg_bot
        '''

    @staticmethod
    def render_rules_tpl():
        return f'''
<b>Правила</b>:
1. Каждому участнику случайно выбирается число
2. Побеждают те участники, которые получили большее число
3. Стоимость игры 10 баллов
4. Приз - общий банк поделенный между всеми победителями

Доступные команды /{HELP_COMMAND}
        '''

    @staticmethod
    def render_help_tpl():
        return f'''
<b>Основные команды</b>
/{RULES_COMMAND} - Правила
/{HELP_COMMAND} - Список команд
/{INFO_COMMAND} - Информация о банке игрока и статусе игры

/{REGISTER_PLAYER_COMMAND} - Зарегистрировать игрока

/{REGISTER_GAME_COMMAND} - Создать новую игру
/{JOIN_GAME_COMMAND} - Вступить в игру
/{LEAVE_GAME_COMMAND} - Покинуть игру
/{START_GAME_COMMAND} - Запустить игру
/{STOP_GAME_COMMAND} - Остановить и удалить игру
        '''

    @staticmethod
    def render_info_tpl(player: Player | None, game: Game | None):
        return f'''
{GameRenderer.render_info_tpl(game)}{PlayerRenderer.render_info_tpl(player)}
        '''

    @staticmethod
    def render_error_tpl(error: str):
        return f'<i>{error}</i>'
