import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def EDI_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def menu(message):
        modul_for_bot.tests_data[message.chat.id] = 'EDI'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)  # <--- тут будет отправка и меню с выбором


def test_EDI(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('EDI Web', callback_data='EDI Web')
    itembtn2 = types.InlineKeyboardButton('EDI 1C', callback_data='EDI 1C')
    itembtn4 = types.InlineKeyboardButton('Меркурий', callback_data='Меркурий')
    itembtn3 = types.InlineKeyboardButton('Поставки', callback_data='Поставки')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_edi(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('EDI Web', callback_data='EDI Web')
    itembtn2 = types.InlineKeyboardButton('EDI 1C', callback_data='EDI 1C')
    itembtn4 = types.InlineKeyboardButton('Меркурий', callback_data='Меркурий')
    itembtn3 = types.InlineKeyboardButton('Поставки', callback_data='Поставки')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn12)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


EDI_menu("Pитейл", bot)
