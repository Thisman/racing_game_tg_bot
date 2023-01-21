from modules.player import Player
from modules.game import Game
from modules.commands import RULES_COMMAND, \
    HELP_COMMAND, INFO_COMMAND, REGISTER_PLAYER_COMMAND, \
    REGISTER_GAME_COMMAND

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
1. В игру могут играть как несколько игроков, так и один
2. Перед началом "заезда" игроки выбирают участника
3. После начинается "заезд", каждый из участников стремится первым прийти к финишу
4. Побеждают те игроки, чей участник пришел первым
5. Несколько участников могут считаться победителями

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
        '''

    @staticmethod
    def render_info_tpl(player: Player | None, game: Game | None):
        return f'''
{GameRenderer.render_info_tpl(game)}{PlayerRenderer.render_info_tpl(player)}
        '''

    @staticmethod
    def render_error_tpl(error: str):
        return f'<i>{error}</i>'
