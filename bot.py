import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import sort_data, get_data
import os
import asyncio

bot = Bot(token='Token', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['MDK']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите группу', reply_markup=keyboard)


@dp.message_handler(Text(equals='MDK'))
async def get_memes(message: types.Message):
    await message.answer('Мемы загружаются...')

    get_data()
    sort_data()

    with open('top_posts.json', encoding='utf-8') as file:
        data = json.load(file)

    for i in data:
        card = f'{hlink(i.get("Текст"),i.get("Ссылка"))}\n' \
        f'{hbold("Дата: ")}{i.get("Дата")}\n' \
        f'{hbold("Лайки: ")}{i.get("Лайки")}\n'

        await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()