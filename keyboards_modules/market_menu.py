import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def M_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def Market_m(message):
        modul_for_bot.tests_data[message.chat.id] = 'MK'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)


def test_mk(bot, callback_query):  # <--- формируем меню с тестами для Маркета
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Маркет', callback_data='Маркет')
    itembtn2 = types.InlineKeyboardButton('ЕГАИС', callback_data='ЕГАИС')
    itembtn3 = types.InlineKeyboardButton('КМК', callback_data='КМК')
    itembtn4 = types.InlineKeyboardButton('Меркурий в Маркете', callback_data='Меркурий в Маркете')
    itembtn5 = types.InlineKeyboardButton('Маркировка в Маркете', callback_data='Маркировка в Маркете')
    itembtn6 = types.InlineKeyboardButton('РАР', callback_data='РАР')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5)
    markup.add(itembtn6)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_mk(bot, callback_query):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Маркет', callback_data='Маркет')
    itembtn2 = types.InlineKeyboardButton('ЕГАИС', callback_data='ЕГАИС')
    itembtn3 = types.InlineKeyboardButton('КМК', callback_data='КМК')
    itembtn4 = types.InlineKeyboardButton('Меркурий в Маркете', callback_data='Меркурий в Маркете')
    itembtn5 = types.InlineKeyboardButton('Маркировка в Маркете', callback_data='Маркировка в Маркете')
    itembtn6 = types.InlineKeyboardButton('РАР', callback_data='РАР')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


M_menu("Maркет", bot)
