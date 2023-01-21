import random
from datetime import datetime

from modules.player import Player
from modules.db import games_collection
from modules.error import GameError, ERROR_GAME_ALREADY_EXIST, \
    ERROR_REGISTER_GAME

GAME_READY_STATUS = 'ready'
GAME_STARTED_STATUS = 'started'
GAME_FINISHED_STATUS = 'finished'

GAME_CIRCLE_MIN_HORSE_STEP = 2
GAME_CIRCLE_MAX_HORSE_STEP = 8
GAME_CIRCLE_FINISH = 45

class GameData:
    chat_id: int
    participators: list[tuple[int, int]]
    status: str
    time_create: datetime
    result: str

class GameHorse:
    id: int
    distance: int
    is_winnner: bool

class Game:
    @staticmethod
    def register(chat_id: int):
        exisiting_game = Game.load(chat_id)
        if (exisiting_game is not None and exisiting_game.is_finished() is False):
            raise GameError(ERROR_GAME_ALREADY_EXIST)

        games_collection.insert_one({
            'chat_id': chat_id,
            'time_create': datetime.now(),
            'participators': [],
            'status': GAME_READY_STATUS,
        })

        game = Game.load(chat_id)

        if (game is not None):
            return game
        else:
            raise GameError(ERROR_REGISTER_GAME)

    @staticmethod
    def load(chat_id: int):
        games = list(games_collection.find({ 'chat_id': chat_id }).sort('time_create', -1).limit(1))
        if (len(games) == 0 or games[0] is None):
            return None
        else:
            return Game(games[0])

    @staticmethod
    def get_stared_game(chat_id: int):
        game = Game.load(chat_id)
        if (game is None or game.is_started() is False):
            return None
        else:
            return game

    def __init__(self, data: GameData):
        self.data = data
        self.games_collection = games_collection
        self.current = 0
        self.horses: list[GameHorse] = [
            { 'distance': 0, 'is_winner': False, 'id': 0 },
            { 'distance': 0, 'is_winner': False, 'id': 1  },
            { 'distance': 0, 'is_winner': False, 'id': 2  },
            { 'distance': 0, 'is_winner': False, 'id': 3  },
            { 'distance': 0, 'is_winner': False, 'id': 4  },
        ]

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

    def get_id(self) -> str:
        return self.data['_id']

    def is_player_in_game(self, player: Player) -> bool:
        for data in self.get_participators():
            if (player.get_id() == data[0]):
                return True

        return False

    def get_participators(self) -> list[tuple[int, int]]:
        return self.data['participators']

    def get_horses(self) -> list[GameHorse]:
        return self.horses

    def get_winner_horses(self) -> list[GameHorse]:
        return list(filter(lambda horse: horse['is_winner'] is True, self.get_horses()))

    def join(self, player: Player, horse: int):
        self.data['participators'] += [(player.get_id(), horse)]

    def leave(self, player: Player):
        self.data['participators'] = list(filter(lambda data: data[0] != player.get_id(), self.get_participators()))

    def start(self):
        self.data['status'] = GAME_STARTED_STATUS

        def rounds():
            while(len(self.get_winner_horses()) == 0):
                self.__next_round()
                yield self.horses

            return self.horses

        return rounds

    def stop(self) -> bool:
        self.data['status'] = GAME_FINISHED_STATUS

    def __next_round(self):
        for horse in self.horses:
            horse['distance'] += random.randint(
                GAME_CIRCLE_MIN_HORSE_STEP,
                GAME_CIRCLE_MAX_HORSE_STEP
            )
            if (horse['distance'] > GAME_CIRCLE_FINISH):
                horse['is_winner'] = True


def check_started_game_in_chat(chat_id: int) -> bool:
    game = Game.load(chat_id)
    return game is not None and game.is_started()
