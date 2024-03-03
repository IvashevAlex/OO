from time import sleep
from modul_for_bot import *
from config import *
import text
import test_mode_check
import log


# Переменные
ver = '1.1.1.1'
info = text.info
test_mode = test_mode_check.test_mode()


# Обработка команды /start
@bot.message_handler(commands=["start"])
def greeting(message):

    time_info = str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5]) + ' '
    user_info = str(message.from_user.id) + ' ' + str(message.from_user.username) + ' '
    result = time_info + user_info + ' --- /start\n'
    print('--->', result)
    
    if echo(message) == True:
        question(bot, message)


# Обработка команды /help
@bot.message_handler(commands=["help"])
def help(message):

    if echo(message) == True:
        bot.send_message(message.chat.id, info, parse_mode='Markdown')


# Обработка команды /admin
@bot.message_handler(commands=["admin"])
def admin_menu(message):

    if message.chat.id in admins:
        Admin_menu(message, bot)
    else:
        bot.send_message(message.from_user.id, text.no_admin_access)


# Обработка команды /remove
@bot.message_handler(commands=["remove"])
def remove_access(message):
    if message.chat.id in admins:
        try:
            
            try:
                connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
                cursor = connection.cursor()
                SQLQuery = sql_queries.remove_true_access(message.text.split(' ')[1])
                cursor.execute(SQLQuery) 
                connection.commit()
                connection.close()
                bot.send_message(message.from_user.id, 'Юзер с почтой' + str(message.text.split(' ')[1] + ' удалён из базы. \n\
                                    Теперь при новом цикле автодобавления он будет записан с новым юзернеймом.'))
            
            except Exception as EX:
                    print(EX.args)
            
            print(message.text.split(' ')[1])
        except Exception as EX:
            bot.send_message(message.from_user.id, 'Не указана почта! Команду необходимо указать как \"/remove mail@skbkontur.ru\"')
    else:
        bot.send_message(message.from_user.id, text.no_admin_access)


# Обработка текстового сообщения "В меню"
@bot.message_handler(func=lambda message: message.text == "В меню")
def back(message):

    if echo(message) == True:
        question(bot, message)


# Обработка текстового сообщения "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def back_menu(message):

    if echo(message) == True:
        # Запускаем test_menu из modul_for_bot
        back_to_menu(bot, message)


# Обработка текстового сообщения "Пoмощь". Первая буква "o" в слове латинская
@bot.message_handler(func=lambda message: message.text == "Пoмощь")
def help_text(message):

    if echo(message) == True:
        bot.send_message(message.chat.id, info, parse_mode='Markdown')


# Обработка текстового сообщения "Результаты"
@bot.message_handler(func=lambda message: message.text == "Результаты")
def results_key(message):

    if echo(message) == True:
        res(bot, message)


# Обработка нажатия кнопки "Сообщить об ошибке"
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Сообщить об ошибке')
def error_send(callback_query):

    if echo(callback_query) == True:
        send_error(bot, callback_query)


# Обработка любых текстовых сообщений, исключая вышеперечисленные.
# В среднем, считаем, что это ответы на вопросы, заданные пользователю.
@bot.message_handler(content_types=['text'])
def answer_text(message):

    if callback_check.get(message.from_user.id) == 'tests':

        continue_(bot, message)
        messages = bot.send_message(message.from_user.id, text.waiting_check)
        save_message_id['message_id'][message.from_user.id] = messages.message_id
        check_answer(bot, message)
        return

    elif callback_check.get(message.from_user.id) == 'practicks':

        continue_(bot, message)
        messages = bot.send_message(message.from_user.id, text.waiting_check)
        save_message_id['message_id'][message.from_user.id] = messages.message_id
        check_answer_prk(bot, message)
        return
    

    elif callback_check.get(message.from_user.id) == None:

        if echo(message) == True:
            messages = bot.send_message(message.from_user.id, text.not_selected)
            save_message_id['message_id'][message.from_user.id] = messages.message_id

    continue_(bot, message)


# Информация по боту 
print(f'Бот запущен! Текущая версия {ver}')

if test_mode == True:
    print('Активирован режим тестирования!')
else:
    pass

# Запуск основного цикла работы бота
while True:
    try:
        bot.polling(none_stop=False, interval=0, timeout=20)
    except Exception as EX:
        print(EX.args)
        sleep(1)
