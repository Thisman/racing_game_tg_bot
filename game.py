"""
_id: number
chat_id: number
creator: number
time_create: date
players: number[]
status: active | process | finished
result: string
"""

import random
from datetime import datetime

from db import games_collection
from player import get_player

def create_game(id, chat_id):
    if (chat_id > 0):
        return [False, 'Нельзя создать игру не в чате!']

    active_game_in_chat = games_collection.find_one({ 'chat_id': chat_id, 'status': { '$in': ['active', 'process'] } })
    if (active_game_in_chat is not None):
        return [False, 'В чате уже есть активная игра! Закончите ее командой /stop']
    
    [existing_player, _] = get_player(id)
    if (existing_player is None):
        return [False, 'Нельзя создать игру не зарегистрированному игроку. Для регистрации введите команду /register']

    games_collection.insert_one({
        'chat_id': chat_id,
        'creator': id,
        'time_create': datetime.now(),
        'players': [id],
        'status': 'active',
        'result': '',
    })
    return [True, None]

def join_to_game(id, chat_id):
    if (chat_id > 0):
        return [False, 'Нельзя входить в игру не в чате!']


    active_game_in_chat = games_collection.find_one({ 'chat_id': chat_id, 'status': 'active' })
    if (active_game_in_chat is None):
        return [False, 'Нет активной игры! Чтобы начать игру вызовите команду /create']

    if(id in active_game_in_chat['players']):
        return [False, 'Игрок уже в игре!']
    
    games_collection.update_one({ '_id': active_game_in_chat['_id'] }, {
        '$set': {
            'players': active_game_in_chat['players'] + [id]
        }
    })
    return [True, None]

def leave_from_game(id, chat_id):
    if (chat_id > 0):
        return [False, 'Нельзя покидать игру не в чате!']

    active_game_in_chat = games_collection.find_one({ 'chat_id': chat_id, 'status': 'active' })
    if (active_game_in_chat is None):
        return [False, 'Нет активной игры! Чтобы начать игру вызовите команду /create']

    if(id not in active_game_in_chat['players']):
        return [False, 'Игрок уже не в игре!']
    
    games_collection.update_one({ '_id': active_game_in_chat['_id'] }, {
        '$set': {
            'players': list(filter(lambda player: player != id, active_game_in_chat['players']))
        }
    })
    return [True, None]

def spin_in_game(id, chat_id):
    active_game_in_chat = games_collection.find_one({ 'chat_id': chat_id, 'status': 'active' })
    if (active_game_in_chat is None):
        return [False, 'Нет ни одной активной игры в чате!']

    # if (len(active_game_in_chat['players']) <= 1):
    #     return [False, 'Нельзя начать игру, когда в ней один или меньше игроков!']

    games_collection.update_one({ '_id': active_game_in_chat['_id'] }, {
        '$set': {
            'status': 'process'
        }
    })

    results = []
    for id in active_game_in_chat['players']:
        [player, _] = get_player(id)
        if (player is not None):
            results.append({ 'player': player['name'], 'result': random.randint(0, 10) })

    results.sort(key=lambda player: player['result'], reverse=True)
    result_table = '\n'.join(map(lambda result: f'Игрок: {result["player"]} - {result["result"]}', results))
    result_str = f'''
Результаты:
{result_table}
    '''

    games_collection.update_one({ '_id': active_game_in_chat['_id'] }, {
        '$set': {
            'status': 'finished',
            'result': result_str,
        }
    })
    return [result_str, None]

def end_game(id, chat_id):
    active_game_in_chat = games_collection.find_one({ 'chat_id': chat_id, 'status': 'active' })
    if (active_game_in_chat is None):
        return [False, 'Нет ни одной активной игры в чате!']

    if (active_game_in_chat['creator'] != id):
        return [False, 'Вы не можете остановить игру, в которой не являетесь создателем!']

    games_collection.update_one({ '_id': active_game_in_chat['_id'] }, {
        '$set': {
            'status': 'finished'
        }
    })
    return [True, None]
