from time import sleep
from modul_for_bot import *
import text
import test_mode_check

# Переменные
ver = '1.0.2.4'
info = text.info
test_mode = test_mode_check.test_mode()

# Обработка команды /start
@bot.message_handler(commands=["start"])
def greeting(message):
    print('IN greeting')
    if echo(message) == True:
        question(bot, message)


# Обработка команды /help
@bot.message_handler(commands=["help"])
def help(message):
    print('IN help')
    if echo(message) == True:
        bot.send_message(message.chat.id, info, parse_mode='Markdown')


# Обработка команды /admin
@bot.message_handler(commands=["admin"])
def admin_menu(message):
    print('IN admin_menu')
    if message.chat.id in (233770916, 391368365, 1325029854, 411204685):
        Admin_menu(message, bot)
    else:
        bot.send_message(message.from_user.id, text.no_admin_access)

# Обработка команды /test_1
@bot.message_handler(commands=["test_1"])
def test(message):
    print('IN test')
    if echo(message) == True:
        bot.send_message(message.chat.id, text.test_1, parse_mode='Markdown')

# Обработка текстового сообщения "В меню"
@bot.message_handler(func=lambda message: message.text == "В меню")
def back(message):
    print('IN back')
    if echo(message) == True:
        question(bot, message)


# Обработка текстового сообщения "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def back_menu(message):
    print('IN back_menu')
    if echo(message) == True:
        # Запускаем test_menu из modul_for_bot
        back_to_menu(bot, message)


# Обработка текстового сообщения "Пoмощь". Первая буква "o" в слове латинская
@bot.message_handler(func=lambda message: message.text == "Пoмощь")
def help_text(message):
    print('IN help_text')
    if echo(message) == True:
        bot.send_message(message.chat.id, info, parse_mode='Markdown')


# Обработка текстового сообщения "Результаты"
@bot.message_handler(func=lambda message: message.text == "Результаты")
def res0(message):
    print('IN res0')
    if echo(message) == True:
        res(bot, message)


# Обработка нажатия кнопки "Сообщить об ошибке"
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Сообщить об ошибке')
def error_send(callback_query):
    print('IN error_send')
    if echo(callback_query) == True:
        send_error(bot, callback_query)


# Обработка любых текстовых сообщений, исключая вышеперечисленные.
# В среднем, считаем, что это ответы на вопросы, заданные пользователю.
@bot.message_handler(content_types=['text'])
def answer0(message):
    print('IN answer0')
    if callback_check.get(message.from_user.id) == 'tests':
        print('IF tests')
        continue_(bot, message)
        messages = bot.send_message(message.from_user.id, text.waiting_check)
        save_message_id['message_id'][message.from_user.id] = messages.message_id
        check_answer(bot, message)
        return

    elif callback_check.get(message.from_user.id) == 'practicks':
        print('IF practics')
        continue_(bot, message)
        messages = bot.send_message(message.from_user.id, text.waiting_check)
        save_message_id['message_id'][message.from_user.id] = messages.message_id
        check_answer_prk(bot, message)
        return
    

    elif callback_check.get(message.from_user.id) == None:
        print('IF None')
        if echo(message) == True:
            messages = bot.send_message(message.from_user.id, text.not_selected)
            save_message_id['message_id'][message.from_user.id] = messages.message_id

    continue_(bot, message)


# Информация по боту 
print(f'Бот запущен! Текущая версия {ver}.')
if test_mode == True:
    print('Активирован режим тестирования!')
else:
    pass

# Запуск основного цикла работы бота
while True:
    try:
        bot.polling(none_stop=False, interval=0, timeout=20)
    except Exception as e:
        print(e.args)
        sleep(0.7)
