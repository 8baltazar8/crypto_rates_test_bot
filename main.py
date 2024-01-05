#!/usr/bin/python
import pprint

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
from utils.db_utils import insert_user, select_all, check_user_exsists, last_user_state, insert_state
load_dotenv()
# apihelper.ENABLE_MIDDLEWARE = True
bot = AsyncTeleBot(os.getenv('BOT_TOKEN'), state_storage=StateMemoryStorage())
calculator_global_var = ''
calculator_dict = {'btcto$': 'bitcoin',
                   'ethto$': 'ethereum',
                   'bnbto$': 'binancecoin',
                   '$tobtc': 'bitcoin',
                   '$toeth': 'ethereum',
                   '$tobnb': 'binancecoin'}


class MyStates(StatesGroup):
    num = State()
    is_logged_in = State()
    num_of_coins = State()
    num_of_d = State()
    logged_out = State()

# SimpleCustomFilter is for boolean values, such as is_admin=True


class IsGood(asyncio_filters.SimpleCustomFilter):
    key = 'is_good'

    @staticmethod
    async def check(message: types.Message):
        try:
            float(message.text)
            return True
        except Exception:
            return False




@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, "Hi there")


@bot.message_handler(state="*", commands=['menu'])
async def logged_menu(message):
    if not message.__dict__['reply_markup']:
        is_logged = await last_user_state(message.from_user.username)
        if is_logged == 'MyStates:is_logged_in':
            await bot.set_state(message.from_user.id, MyStates.is_logged_in, message.chat.id)
            await insert_state(message.from_user.username, await bot.get_state(message.from_user.id, message.chat.id))
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('Rates', callback_data='rates')
            item2 = types.InlineKeyboardButton('Calculator', callback_data='calculator')
            item3 = types.InlineKeyboardButton('Log out', callback_data='log_out')

            markup.row(item1)
            markup.row(item2)
            markup.row(item3)

            await bot.send_message(message.chat.id, 'Choose an option', reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, 'Please log in or register first \nClick /register')
            # await register(message=message)
    else:
        is_logged = await last_user_state(message.json['chat']['username'])
        if is_logged == 'MyStates:is_logged_in':
            await bot.set_state(message.chat.id, MyStates.is_logged_in, message.chat.id)
            await insert_state(message.json['chat']['username'], await bot.get_state(message.chat.id, message.chat.id))
            #select_all()
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('Rates', callback_data='rates')
            item2 = types.InlineKeyboardButton('Calculator', callback_data='calculator')
            item3 = types.InlineKeyboardButton('Log out', callback_data='log_out')

            markup.row(item1)
            markup.row(item2)
            markup.row(item3)

            await bot.send_message(message.chat.id, 'Choose an option', reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, 'Please log in or register first \nClick /register')


