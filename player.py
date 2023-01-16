"""
_id: number
id: number
name: string
bank: number
"""

from aiogram import types

from db import players_collection

def register_player(player: types.User):
    existing_player = players_collection.find_one({ 'id': player.id })
    if (existing_player is not None):
        return [False, 'Игрок уже существует!']

    players_collection.insert_one({
        'id': player.id,
        'name': player.full_name,
        'bank': 100,
    })
    return [True, None]

def get_player(id):
    existing_player = players_collection.find_one({ 'id': id })
    if (existing_player is None):
        return [None, 'Ошибка! Игрока не существует']

    return [existing_player, None]
