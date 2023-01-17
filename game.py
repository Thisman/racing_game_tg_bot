import random
from datetime import datetime

from db import games_collection
from player import PlayerData, get_player, update_player
from error import GameError, ERROR_COMMAND_NOT_IN_CHAT, \
    ERROR_GAME_ALREADY_EXIST, ERROR_GAME_NOT_EXIST, ERROR_PLAYER_ALREADY_IN_GAME, \
    ERROR_PLAYER_NOT_IN_GAME, ERROR_GAME_NOT_ENOUGH_PLAYERS

class GameResult:
    player: PlayerData
    is_winner: bool
    value: int

class GameData:
    chat_id: int
    creator: int
    players: list[int]
    status: str
    result: list[GameResult]
    time_create: datetime


def check_is_command_valid(chat_id: int):
    if (chat_id > 0):
        raise GameError(ERROR_COMMAND_NOT_IN_CHAT)

def create_new_game(creator: PlayerData, chat_id: int):
    games_collection.insert_one({
        'chat_id': chat_id,
        'creator': creator['id'],
        'time_create': datetime.now(),
        'players': [creator['id']],
        'status': 'active',
        'result': '',
    })

def update_game(game_id: int, data):
    games_collection.update_one({ '_id': game_id }, {
        '$set': data,
    })

def get_active_game(chat_id: int) -> GameData | None:
    return games_collection.find_one({ 'chat_id': chat_id, 'status': 'active' })

def get_game_result(game: GameData) -> list[GameResult]:
    results: list[GameResult] = []
    for id in game['players']:
        player = get_player(id)
        results.append({ 'player': player, 'value': random.randint(0, 10), 'is_winner': False })

    results.sort(key=lambda player: player['value'], reverse=True)
    winner = results[0]
    for result in results:
        if (result['value'] == winner['value']):
            result['is_winner'] = True

    return results


def command_create_game(player: PlayerData, chat_id: int):
    check_is_command_valid(chat_id)

    game = get_active_game(chat_id)
    if (game is not None):
        raise GameError(ERROR_GAME_ALREADY_EXIST)
    
    create_new_game(player, chat_id)

def command_join_to_game(player: PlayerData, chat_id: int):
    check_is_command_valid(chat_id)

    game = get_active_game(chat_id)
    if (game is None):
        raise GameError(ERROR_GAME_NOT_EXIST)

    if(player['id'] in game['players']):
        raise GameError(ERROR_PLAYER_ALREADY_IN_GAME)
    
    update_game(game['_id'], {
        'players': game['players'] + [player['id']]
    })


def command_leave_from_game(player: PlayerData, chat_id: int):
    check_is_command_valid(chat_id)

    game = get_active_game(chat_id)
    if (game is None):
        raise GameError(ERROR_GAME_NOT_EXIST)

    if(player['id'] not in game['players']):
        raise GameError(ERROR_PLAYER_NOT_IN_GAME)

    update_game(game['_id'], {
        'players': list(filter(lambda id: id != player['id'], game['players']))
    })

def command_spin_in_game(player: PlayerData, chat_id: int) -> list[GameResult]:
    check_is_command_valid(chat_id)

    game = get_active_game(chat_id)
    if (game is None):
        raise GameError(ERROR_GAME_NOT_EXIST)

    if(player['id'] not in game['players']):
        raise GameError(ERROR_PLAYER_NOT_IN_GAME)

    if (len(game['players']) <= 1):
        raise GameError(ERROR_GAME_NOT_ENOUGH_PLAYERS)

    update_game(game['_id'], {
        'status': 'process'
    })

    game_results = get_game_result(game)
    winners_len = len(list(filter(lambda data: data['is_winner'], game_results)))
    for result in game_results:
        player = result['player']
        if (result['is_winner']):
            update_player(player, {
                'bank': player['bank'] + round((10 * (len(game_results) - 1)) / winners_len)
            })
        else:
            update_player(player, {
                'bank': player['bank'] - 10
            })

    update_game(game['_id'], {
        'status': 'finished',
        'result': game_results,
    })

    return game_results

def command_end_game(player: PlayerData, chat_id: int):
    check_is_command_valid(chat_id)

    game = get_active_game(chat_id)
    if (game is None):
        raise GameError(ERROR_GAME_NOT_EXIST)

    update_game(game['_id'], {
        'status': 'finished'
    })
