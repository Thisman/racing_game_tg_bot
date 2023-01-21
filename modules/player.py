from aiogram import types

from modules.db import players_collection
from modules.error import GameError, ERROR_PLAYER_ALREADY_EXIST, \
    ERROR_REGISTER_PLAYER

class PlayerData:
    name: str
    id: int
    bank: int

class Player:
    @staticmethod
    def register(user: types.User):
        existing_player = Player.load(user.id)
        if (existing_player is not None):
            raise GameError(ERROR_PLAYER_ALREADY_EXIST)

        players_collection.insert_one({
            'id': user.id,
            'name': user.full_name,
            'bank': 100,
        })

        player = Player.load(user.id)

        if (player is not None):
            return player
        else:
            raise GameError(ERROR_REGISTER_PLAYER)

    @staticmethod
    def load(user_id: int):
        data = players_collection.find_one({ 'id': user_id })
        if (data is None):
            return None
        else:
            return Player(data)


    def __init__(self, data: PlayerData):
        self.data = data
        self.players_collection = players_collection
    
    def save(self):
        id = self.data['id']
        self.players_collection.update_one({ 'id': id }, {
            '$set': self.data,
        })

    def get_id(self) -> int:
        return self.data['id']

    def get_name(self) -> str:
        return self.data['name']

    def get_bank(self) -> int:
        return self.data['bank']

    def set_bank(self, bank: int) -> str:
        self.data['bank'] = bank

    def is_enough_bank(self) -> bool:
        return self.data['bank'] > 0