@bot.callback_query_handler(state="*", func=lambda callback: True)
async def callback_f(callback):
    global calculator_global_var
    cur_state = await last_user_state(callback.message.json['chat']['username'])
    if cur_state == 'MyStates:is_logged_in' and cur_state != "MyStates:num_of_coins":
        #await bot.set_state(callback.message.chat.id, MyStates.is_logged_in, callback.message.chat.id)
        #print('підорастія')
        #await insert_state(callback.message.json['chat']['username'], await bot.get_state(callback.message.chat.id, callback.message.chat.id))
        if callback.data == 'calculator':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('BTC/$', callback_data='btcto$')
            item2 = types.InlineKeyboardButton('$/BTC', callback_data='$tobtc')
            item3 = types.InlineKeyboardButton('ETH/$', callback_data='ethto$')
            item4 = types.InlineKeyboardButton('$/ETH', callback_data='$toeth')
            item5 = types.InlineKeyboardButton('BNB/$', callback_data='bnbto$')
            item6 = types.InlineKeyboardButton('$/BNB', callback_data='$tobnb')
            item7 = types.InlineKeyboardButton('Menu', callback_data='menu')
            markup.add(item1, item2, item3, item4, item5, item6, item7)
            await bot.send_message(callback.message.chat.id, 'Choose an option', reply_markup=markup)
        elif callback.data == "log_out":
            await bot.send_message(callback.message.chat.id, 'Logged out')
            await bot.set_state(callback.message.chat.id, MyStates.logged_out, callback.message.chat.id)
            await insert_state(callback.message.json['chat']['username'], await bot.get_state(callback.message.chat.id, callback.message.chat.id))
            #print(await bot.get_state(callback.message.chat.id, callback.message.chat.id))
            #select_all()
        elif callback.data == 'rates':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('BTC', callback_data='btc')
            item2 = types.InlineKeyboardButton('ETH', callback_data='eth')
            item3 = types.InlineKeyboardButton('BNB', callback_data='bnb')
            item4 = types.InlineKeyboardButton('Menu', callback_data='menu')
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            markup.row(item4)
            await bot.send_message(callback.message.chat.id, 'Choose a coin:', reply_markup=markup)
        elif callback.data == 'btc':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('$ -> BTC', callback_data='$btc')
            item2 = types.InlineKeyboardButton('BTC -> $', callback_data='btc$')
            item3 = types.InlineKeyboardButton('Go back to coins', callback_data='rates')
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            await bot.send_message(callback.message.chat.id, 'Select the type of exchange: ', reply_markup=markup)
        elif callback.data == 'eth':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('$ -> ETH', callback_data='$eth')
            item2 = types.InlineKeyboardButton('ETH -> $', callback_data='eth$')
            item3 = types.InlineKeyboardButton('Go back to coins', callback_data='rates')
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            await bot.send_message(callback.message.chat.id, 'Select the type of exchange: ', reply_markup=markup)
        elif callback.data == 'bnb':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('$ -> BNB', callback_data='$bnb')
            item2 = types.InlineKeyboardButton('BNB -> $', callback_data='bnb$')
            item3 = types.InlineKeyboardButton('Go back to coins', callback_data='rates')
            markup.row(item1)
            markup.row(item2)
            markup.row(item3)
            await bot.send_message(callback.message.chat.id, 'Select the type of exchange: ', reply_markup=markup)
        elif callback.data == 'menu':
            await logged_menu(callback.message)
        elif callback.data in ['btcto$', 'ethto$', 'bnbto$', '$tobtc', '$toeth', '$tobnb']:
            await bot.set_state(callback.message.chat.id, MyStates.num_of_coins, callback.message.chat.id)
            await insert_state(callback.message.json['chat']['username'], await bot.get_state(callback.message.chat.id, callback.message.chat.id))
            calculator_global_var = callback.data
            if calculator_global_var[-1] == '$':
                await bot.send_message(callback.message.chat.id, f'Enter the number of {calculator_dict[callback.data]}s: ')
            else:
                await bot.send_message(callback.message.chat.id, 'Enter the number of dollars: ')

        elif callback.data == 'btc$':
            btc = await req.get_crypto_rates()
            await bot.send_message(callback.message.chat.id, f"1 Bitcoin costs {btc['bitcoin']['usd']}$")
        elif callback.data == '$btc':
            btc = await req.get_crypto_rates()
            await bot.send_message(callback.message.chat.id, f"1 $ costs {(1/btc['bitcoin']['usd']):.8f} BTC")
        elif callback.data == 'eth$':
            btc = await req.get_crypto_rates()
            await bot.send_message(callback.message.chat.id, f"1 Ethereum costs {btc['ethereum']['usd']}$")
        elif callback.data == '$eth':
            btc = await req.get_crypto_rates()
            await bot.send_message(callback.message.chat.id, f"1 $ costs {(1/btc['ethereum']['usd']):.8f} ETH")
        elif callback.data == 'bnb$':
            btc = await req.get_crypto_rates()
            await bot.send_message(callback.message.chat.id, f"1 Binancecoin costs {btc['binancecoin']['usd']}$")
        elif callback.data == '$bnb':
            btc = await req.get_crypto_rates()
            await bot.send_message(callback.message.chat.id, f"1 $ costs {(1/btc['binancecoin']['usd']):.8f} BNB")
    # elif cur_state == "MyStates:num_of_coins":
    #     await bot.set_state(callback.message.chat.id, MyStates.is_logged_in, callback.message.chat.id)
    #     #calculator_global_var = ''
    #     await bot.send_message(callback.message.chat.id, "Cancelled")
    elif cur_state != 'MyStates:num_of_coins':
        # print(last_user_state(callback.message.json['chat']['username']))
        await bot.send_message(callback.message.chat.id, 'Please log in or register first \nClick /register')





