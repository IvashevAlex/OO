import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def FMS_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def FMS_menu_start(message):
        modul_for_bot.tests_data[message.chat.id] = 'FMS'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)


def test_fms(bot, callback_query):  # <--- формируем меню с тестами для ФМС
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn3 = types.InlineKeyboardButton('ФМС', callback_data='ФМС')
    itembtn4 = types.InlineKeyboardButton('Отель', callback_data='Отель')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn3, itembtn4)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_fms(bot, callback_query):
    markup = types.InlineKeyboardMarkup()
    itembtn3 = types.InlineKeyboardButton('ФМС', callback_data='ФМС')
    itembtn4 = types.InlineKeyboardButton('Отель', callback_data='Отель')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn3, itembtn4)
    markup.add(itembtn12)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


FMS_menu("ФMС", bot)
