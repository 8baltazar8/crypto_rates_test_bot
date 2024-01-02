#!/usr/bin/python

import asyncio
import aiohttp
import os
import req
from dotenv import load_dotenv
from telebot import asyncio_filters
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from db_create import create_db
from utils.db_utils import insert_user, select_all, check_user_exsists
load_dotenv()

bot = AsyncTeleBot(os.getenv('BOT_TOKEN'), state_storage=StateMemoryStorage())


class MyStates(StatesGroup):
    num = State()
    is_logged_in = State()


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, "Hi there")


@bot.message_handler(commands=['lol'])
async def send_lol(message):
    lol = await req.get_crypto_rates()
    await bot.reply_to(message, f"{lol['ethereum']['usd']}")


@bot.message_handler(state="*", commands=['cancel'])
async def any_state(message):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, "Cancelled.")
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['reg'])
async def lol(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    item1 = types.KeyboardButton('Share my contact', request_contact=True)
    markup.add(item1)
    await bot.set_state(message.from_user.id, MyStates.num, message.chat.id)
    await bot.send_message(message.chat.id, 'HEY', reply_markup=markup)


@bot.message_handler(state=MyStates.num, content_types=['contact'])
async def num(message):
    remove_markup = types.ReplyKeyboardRemove()
    user_info = {'id': message.from_user.id,
                 'username': message.from_user.username,
                 'first_name': message.from_user.first_name,
                 'last_name': message.from_user.last_name,
                 'phone_number': message.contact.phone_number}
    check_user = check_user_exsists(*user_info.values())
    if len(check_user) > 1:
        await bot.send_message(message.chat.id, 'Something went wrong', reply_markup=remove_markup)
    elif len(check_user) == 1 and check_user[0][-1] == 0:
        await bot.send_message(message.chat.id, 'You are logged in', reply_markup=remove_markup)
        await bot.set_state(message.from_user.id, MyStates.is_logged_in, message.chat.id)
    elif len(check_user) == 1 and check_user[0][-1] == 1:
        await bot.send_message(message.chat.id, 'Your account has been deleted by the admin', reply_markup=remove_markup)
    else:
        await insert_user(*user_info.values())
        await bot.set_state(message.from_user.id, MyStates.is_logged_in, message.chat.id)
        await bot.send_message(message.chat.id, 'You have successfully registered', reply_markup=remove_markup)
    # select_all()

create_db()
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
asyncio.run(bot.polling())
