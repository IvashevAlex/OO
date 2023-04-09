import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def ext_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def Extern_menu(message):
        modul_for_bot.tests_data[message.chat.id] = 'extrn'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)  # <--- тут будет отправка и меню с выбором


def test_ext(bot, callback_query):  # <--- формируем меню с тестами для КЭ
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('Знакомство с КЭ', callback_data='Знакомство')
    itembtn2 = types.InlineKeyboardButton('ФНС', callback_data='ФНС')
    itembtn3 = types.InlineKeyboardButton('ЕНП', callback_data='ЕНП')
    itembtn4 = types.InlineKeyboardButton('Мелкие сервисы', callback_data='Мелкие сервисы')
    itembtn5 = types.InlineKeyboardButton('Отчетность ПФР и СФР', callback_data='ПФР и СФР')
    itembtn6 = types.InlineKeyboardButton('ФСС', callback_data='ФСС')
    itembtn7 = types.InlineKeyboardButton('НДС и НДС+', callback_data='НДС')
    itembtn8 = types.InlineKeyboardButton('Требования и коннектор', callback_data='Требования')
    itembtn9 = types.InlineKeyboardButton('РСВ', callback_data='РСВ')
    itembtn10 = types.InlineKeyboardButton('НДФЛ', callback_data='НДФЛ')

    itembtn20 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn7, itembtn8, itembtn9)
    markup.add(itembtn10, itembtn20)

    try:
        bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                            message_id=callback_query.message.message_id, reply_markup=markup)
    except Exception as EX:
        print(EX.args)

def prk_ext(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('Мелкие сервисы', callback_data='Case.Мелкие')
    itembtn2 = types.InlineKeyboardButton('Отчетность ПФР и СФР', callback_data='Case.ПФР')
    itembtn3 = types.InlineKeyboardButton('ФСС', callback_data='Case.ФСС')
    itembtn4 = types.InlineKeyboardButton('НДС', callback_data='Case.НДС')
    itembtn5 = types.InlineKeyboardButton('Требования', callback_data='Case.Требования')
    itembtn6 = types.InlineKeyboardButton('РСВ', callback_data='Case.РСВ')
    itembtn7 = types.InlineKeyboardButton('НДФЛ', callback_data='Case.НДФЛ')

    itembtn20 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn7, itembtn20)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)
    except Exception as EX:
        print(EX.args)

ext_menu("Экстeрн", bot)

# def test_ext(bot, callback_query):  # <--- формируем меню с тестами для КЭ
#     modul_for_bot.sql_user(bot, callback_query)

#     markup = types.InlineKeyboardMarkup()

#     itembtn3 = types.InlineKeyboardButton('Интерфейс', callback_data='Интерфейс')
#     itembtn4 = types.InlineKeyboardButton('Режим работы', callback_data='Режим работы')
#     itembtn5 = types.InlineKeyboardButton('ФНС', callback_data='ФНС')
#     itembtn6 = types.InlineKeyboardButton('ИОН', callback_data='ИОН')
#     itembtn7 = types.InlineKeyboardButton('Таблица отчетности', callback_data='Таблица отчетности')
#     itembtn8 = types.InlineKeyboardButton('Письма ФНС', callback_data='Письма ФНС')
#     itembtn9 = types.InlineKeyboardButton('ПФР', callback_data='ПФР')
#     itembtn10 = types.InlineKeyboardButton('НДС и требования', callback_data='НДС и требования')
#     itembtn11 = types.InlineKeyboardButton('НДФЛ', callback_data='НДФЛ')
#     itembtn13 = types.InlineKeyboardButton('Росстат', callback_data='Росстат')
#     itembtn14 = types.InlineKeyboardButton('РСВ', callback_data='РСВ')
#     itembtn15 = types.InlineKeyboardButton('Заполнение ПФР', callback_data='Заполнение ПФР')

#     itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

#     markup.add(itembtn3, itembtn4, itembtn5)
#     markup.add(itembtn6, itembtn7, itembtn8)
#     markup.add(itembtn9, itembtn10, itembtn11)
#     markup.add(itembtn13, itembtn14, itembtn15)
#     markup.add(itembtn12)

#     bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
#                           message_id=callback_query.message.message_id, reply_markup=markup)


# def prk_ext(bot, callback_query):
#     modul_for_bot.sql_user(bot, callback_query)

#     markup = types.InlineKeyboardMarkup()

#     itembtn3 = types.InlineKeyboardButton('Интерфейс', callback_data='Интерфейс')
#     itembtn4 = types.InlineKeyboardButton('Режим работы', callback_data='Режим работы')
#     itembtn5 = types.InlineKeyboardButton('ФНС', callback_data='ФНС')
#     itembtn6 = types.InlineKeyboardButton('ИОН', callback_data='ИОН')
#     itembtn7 = types.InlineKeyboardButton('Таблица отчетности', callback_data='Таблица отчетности')
#     itembtn8 = types.InlineKeyboardButton('Письма ФНС', callback_data='Письма ФНС')
#     itembtn9 = types.InlineKeyboardButton('ПФР', callback_data='ПФР')
#     itembtn10 = types.InlineKeyboardButton('НДС и требования', callback_data='НДС и требования')
#     itembtn11 = types.InlineKeyboardButton('НДФЛ', callback_data='НДФЛ')
#     itembtn13 = types.InlineKeyboardButton('Росстат', callback_data='Росстат')
#     itembtn14 = types.InlineKeyboardButton('РСВ', callback_data='РСВ')
#     itembtn15 = types.InlineKeyboardButton('Заполнение ПФР', callback_data='Заполнение ПФР')

#     itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

#     markup.add(itembtn3, itembtn4, itembtn5)
#     markup.add(itembtn6, itembtn7, itembtn8)
#     markup.add(itembtn9, itembtn10, itembtn11)
#     markup.add(itembtn13, itembtn14, itembtn15)
#     markup.add(itembtn12)
#     bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
#                           message_id=callback_query.message.message_id, reply_markup=markup)

