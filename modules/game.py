import random
from datetime import datetime

from modules.player import Player
from modules.db import games_collection
from modules.error import GameError, ERROR_GAME_ALREADY_EXIST, \
    ERROR_REGISTER_GAME, ERROR_READY_GAME_NOT_EXIST, ERROR_GAME_NOT_ENOUGH_PLAYERS, \
    ERROR_PLAYER_NOT_IN_GAME, ERROR_PLAYER_ALREADY_IN_GAME, ERROR_NOT_ENOUGH_PLAYER_BANK

GAME_READY_STATUS = 'ready'
GAME_STARTED_STATUS = 'started'
GAME_FINISHED_STATUS = 'finished'

GAME_CIRCLE_MIN_HORSE_STEP = 2
GAME_CIRCLE_MAX_HORSE_STEP = 8
GAME_CIRCLE_FINISH = 45

class GameData:
    status: str
    result: str
    chat_id: int
    time_create: datetime
    players: list[tuple[int, int]]

class GameTrack:
    id: int
    distance: int
    is_winnner: bool

class Game:
    @staticmethod
    def register(chat_id: int):
        last_game = Game.load_last(chat_id)
        if (last_game is not None and last_game.is_finished() is False):
            raise GameError(ERROR_GAME_ALREADY_EXIST)

        games_collection.insert_one({
            'players': [],
            'chat_id': chat_id,
            'status': GAME_READY_STATUS,
            'time_create': datetime.now(),
        })

        game = Game.load_last(chat_id)

        if (game is not None):
            return game
        else:
            raise GameError(ERROR_REGISTER_GAME)

    @staticmethod
    def load_last(chat_id: int):
        games = list(games_collection.find({ 'chat_id': chat_id }).sort('time_create', -1).limit(1))
        if (len(games) == 0 or games[0] is None):
            return None
        else:
            return Game(games[0])

    @staticmethod
    def load_last_or_error(chat_id: int):
        last_game = Game.load_last(chat_id)
        if (last_game is None):
            raise GameError(ERROR_READY_GAME_NOT_EXIST)
        else:
            return last_game

    @staticmethod
    def load_stared_game(chat_id: int):
        game = Game.load_last(chat_id)
        if (game is None or game.is_started() is False):
            return None
        else:
            return game


    def __init__(self, data: GameData):
        self.data = data
        self.games_collection = games_collection
        self.tracks: list[GameTrack] = [
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
        for data in self.get_players():
            if (player.get_id() == data[0]):
                return True

        return False

    def get_players(self) -> list[tuple[int, int]]:
        return self.data['players']

    def get_tracks(self) -> list[GameTrack]:
        return self.tracks

    def get_winner_tracks(self) -> list[GameTrack]:
        return list(filter(lambda horse: horse['is_winner'] is True, self.get_tracks()))

    def join(self, player: Player, track: int):
        if (self.is_ready() is False):
            raise GameError(ERROR_READY_GAME_NOT_EXIST)

        if (self.is_player_in_game(player) is True):
            raise GameError(ERROR_PLAYER_ALREADY_IN_GAME)

        if (player.is_enough_bank() is False):
            raise GameError(ERROR_NOT_ENOUGH_PLAYER_BANK)

        self.data['players'] += [(player.get_id(), track)]

    def leave(self, player: Player):
        if (self.is_ready() is False):
            raise GameError(ERROR_READY_GAME_NOT_EXIST)

        if (self.is_player_in_game(player) is False):
            raise GameError(ERROR_PLAYER_NOT_IN_GAME)

        self.data['players'] = list(filter(lambda data: data[0] != player.get_id(), self.get_players()))

    def start(self):
        if (self.is_ready() is False):
            raise GameError(ERROR_READY_GAME_NOT_EXIST)

        if (len(self.get_players()) == 0):
            raise GameError(ERROR_GAME_NOT_ENOUGH_PLAYERS)

        self.data['status'] = GAME_STARTED_STATUS

        def rounds():
            while(len(self.get_winner_tracks()) == 0):
                self.__next_round()
                yield self.tracks

            return self.tracks

        return rounds

    def stop(self):
        if (self.is_finished() is True):
            raise GameError(ERROR_READY_GAME_NOT_EXIST)

        self.data['status'] = GAME_FINISHED_STATUS

    def __next_round(self):
        for track in self.tracks:
            track['distance'] += random.randint(
                GAME_CIRCLE_MIN_HORSE_STEP,
                GAME_CIRCLE_MAX_HORSE_STEP
            )
            if (track['distance'] > GAME_CIRCLE_FINISH):
                track['is_winner'] = True
