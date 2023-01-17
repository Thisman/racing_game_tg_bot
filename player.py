from aiogram import types

from db import players_collection
from error import GameError, ERROR_PLAYER_ALREADY_EXIST, ERROR_PLAYER_NOT_EXIST

class PlayerData:
    id: int
    name: str
    bank: int

def register_player(user: types.User) -> None:
    existing_player = players_collection.find_one({ 'id': user.id })
    if (existing_player is not None):
        raise GameError(ERROR_PLAYER_ALREADY_EXIST)

    players_collection.insert_one({
        'id': user.id,
        'name': user.full_name,
        'bank': 100,
    })

def get_player(id) -> PlayerData:
    player = players_collection.find_one({ 'id': id })
    if (player is None):
        raise GameError(ERROR_PLAYER_NOT_EXIST)
    
    return player

def update_player(player: PlayerData, data):
    players_collection.update_one({ 'id': player['id'] }, {
        '$set': data,
    })
