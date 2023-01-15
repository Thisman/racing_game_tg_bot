import sys
import hashlib

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

from player import register_player
from game import create_game, end_game

if(len(sys.argv) == 1):
    print('Не передан токен для авторизации')
    exit(1)

API_TOKEN = sys.argv[1]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('<i>Написать приветственный текст</i>')

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply('''
Основные команды
/info - информация о боте

/register - создать игрока
/create - создать новую игру
/join - вступить в активную игру
/leave - покинуть активную игру
/spin - запустить игру
/stop - удалить активную игру
    ''')

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await message.reply(
        '<i>Написать информацию о боте</i>',
        parse_mode=types.ParseMode.HTML
    )


@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    [is_success, error] = register_player(message.from_user.id)
    if (is_success is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            f'<i>Зарегистрирован новый игрок {message.from_user.full_name}</i>',
            parse_mode=types.ParseMode.HTML
        )

@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    [is_success, error] = create_game(message.from_user.id, message.chat.id)
    if (is_success is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            '<i>Создана новая игра. Для входа используйте команды /join, для окончания /stop</i>',
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    await message.reply(
        '<i>Добавляю игрока в игру</i>',
        parse_mode=types.ParseMode.HTML
    )

@dp.message_handler(commands=['leave'])
async def leave(message: types.Message):
    await message.reply(
        '<i>Исключаю игрока из игры</i>',
        parse_mode=types.ParseMode.HTML
    )

@dp.message_handler(commands=['spin'])
async def spin(message: types.Message):
    await message.reply(
        '<i>Начинаю игру</i>',
        parse_mode=types.ParseMode.HTML
    )

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    [is_success, error] = end_game(message.from_user.id, message.chat.id)
    if (is_success is False):
        await message.reply(
            f'<i>{error}</i>',
            parse_mode=types.ParseMode.HTML
        )
    else:
        await message.reply(
            '<i>Активная игра в чате остановлена</i>',
            parse_mode=types.ParseMode.HTML
        )


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query
    match text:
        case 'register':
            input_content = InputTextMessageContent('/register')
            command = 'Создать нового игрока'
        case 'create':
            input_content = InputTextMessageContent('/create')
            command = 'Создать игру'
        case 'join':
            input_content = InputTextMessageContent('/join')
            command = 'Вступить в игру'
        case 'leave':
            input_content = InputTextMessageContent('/leave')
            command = 'Покинуть игру'
        case 'spin':
            input_content = InputTextMessageContent('/spin')
            command = 'Запустить игру'
        case 'stop':
            input_content = InputTextMessageContent('/stop')
            command = 'Остановить и удалить игру'
        case _:
            input_content = None
            command = ''
    
    if(input_content is None):
        return

    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=command,
        input_message_content=input_content,
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
