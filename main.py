#MAIN файл в котором вся инициализация и запуск

from time import sleep
from keyboards import *
from WhiteList import *



#ip_port = Proxy_bot.read_proxy()
#telebot.apihelper.proxy = {'https':'https://{}'.format(ip_port)}

#bot = telebot.TeleBot('935355674:AAFDc4BwAB4jQtugRIpcGiEPqyhKZqv3XSU',  threaded=False)
bot = telebot.TeleBot('1253732018:AAESPvgR9YfmnTAHtHRMWJ8tjOmApA_qSyI',  threaded=False) #OOHelper

#db = xlrd.open_workbook('111.xlsx')
#db = openpyxl.load_workbook('./Data/111.xlsx')

a = 0

info = "Выбери тему и вид обучения для подготовки." \
       "\n\n*Тесты:* пиши правильные варианты ответа цифрами без пробелов и дополнительных символов. Вариантов может быть несколько." \
       "\n\n*Кейсы:* пиши правильные ответы в соответствии с требованиями вопросов. " \
       "\n\nДля того, чтобы ответить на вопрос:" \
       "\n1. Напиши ответ." \
       "\n2. Нажми «Отправить»." \
       "\n3. Нажми «Ответить», если уверен в предоставленных вариантах." \
       "\n\nЕсли во время прохождения теста ты перейдешь в меню, то результат сбросится, помни об этом!"

#Кнопка старт
@bot.message_handler(commands=["start"])
def greeting(message):
    if echo(message) == True:
        question(bot, message)

#Кнопка help
@bot.message_handler(commands=["help"])
def help(message):
    if echo(message) == True:
        bot.send_message(message.chat.id, info)


#Админка по команде /admin
@bot.message_handler(commands=["admin"]) #<---- Обновить таблицы в памяти, после изменений
def admin_menu(message):
    if message.chat.id in (233770916, 391368365):
        Admin_menu(message, bot)
    else:
        bot.send_message(message.from_user.id, 'У тебя нет доступа к данному функционалу.')


#Кнопка В меню
@bot.message_handler(func=lambda message: message.text == "В меню")
def back(message):
    if echo(message) == True:
        question(bot, message)


#Кнопка Назад
@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    if echo(message) == True:
        back_to_menu(bot, message)


#Кнопка Помощь
@bot.message_handler(func=lambda message: message.text == "Помощь")
def help_text(message):
    if echo(message) == True:
        bot.send_message(message.chat.id, info, parse_mode='Markdown')


#Кнопка ответить
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Ответить')
def ans_true(callback_query: CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    if echo(callback_query) == True:
        try:
            del callback_check[callback_query.from_user.id]
        except:
            pass

        try:
            check_answer_id = save_message_id['check_answer'][callback_query.from_user.id] #ПОлучаем ID сообщения заданного послений раз вопроса
        except:
            check_answer_id = 0 #Если вопрос не задавался то ставим 0

        if check_answer_id == callback_query.message.message_id: #Совпадает ли ID запомненного вопроса с ID где мы нажали кнопку "Ответить"

            message = bot.send_message(callback_query.from_user.id, "Проверяем ответ.\nПодожди немного.")
            save_message_id['message_id'][callback_query.from_user.id] = message.message_id

            if practicks_data.get(callback_query.from_user.id) == 'PR':
                check_answer_prk(bot, callback_query)
            else:
                check_answer(bot, callback_query)

        else: #Если нажали Ответить не в последнем заданном вопросе, то
            bot.edit_message_text("Ты пытаешься ответить на вопрос, который задавался гораздо раньше.",
                              chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


#Кнопка Результаты
@bot.message_handler(func=lambda message: message.text == "Результаты")
def res0(message):
    if echo(message) == True:
        res(bot, message)


#Inline кнопка Сообщить об ошибке
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Сообщить об ошибке')
def error_send(callback_query):
    if echo(callback_query) == True:
        send_error(bot, callback_query)


#Обработчик отправленного текстового сообщения от пользователя
@bot.message_handler(content_types=['text'])
def answer0(message):
    if echo(message) == True:
        continue_(bot, message)
        print(message.message_id)


# --------- Собственно сам MAIN запуск ------------ #
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(e.args)
        sleep(0.7)