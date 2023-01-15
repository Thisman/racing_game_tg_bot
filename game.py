"""
_id: number
chat_id: number
creator: number
time_create: date
players: number[]
status: active | process | finished
result: string
"""

from datetime import datetime

from db import games_collection

def create_game(id, chat_id):
    if (chat_id > 0):
        return [False, 'Нельзя создать игру не в чате!']

    try:
        active_game_in_chat = games_collection.find_one({ 'chat_id': chat_id, 'status': { '$in': ['active', 'process'] } })
        if (active_game_in_chat is not None):
            return [False, 'В чате уже есть активная игра! Закончите ее командой /stop']

        games_collection.insert_one({
            'chat_id': chat_id,
            'creator': id,
            'time_create': datetime.now(),
            'players': [id],
            'status': 'active',
            'result': '',
        })
        return [True, None]
    except:
        return [False, 'Неизвестная ошибка!']

def join_to_game():
    return

def leave_from_game():
    return

def spin_in_game():
    return

def end_game(id, chat_id):
    try:
        active_game_in_chat = games_collection.find_one({ 'chat_id': chat_id, 'status': { '$in': ['active', 'process'] } })
        if (active_game_in_chat is None):
            return [False, 'Нет ни одной активной игры в чате!']

        if (active_game_in_chat['creator'] != id):
            return [False, 'Вы не можете остановить игру, в которой не являетесь создателем!']

        games_collection.update_one({ 'chat_id': chat_id }, {
            '$set': {
                'status': 'finished'
            }
        })
        return [True, None]
    except:
        return [False, 'Неизвестная ошибка!']
