"""
_id: number
id: number
bank: number
"""

from db import players_collection

def register_player(id):
    existing_player = players_collection.find_one({ 'id': id })
    if (existing_player is not None):
        return [False, 'Игрок уже существует!']

    players_collection.insert_one({
        'id': id,
        'bank': 100,
    })
    return [True, None]

def get_player(id):
    existing_player = players_collection.find_one({ 'id': id })
    if (existing_player is None):
        return [None, 'Ошибка! Игрока не существует']

    return [existing_player, None]
