from datetime import datetime

from modules.player import Player
from modules.db import games_collection

GAME_READY_STATUS = 'ready'
GAME_STARTED_STATUS = 'started'
GAME_FINISHED_STATUS = 'finished'

class GameData:
    chat_id: int
    players: list[int]
    status: str
    time_create: datetime
    result: str
    creator: int

class Game:
    @staticmethod
    def register(creator: Player, chat_id: int):
        games_collection.insert_one({
            'chat_id': chat_id,
            'creator': creator.get_id(),
            'time_create': datetime.now(),
            'players': [creator.get_id()],
            'status': GAME_READY_STATUS,
            'result': '',
        })

        game = Game.load(chat_id)

        if (game is not None):
            return game
        else:
            return None

    @staticmethod
    def load(chat_id: int):
        games = list(games_collection.find({ 'chat_id': chat_id }).sort('time_create', -1).limit(1))
        if (len(games) == 0 or games[0] is None):
            return None
        else:
            return Game(games[0])


    def __init__(self, data: GameData):
        self.data = data
        self.games_collection = games_collection

    def save(self):
        game_id = self.data['_id']
        self.games_collection.update_one({ '_id': game_id }, {
            '$set': self.data,
        })

    def is_ready(self) -> bool:
        return self.data['status'] == GAME_READY_STATUS
    
    def is_started(self) -> bool:
        return self.data['status'] == GAME_STARTED_STATUS
    
    def is_finished(self) -> bool:
        return self.data['status'] == GAME_FINISHED_STATUS

    def is_player_in_game(self, player: Player) -> bool:
        if(player.get_id() in self.data['players']):
            return True

        return False

    def join(self, player: Player):
        self.data['players'] += [player.get_id()]

    def leave(self, player: Player):
        self.data['players'] = list(filter(lambda id: id != player.get_id(), self.data['players']))

    def get_id(self) -> str:
        return self.data['_id']

    def get_players(self) -> list[int]:
        return self.data['players']

    def start(self) -> bool:
        self.stop()
        return True

    def stop(self) -> bool:
        self.data['status'] = GAME_FINISHED_STATUS


def check_is_chat_dialog(chat_id: int) -> bool:
    return chat_id > 0

def check_started_game_in_chat(chat_id: int) -> bool:
    game = Game.load(chat_id)
    return game is not None and game.is_started()
