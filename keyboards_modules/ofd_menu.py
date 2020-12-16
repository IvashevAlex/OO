import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def OFD_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def OFD_KKT_menu(message):
        modul_for_bot.tests_data[message.chat.id] = 'OFD'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)


def test_ofd(bot, callback_query):  # <--- формируем меню с тестами для ОФД
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('API', callback_data='API')
    itembtn2 = types.InlineKeyboardButton('1C', callback_data='1C')
    itembtn3 = types.InlineKeyboardButton('ОФД', callback_data='ОФД')
    itembtn4 = types.InlineKeyboardButton('ККТ', callback_data='ККТ')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn3, itembtn4)
    markup.add(itembtn1, itembtn2)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_ofd(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn5 = types.InlineKeyboardButton('ОФД', callback_data='ОФД')
    itembtn1 = types.InlineKeyboardButton('API', callback_data='API')
    itembtn6 = types.InlineKeyboardButton('ККТ', callback_data='ККТ')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn5, itembtn6, itembtn1)

    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


OFD_menu("OФД", bot)
