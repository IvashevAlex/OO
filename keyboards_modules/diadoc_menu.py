import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def DD_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def menu(message):
        modul_for_bot.tests_data[message.chat.id] = 'DD'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)  # <--- тут будет отправка и меню с выбором


def test_DD(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Web', callback_data='Web.Диадок')
    itembtn2 = types.InlineKeyboardButton('Модуль', callback_data='Модуль.Диадок')
    itembtn3 = types.InlineKeyboardButton('Роуминг', callback_data='Роуминг.Диадок')
    itembtn4 = types.InlineKeyboardButton('Коннекторы', callback_data='Коннекторы.Диадок')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn12)

    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)

def prk_diadoc(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn5 = types.InlineKeyboardButton('Web', callback_data='Web.Диадок')
    itembtn6 = types.InlineKeyboardButton('Модуль', callback_data='Модуль.Диадок')
    itembtn7 = types.InlineKeyboardButton('Роуминг', callback_data='Роуминг.Диадок')
    # itembtn8 = types.InlineKeyboardButton('Коннекторы', callback_data='Коннекторы.Дидаок')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn5, itembtn6, itembtn7)
    # markup.add(itembtn8) Коннекторы диадок
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


DD_menu("Диaдoк", bot)
