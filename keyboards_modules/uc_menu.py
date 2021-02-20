import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def UC_menu(name, bot):
  @bot.message_handler(func=lambda message: message.text == name)
  def UC(message):
    modul_for_bot.tests_data[message.chat.id] = 'UC'
    modul_for_bot.sql_user(bot, message)
    keyboards.test_menu(bot, message)


def test_uc(bot, callback_query):  # <--- формируем меню с тестами для УЦ
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Проекты УЦ', callback_data='Проекты УЦ')
    itembtn2 = types.InlineKeyboardButton('ЭТП', callback_data='ЭТП')
    itembtn3 = types.InlineKeyboardButton('ИС', callback_data='ИС')
    itembtn4 = types.InlineKeyboardButton('Закупки', callback_data='Закупки')
    itembtn5 = types.InlineKeyboardButton('Реестро', callback_data='Реестро')
    itembtn6 = types.InlineKeyboardButton('Контур.Торги', callback_data='Контур.Торги')
    itembtn7 = types.InlineKeyboardButton('Декларант', callback_data='Декларант')
    itembtn8 = types.InlineKeyboardButton('Школа', callback_data='Школа')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn7, itembtn8)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_uc(bot, callback_query):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Проекты УЦ', callback_data='Проекты УЦ')
    itembtn2 = types.InlineKeyboardButton('ЭТП', callback_data='ЭТП')
    itembtn3 = types.InlineKeyboardButton('ИС', callback_data='ИС')
    itembtn4 = types.InlineKeyboardButton('Закупки', callback_data='Закупки')
    itembtn5 = types.InlineKeyboardButton('Декларант', callback_data='Декларант')
    itembtn6 = types.InlineKeyboardButton('Школа', callback_data='Школа')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


UC_menu("ᎩЦ", bot)
