from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start']) # message_handler - метод обработчика сообщений
async def process_start_command(message: types.Message): # аннотация явно указывает тип параметра message
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")