import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def focus_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def focus_menu_start(message):
        modul_for_bot.tests_data[message.chat.id] = 'KF'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)


def test_focus(bot, callback_query):  # <--- формируем меню с тестами для Фокус
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Фокус', callback_data='Фокус')
    itembtn2 = types.InlineKeyboardButton('API Фокус', callback_data='API Фокус')
    itembtn3 = types.InlineKeyboardButton('Компас', callback_data='Компас')
    itembtn4 = types.InlineKeyboardButton('Декларант технический', callback_data='KD.Test.Tech')
    itembtn5 = types.InlineKeyboardButton('Декларант методология', callback_data='KD.Test.Method')
    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5)
    markup.add(itembtn10)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_focus(bot, callback_query):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Фокус', callback_data='Case.Фокус')
    itembtn2 = types.InlineKeyboardButton('API Фокус', callback_data='Case.API Фокус')
    itembtn3 = types.InlineKeyboardButton('Компас', callback_data='Case.Компас')
    itembtn4 = types.InlineKeyboardButton('Декларант технический', callback_data='KD.Case.Tech')
    itembtn5 = types.InlineKeyboardButton('Декларант методология', callback_data='KD.Case.Method')
    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5)
    markup.add(itembtn10)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


focus_menu("Фокус", bot)
