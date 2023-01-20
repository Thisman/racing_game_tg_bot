from modules.player import Player

class PlayerRenderer:
    @staticmethod
    def render_register_success_tpl(player: Player):
        return f'<i>Зарегистрирован новый игрок {player.get_name()}!</i>'

    @staticmethod
    def render_info_tpl(player: Player | None):
        if (player is None):
            return ''
        else:
            return f'''
Текущий банк игрока {player.get_name()}: {player.get_bank()}
            '''