@bot.message_handler(state="*", commands=['cancel'])
async def any_state(message):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, "Cancelled.")
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['register'])
async def register(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    item1 = types.KeyboardButton('Share my contact', request_contact=True)
    markup.add(item1)
    await bot.set_state(message.from_user.id, MyStates.num, message.chat.id)
    await insert_state(message.from_user.username, await bot.get_state(message.from_user.id, message.chat.id))
    await bot.send_message(message.chat.id, 'Please share your contact', reply_markup=markup)


@bot.message_handler(content_types=['contact'])
async def num(message):
    cur_state = await last_user_state(message.from_user.username)
    if cur_state == 'MyStates:num':
        remove_markup = types.ReplyKeyboardRemove()
        user_info = {'id': message.from_user.id,
                     'username': message.from_user.username,
                     'first_name': message.from_user.first_name,
                     'last_name': message.from_user.last_name,
                     'phone_number': message.contact.phone_number}
        check_user = check_user_exsists(*user_info.values())
        # print(check_user)
        if len(check_user) > 1:
            await bot.send_message(message.chat.id, 'Something went wrong', reply_markup=remove_markup)
        elif len(check_user) == 1 and check_user[0][-1] == 0:
            await bot.send_message(message.chat.id, 'You are logged in \nClick /menu to open the menu', reply_markup=remove_markup)
            await bot.set_state(message.from_user.id, MyStates.is_logged_in, message.chat.id)
            await insert_state(message.from_user.username, await bot.get_state(message.from_user.id, message.chat.id))
        elif len(check_user) == 1 and check_user[0][-1] == 1:
            await bot.send_message(message.chat.id, 'Your account has been deleted by the admin', reply_markup=remove_markup)
        else:
            insert_user(*user_info.values())
            await bot.set_state(message.from_user.id, MyStates.is_logged_in, message.chat.id)
            await insert_state(message.from_user.username, await bot.get_state(message.from_user.id, message.chat.id))
            await bot.send_message(message.chat.id, 'You have successfully registered', reply_markup=remove_markup)

@bot.message_handler(is_good=True)
async def calculator_coins_to_dollar(message):
    global calculator_global_var
    cur_state = await last_user_state(message.from_user.username)
    if cur_state == 'MyStates:num_of_coins':
        try:
            coins_or_dollars = float(message.text.strip())
        except ValueError:
            await bot.send_message(message.chat.id, "Enter the number of coins like a number please")
        else:
            btc = await req.get_crypto_rates()
            if calculator_global_var[-1] == '$':
                dollar = coins_or_dollars * btc[calculator_dict[calculator_global_var]]['usd']
                await bot.send_message(message.chat.id, "≈ " + str(round(dollar, 3)) + "$")
            else:
                dollar = coins_or_dollars * (1/btc[calculator_dict[calculator_global_var]]['usd'])
                await bot.send_message(message.chat.id, f"≈ {str(round(dollar, 3))} {calculator_dict[calculator_global_var]}s")
            calculator_global_var = ''
            await bot.set_state(message.from_user.id, MyStates.is_logged_in, message.chat.id)
            await insert_state(message.from_user.username, await bot.get_state(message.from_user.id, message.chat.id))
# state=MyStates.num_of_coins
create_db()
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(IsGood())
#asyncio.run(bot.polling())
asyncio.run(bot.infinity_polling())
