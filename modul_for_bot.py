import random
# import requests
import time
# import openpyxl
import pypyodbc
import re
import test_mode_check
import get_db_excel
from keyboards import *
from keyboards_modules.modules import *
from keyboards_modules.diadoc_menu import *

import text
import datetime as dt

today = dt.date.today()

test_mode = test_mode_check.test_mode()

if test_mode == False:
    alex_id = 233770916 #ID для обработки сообщений об ошибке в вопросе
    fafa_id = 1325029854 #ID для обработки технической ошибки
else:
    alex_id = 1325029854 #ID для обработки сообщений об ошибке в вопросе
    fafa_id = 1325029854 #ID для обработки технической ошибки

data_base = {'BotUsers': {},
             'UserQuestions': {},
             }

sheet = 0
count = 0
rand = 0

# Переменная для хранения словаря {id пользователя: номер страницы}
a = {}

save_check = {'wic_search':{}
              }
tests_data = {}
practicks_data = {'check_attempt':{}}
ans = {'lower': {}}
callback_check = {'text': {}}
file_id = {}
file_dir = 'Data/screens/'  # Указываем путь до папок отделов с скринами и файлами
save_message_id = {'check_answer': {},
                   'message_id': {},
                   'message_text':{},
                   'message_id_answer':{}
                   }

rand_question = {} #<-- тут мы держим номера вопросов, которые нужно задать
db_data = {} #<---- База данных с вопросами по всем продуктам



# -----------------------   Загружаем все эксели в базу -------------------------#
db_data = get_db_excel.get_question()  # <-- тут мы для храним файл ексель для каждого отдела

# ------------ Функция обработки нажатия кнопок ---------- #
# Списки кнопок для тестов находятся в файле modules.py, а для кейсов к ним прибавляется единица
# Разделы у которых нет стандартного разделения тесты/кейсы обрабабатываются подругому
def quest(theme, number_of_page, bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == theme)
    def name_def(callback_query):
        print('IN quest')
        if echo(callback_query) != True:
            bot.send_message(callback_query.from_user.id, text.no_rights)
            return

        try:
            bot.edit_message_text(text=text.wait, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
            bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
        except Exception as Abc:
            pass

        a[callback_query.from_user.id] = number_of_page  # <--- Запоминаем номер страницы с продуктом (Ехель)
        save_check['wic_search'][callback_query.from_user.id] = False #Отвечает за нажатие кнопки Wic поиск знаний. Для того чтобы формируя кейс влиять на сообщение

        if practicks_data.get(callback_query.from_user.id) == 'PR':  # <---- находимся ли мы в кейсах
            if tests_data[callback_query.from_user.id] == 'extrn':
                # a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1 #из Екселя берем number_of_page + 1, ибо в файле 1ая табла тесты а следующая кейсы
                pass
            elif tests_data[callback_query.from_user.id] == 'BUH':
                a[callback_query.from_user.id] = 7 #В продукте КБ кейсы всегда на 7 индексе
            elif tests_data[callback_query.from_user.id] == 'ELB':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'OFD':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'EDI':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'FMS':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'UC':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'MK':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'DD':
                pass
                # a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'KF':
                # a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1 
                pass           
            elif tests_data[callback_query.from_user.id] == 'WIC':
                if callback_query.data == 'WIC.Поиск_знаний': #Проверяем нажата ли кнопка поиск знаний раздела ВИК
                    save_check['wic_search'][callback_query.from_user.id] = True #Если нажата то активируем переменную, для формирования определенного сообщения в кейсах
            elif tests_data[callback_query.from_user.id] == 'OTHER':
                pass # нам не нужно присваивать новые номера для внутр сервисов

            answers_prk(bot, callback_query) #Запускаем цикл вопрос\ответ по кейсам
        else:
            answers(bot, callback_query) #Если выбрали не кейсы, то запускаем цикл вопрос\ответ по тестам


def sql_user(bot, callback_query):
    print('IN sql_user')
    userid = str(callback_query.from_user.id)
    print('Пользователь =', userid,' Время обращения:', 
            time.localtime()[3],':',time.localtime()[4],':',time.localtime()[5])

    if str(callback_query.from_user.id) == userid:
        # print('user -', callback_query.from_user.id)
        data_base['BotUsers'][callback_query.from_user.id] = {'UserChat': str(callback_query.from_user.id),
                                                              'UserRand': '0',
                                                              'UserPage': 'None',
                                                              'UserAnswer': 'None',
                                                              'UserRowQuestions': '0',
                                                              'UserCounterTrueAns': '0'}

        rand_question[callback_query.from_user.id] = []
        try:
            del callback_check[callback_query.from_user.id]
        except:
            pass


    else:
        data_base['BotUsers'][callback_query.from_user.id] = {'UserChat': str(callback_query.from_user.id),
                                                              'UserRand': '0',
                                                              'UserPage': 'None',
                                                              'UserAnswer': 'None',
                                                              'UserRowQuestions': '0',
                                                              'UserCounterTrueAns': '0'}
        rand_question[callback_query.from_user.id] = []

    try:
        del data_base['UserQuestions'][callback_query.from_user.id]
    except:
        pass

    try:
        del callback_check[callback_query.from_user.id]
    except:
        pass

    results = data_base['BotUsers'][callback_query.from_user.id]['UserChat'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns']

    # print(results)


# ------ Проверяем по какому продукту сейчас проходит тестирование ------------#
def check_product(callback_query):
    print('IN check_product')
    if tests_data[callback_query.from_user.id] == 'DD':
        print('DD question')
        db = db_data['DD']
    elif tests_data[callback_query.from_user.id] == 'EDI':
        print('EDI question')
        db = db_data['EDI']
    elif tests_data[callback_query.from_user.id] == 'extrn':
        print('KE question')
        db = db_data['KE']
    elif tests_data[callback_query.from_user.id] == 'UC':
        print('UC question')
        db = db_data['UC']
    elif tests_data[callback_query.from_user.id] == 'MK':
        print('MK question')
        db = db_data['MK']
    elif tests_data[callback_query.from_user.id] == 'FMS':
        print('FMS question')
        db = db_data['FMS']
    elif tests_data[callback_query.from_user.id] == 'OFD':
        print('OFD question')
        db = db_data['OFD']
    elif tests_data[callback_query.from_user.id] == 'BUH':
        print('BH question')
        db = db_data['BH']
    elif tests_data[callback_query.from_user.id] == 'ELB':
        print('ELB question')
        db = db_data['ELB']
    elif tests_data[callback_query.from_user.id] == 'INST':
        print('INST question')
        db = db_data['INST']
    elif tests_data[callback_query.from_user.id] == 'WIC':
        print('WIC question')
        db = db_data['WIC']
    elif tests_data[callback_query.from_user.id] == 'OTHER':
        print('OTHER question')
        db = db_data['OTHER']
    elif tests_data[callback_query.from_user.id] == 'KF':
        print('KF question')
        db = db_data['KF']
    else:
        print('ELSE')
        db = db_data['all']

    return db


def get_max_row(sheet):  # <--- Функция для получения максимального числа вопросов
    print('IN get_max_row')
    number_A = 1  # <--- Это число для ячейки в столбике А
    max_row = 0  # <--- Максимальное число вопросов

    while sheet[f'{chr(65) + str(number_A)}'].value != 'stop':
        if sheet[f'{chr(65) + str(number_A)}'].value != None:
            max_row += 1
            number_A += 1
        else:
            break

    return max_row


# Функция выбора случайного вопроса
def random_question(id_user, max_row):
    print('IN random_question')
    if len(rand_question[id_user]) < 1:
        for i in range(0, max_row):
            rand_question[id_user].append(i)

    index_question = random.choice(rand_question[id_user])  # <--- получаем случайное число из списка
    rand_question[id_user].remove(index_question)

    return index_question


def answers(bot, callback_query):  # <--- Функция отвечающая за поиск и отправку вопросов по тестам
    print('IN answers')
    db = check_product(callback_query)  # db = db_data['FMS']['Название листа'] внутри будет dict с вопросами и вариантами ответов

    # <--- Получаем название вкладки (продукта) в таблице
    name_sheet = int(a[callback_query.from_user.id])
    # <--- Загружаем все вопросы во вкладке, имя которой узнали выше
    sheets_name = list(db.keys()) #Тут мы получили название листов

    name_sheet = sheets_name[name_sheet] #Тут мы получаем название нужного листа

    sheet = db[name_sheet] #Получаем вопросы из полученного листа
    

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    if str(results[1]) == 'None':
        data_base['BotUsers'][callback_query.from_user.id]['UserPage'] = str(a[callback_query.from_user.id])
        data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'] = len(sheet)

    data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'] = 'None'

    results = int(data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'])

    try:
        # смотрим сколько всего вопросов было и добавляем 1
        ress = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand'])
    except:
        ress = 0 + 1

    print('ress = ', ress)

    if ress == results:  # <--- Если ответил на все вопросы
        print('Task complete!')

        results_cmpl = data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'], \
            data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns']

        sc = results_cmpl
        results_cmpl = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand'])
        ans_q = results_cmpl

        bot.send_message(callback_query.from_user.id, f'Ты ответил на все вопросы! \n'
                                                      f'\nКоличество вопросов, которые были заданы: {str(ans_q)}'
                                                      f'\nПравильных ответов: {int(sc[1])}')

        callback_check[callback_query.from_user.id] = 'end'

    else:  # <--- Если ответил не на все вопросы
        t = 0
        while t != 1:
            try:  # <--- Если номер вопроса получится тем же на который уже был ответ то получим исключение
                # --------------- Ниже мы получаем рандомное число вопроса, и записываем егов BotUsers UserRand ------- #
                max_row = len(sheet)
                # Получаем случайный вопрос
                number = random_question(callback_query.from_user.id, max_row)

                try:
                    data_base['UserQuestions'][callback_query.from_user.id]['UserChat'] = str(callback_query.from_user.id)
                except:
                    data_base['UserQuestions'][callback_query.from_user.id] = {'UserChat': '0',
                                                                               'UserRand': []}

                    data_base['UserQuestions'][callback_query.from_user.id]['UserChat'] = str(callback_query.from_user.id)
                try:
                    user_rand = data_base['UserQuestions'][callback_query.from_user.id]['UserRand']
                except:
                    data_base['UserQuestions'][callback_query.from_user.id]['UserRand'] = [
                    ]
                    user_rand = data_base['UserQuestions'][callback_query.from_user.id]['UserRand']

                # <-- Если сгенерированного вопроса нет в списке заданных вопросов, то его мы опубликуем
                if str(number) not in user_rand:
                    user_rand.append(str(number))
                else:
                    continue

                data_base['BotUsers'][callback_query.from_user.id]['UserRand'] = str(
                    number)

                t += 1
            except Exception as ty:
                print(ty)

        # --- Делаем запрос в БД с целью узнать число в BotUsers->UserRand, UserRowQuestions ------ #
        results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], \
                  data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions']

        fs = results  # <-- тут мы имеем сразу UserRand и UserRowQuestions
        # sc = re.findall(r'\b\d+\b', fs) #<--- распарсиваем их чтоб можно было выбрать, но надо ли?
        print('Номер вопроса =', int(fs[0])+1, 'из', int(fs[1]))

        # ----- формируем сообщение для отправки вопроса ------ #
        question_dict = sheet[int(fs[0])]

        # Формируем сообщение
        message_question = f'<b>Вопрос</b>: {question_dict["Вопрос"]}'
        number_question = 1  # Номер вопроса

        #Перебираем каждый ключ в словаре с вопросом
        for i in question_dict:
            if 'Вопрос' not in i and question_dict[i] != 'stop' and 'Ответ' not in i:
                message_question += f"\n<b>{number_question}</b>. {question_dict[i]}"
                number_question += 1
        # ----------------------------------------------------- #

        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('Результаты', callback_data='Результаты')
        itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')

        markup.add(itembtn1)
        markup.add(itembtn2)

        message_question += text.instruction

        message_id = bot.send_message(callback_query.from_user.id, message_question, parse_mode='HTML', reply_markup=markup)

        save_message_id['message_text'][callback_query.from_user.id] = message_question

        # сохраняем ID заданного вопроса
        save_message_id['check_answer'][callback_query.from_user.id] = message_id.message_id
        # Указываем что тест еще выполняется (для обработки текстового сообщения)
        callback_check[callback_query.from_user.id] = 'tests'
    
    # try:
    #     print('results[0][1] = ', results[1])
    # except:
    #     pass


def answers_prk(bot, callback_query):  # <--- Функция отвечающая за поиск и отправку вопросов по кейсам
    print('IN answers_prk')
    
    practicks_data['check_attempt'][callback_query.from_user.id] = '1'

    db = check_product(callback_query)

    name_sheet = int(a[callback_query.from_user.id])  # <--- Получаем название вкладки (продукта) в таблице

    sheets_name = list(db.keys())

    name_sheet = sheets_name[name_sheet]

    sheet = db[name_sheet]  # <--- Загружаем все вопросы во вкладке, имя которой узнали выше


    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    if str(results[1]) == 'None':
        data_base['BotUsers'][callback_query.from_user.id]['UserPage'] = str(a[callback_query.from_user.id])
        data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'] = len(sheet)

    data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'] = 'None'

    results = int(data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'])

    try:
        ress = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand'])  # смотрим сколько всего вопросов было
    except:
        ress = 0 

    print('ress = ', ress)

    if ress == results:  # <--- Если ответил на все вопросы
        print('Task complete!')

        results_cmpl = data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'], \
                       data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns']

        sc = results_cmpl
        results_cmpl = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand'])
        ans_q = results_cmpl

        bot.send_message(callback_query.from_user.id, f'Ты выполнил все кейсы! \n'
                                                      f'\nКоличество кейсов, которые были заданы: {str(ans_q)}.'
                                                      f'\nПравильных ответов: {int(sc[1])}.')
        callback_check[callback_query.from_user.id] = 'end'

    else:  # <--- Если ответил не на все вопросы
        t = 0
        while t != 1:
            try:  # <--- Если номер вопроса получится тем же на который уже был ответ то получим исключение
                # --------------- Ниже мы получаем рандомное число вопроса, и записываем егов BotUsers UserRand ------- #
                max_row = len(sheet)
                number = random_question(callback_query.from_user.id, max_row)  # <--- генерируем случайное число чтобы получить вопрос

                try:
                    data_base['UserQuestions'][callback_query.from_user.id]['UserChat'] = str(callback_query.from_user.id)
                except:
                    data_base['UserQuestions'][callback_query.from_user.id] = {'UserChat': '0',
                                                                               'UserRand': []}

                    data_base['UserQuestions'][callback_query.from_user.id]['UserChat'] = str(callback_query.from_user.id)
                try:
                    user_rand = data_base['UserQuestions'][callback_query.from_user.id]['UserRand']
                except:
                    data_base['UserQuestions'][callback_query.from_user.id]['UserRand'] = []
                    user_rand = data_base['UserQuestions'][callback_query.from_user.id]['UserRand']

                if str(number) not in user_rand:
                    user_rand.append(str(number))

                else:
                    continue
                data_base['BotUsers'][callback_query.from_user.id]['UserRand'] = str(number)

                t += 1
            except Exception as ty:
                print(ty)

        # --- Делаем запрос в БД с целью узнать число в BotUsers->UserRand, UserRowQuestions ------ #
        results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], \
                  data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions']

        fs = results  # <-- тут мы имеем сразу UserRand и UserRowQuestions
        print('Номер вопроса = ', int(fs[0]), 'из ', int(fs[1]))

        # ----- формируем сообщение для отправки вопроса ------ #
        question_dict = sheet[int(fs[0])]

        if question_dict.get('Кейс') != None:
            mes_qv = f'{question_dict["Кейс"]}' #Формируем вопрос, чтобы дальше его проверить на недопустимые символы
        else:
            mes_qv = f'{question_dict["Вопрос"]}' #Формируем вопрос, чтобы дальше его проверить на недопустимые символы

        if save_check['wic_search'][callback_query.from_user.id] == True: #Смотрим активна ли переменная Поиск знаний
            message_question = '' #Задача убрать слово "Кейс" из сообщения в вопросе
        else:
            message_question = f'<b>Кейс</b>: '

        if '<' in mes_qv or '>' in mes_qv: #Ищем есть ли в вопросе знак <, он вызывает конфликт при parse_mode=HTML
            for i in mes_qv: #Пробегаем по каждому символу в вопросе
                if i == '<':
                    i = '&lt' #Если нашли этот знак то меняем его на &lt
                message_question += i #Добавляем каждую букву к итоговому сообщению
        else: #Если символа такого в вопросе нет, то к итоговому сообщению добавим сразу вопрос
            message_question += mes_qv

        message_question += f'\n\nПиши правильные ответы в соответствии с требованиями вопросов. Точку в конце не ставь.'

        # Ниже уже делаем запрос к екселю через chr получаем букву столбика и смотрим что в строке (номер вопроса)

        # ----------------------------------------------------- #

        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('Результаты', callback_data='Результаты')
        itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')

        markup.add(itembtn1)
        markup.add(itembtn2)

        if question_dict.get('Вложение') != None:  # <-- Смотрим на столбик "С", ищем путь к файлу для отправки. Если есть то

            file_id[callback_query.from_user.id] = file_dir
            file_id[callback_query.from_user.id] = f'{file_id[callback_query.from_user.id]}{question_dict["Вложение"]}'

            try:
                with open(file_id[callback_query.from_user.id], 'rb') as file:
                    if file_id[callback_query.from_user.id].split('.')[-1] in ('png', 'jpg', 'jpeg', 'bmp'):
                        message_id = bot.send_photo(callback_query.from_user.id, file, reply_markup=markup, caption=message_question, parse_mode='HTML')
                    else:
                        message_id = bot.send_document(callback_query.from_user.id, file, reply_markup=markup, caption=message_question, parse_mode='HTML')

            except:
                pass

            del file_id[callback_query.from_user.id]
        else: #<--- Если файл не должен отправляться
            message_id = bot.send_message(callback_query.from_user.id, message_question, parse_mode='HTML', reply_markup=markup)

        save_message_id['message_text'][callback_query.from_user.id] = message_question
        save_message_id['check_answer'][callback_query.from_user.id] = message_id.message_id  # сохраняем ID заданного вопроса
        callback_check[callback_query.from_user.id] = 'practicks'

    print('results[0][1] = ', results[1])


def true_ans(callback_query):  # <--- Функция отвечает за запись правильных ответов по тестам, чтобы в дальнейшем сравнить с тем что написал пользователь
    print('IN true_ans')
    
    ans[callback_query.from_user.id] = []

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    print('Номер вопроса =', int(results[0]), ', номер вкладки в экселе =', int(results[1]), 'ID пользователя =', str(callback_query.from_user.id))

    db = check_product(callback_query)

    sheets_name = list(db.keys()) #Получаем все названия листов

    sheet_name = sheets_name[int(results[1])] #Получаем название листа

    sheet = db[sheet_name]

    question_dict = sheet[int(results[0])]

    for i in question_dict:
        if 'Ответ' in i and 'stop' not in i and 'stop' != question_dict[i]:
            ans[callback_query.from_user.id].append(str(question_dict[i]))

    print('правильные ответы - ', ans[callback_query.from_user.id])
    return ans[callback_query.from_user.id]


def true_ans_prk(callback_query):  # <--- Функция отвечает за запись правильных ответов по тестам, чтобы в дальнейшем сравнить с тем что написал пользователь
    print('IN true_ans_prk')
    
    ans[callback_query.from_user.id] = []
    ans['lower'][callback_query.from_user.id] = []

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    print('Номер вопроса = ', int(results[0]), ', номер вкладки в экселе = ', int(results[1]))

    db = check_product(callback_query)

    sheets_name = list(db.keys()) #Получаем все названия листов

    sheet_name = sheets_name[int(results[1])] #Получаем название листа

    sheet = db[sheet_name]

    question_dict = sheet[int(results[0])]

    question_dict = (str(question_dict['Ответ']))

    for i in question_dict.split(';'):
        ans['lower'][callback_query.from_user.id].append(i)
        ans[callback_query.from_user.id].append(i.strip().upper())

    print('Правильные ответы -', ans[callback_query.from_user.id])

    return ans[callback_query.from_user.id], ans['lower'][callback_query.from_user.id]


def continue_(bot, message):  # <--- функция обработки простых текстовых сообщений
    print('IN continue_')

    if callback_check.get(message.chat.id) in ('tests', 'practicks', 'admin'):  # Если пользователь не нажимал "Сообщить об ошибке"
        print('IF tests,practicks,admin')
        try:
            data_base['BotUsers'][message.chat.id]['UserAnswer'] = str(message.text)
        except:
            data_base['BotUsers'][message.chat.id] = {'UserAnswer': 'None'}
            data_base['BotUsers'][message.chat.id]['UserAnswer'] = str(message.text)



    elif callback_check[message.chat.id] == '1':  # Если пользователь нажал на сообщить об ошибке
        print('IF 1')
        bot.send_message(message.chat.id, 'Ты еще не выбрал о какой ошибке хочешь сообщить. Если не хочешь сообщать, нажми «Отмена».')
        

    elif callback_check[message.chat.id] == '2':  # Если пользователь нажал на сообщить об ошибке и выбрал "о технческой ошибке"
        print('IF 2')
        text_error = 'Сообщение о технической ошибке: '
        bot.send_message(fafa_id, text=f'{text_error}{message.text}\nОб ошибке сообщил - @{message.from_user.username}')
        bot.send_message(message.chat.id, text.tech_error_msg)

        callback_check[message.from_user.id] = save_check[message.from_user.id]

    elif callback_check[message.chat.id] == '3':  # Если пользователь нажал на сообщить об ошибке и выбрал "об ошибке в вопросе"
        print('IF 3')
        if tests_data[message.chat.id] == 'DD':
            product = 'Диадок'

        elif tests_data[message.chat.id] == 'EDI':
            product = 'ЕДИ'

        elif tests_data[message.chat.id] == 'extrn':
            product = 'Экстерн'

        elif tests_data[message.chat.id] == 'UC':
            product = 'УЦ'

        elif tests_data[message.chat.id] == 'MK':
            product = 'МК'

        elif tests_data[message.chat.id] == 'FMS':
            product = 'ФМС'

        elif tests_data[message.chat.id] == 'OFD':
            product = 'ОФД'

        elif tests_data[message.chat.id] == 'BUH':
            product = 'Бухгалтерия'

        elif tests_data[message.chat.id] == 'ELB':
            product = 'Эльба'
        
        elif tests_data[message.chat.id] == 'KF':
            product = 'Фокус'       
        
        elif tests_data[message.chat.id] == 'WIC':
            product = 'WIC'
        
        elif tests_data[message.chat.id] == 'OTHER':
            product = 'Вн. сервисы'

        elif tests_data[message.chat.id] == 'INST':
            product = 'Установка'
        

        text_error = f'<b>Лёха, конс нашел ошибку в вопросе!</b>\nОтдел: {product}.\n\n{callback_check["text"][message.chat.id]}'
        bot.send_message(alex_id, text=f'{text_error}Комментарий: {message.text}\nОб ошибке сообщил - @{message.from_user.username}', parse_mode='HTML')

        bot.send_message(message.chat.id, text.tech_error_msg)

        callback_check[message.from_user.id] = save_check[message.from_user.id]

    print('IN continue_ END')

def check_answer(bot, callback_query):  # Функция прооверяет правильность введённого ответа от пользователя по тестам
    print('IN check_answer')
    print(callback_query.from_user.id)

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    print('1 if')
    if results[1] == 'None':  # <---смотрим в БД пустой ли ответ
        bot.edit_message_text(text.empty_answer, chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
    else:
        print('2 if')

        markup = types.InlineKeyboardMarkup()
        itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')
        markup.add(itembtn2)
        bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=save_message_id['check_answer'][callback_query.from_user.id],
                              text=save_message_id['message_text'][callback_query.from_user.id], reply_markup=markup, parse_mode='HTML')

        check_true_ans = true_ans(callback_query)

        if sorted(set(map(str, results[1]))) == check_true_ans:
            bot.edit_message_text("Красава!", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
            data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns'] = str(int(results[2]) + 1)

        else:
            check_true_ans_1 = ''
            for i in check_true_ans:
                check_true_ans_1 += f'{i}'
            if len(check_true_ans) == 1:
                bot.edit_message_text(f"Неправильно! Учи! \nПравильный вариант: {check_true_ans_1}.", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
            else:
                bot.edit_message_text(f"Неправильно! Учи! \nПравильные варианты: {check_true_ans_1}.", chat_id=callback_query.from_user.id,
                                      message_id=save_message_id['message_id'][callback_query.from_user.id])
        data_base['BotUsers'][callback_query.from_user.id]['UserRand'] = str(int(results[0]) + 1)

        h = 0
        while h != 1:
            answers(bot, callback_query)
            h += 1


def check_answer_prk(bot, callback_query):  # Функция прооверяет правильность введённого ответа от пользователя по кейсам
    print('IN check_answer_prk')
    
    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserPage']
    print('1 if')

    if results[1] == 'None':  # <---смотрим в БД пустой ли ответ
        bot.edit_message_text("Ты вводишь пустой ответ. Пока не напишешь варианты ответа, дальше не двинемся.",
                              chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
        return
    else:
        print('2 if')
        db_results = str(results[1])

        markup = types.InlineKeyboardMarkup()
        itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')
        markup.add(itembtn2)
        try:
            bot.edit_message_caption(chat_id=callback_query.from_user.id, message_id=save_message_id['check_answer'][callback_query.from_user.id],
                                  caption=save_message_id['message_text'][callback_query.from_user.id], reply_markup=markup, parse_mode='HTML')
        except:
            bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=save_message_id['check_answer'][callback_query.from_user.id],
                                     text=save_message_id['message_text'][callback_query.from_user.id], reply_markup=markup, parse_mode='HTML')

        # Проверям правильный ли ответ
        check_true_ans_prk, lower_ans_prk = true_ans_prk(callback_query)
        if db_results.upper() in check_true_ans_prk:
            bot.edit_message_text("Красава!", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
            data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns'] = str(int(results[2]) + 1)
        else:
            if practicks_data['check_attempt'][callback_query.from_user.id] == '1':
                markup = types.InlineKeyboardMarkup()
                itembtn1 = types.InlineKeyboardButton('Результаты', callback_data='Результаты')
                itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')

                markup.add(itembtn1)
                markup.add(itembtn2)

                message_id = bot.edit_message_text("Неправильно! У тебя есть еще одна попытка.", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id], reply_markup=markup)
                practicks_data['check_attempt'][callback_query.from_user.id] = '0'
                data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'] = 'None'
                save_message_id['check_answer'][callback_query.from_user.id] = message_id.message_id
                return
            else:
                bot.edit_message_text(f"Неправильно! Учи!\nПравильный ответ: {lower_ans_prk[0]}.", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])

        data_base['BotUsers'][callback_query.from_user.id]['UserRand'] = str(int(results[0]) + 1)
        h = 0
        while h != 1:
            answers_prk(bot, callback_query)
            h += 1

def res(bot, callback_query):  # Функция публикует результат
    print('IN res')

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns']

    sc = results
    results = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand'])
    ans_q = results

    bot.send_message(text=f'Результаты! \nКоличество всех вопросов: {int(sc[0])}. '
                          f'\nКоличество вопросов, которые были заданы: {str(ans_q)}.'
                          f'\nПравильных ответов: {int(sc[1])}.',
                     chat_id=callback_query.from_user.id)

    markup = types.ReplyKeyboardMarkup()
    itembtn_back = types.KeyboardButton('В меню')
    markup.add(itembtn_back)


# ------------------------------- Обработка Inline клавиатуры ---------------------------------------#
def send_error(bot, callback_query):  # <--- Меню Inline "Сообщить об ошибке"
    print('IN send_error')
    error_markup = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('О технической ошибке', callback_data='Техническая ошибка')
    itembtn2 = types.InlineKeyboardButton('Об ошибке в вопросе', callback_data='Текстовая ошибка')
    itembtn3 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    error_markup.add(itembtn1, itembtn2)
    error_markup.add(itembtn3)
    bot.send_message(callback_query.from_user.id, text.error_choice, reply_markup=error_markup)
    save_check[callback_query.from_user.id] = callback_check[callback_query.from_user.id]

    callback_check[callback_query.from_user.id] = '1'  # Присваиваем ИД переменную, чтобы дальше фильтровать
    callback_check['text'][callback_query.from_user.id] = callback_query.message.text.split('Пиши')[0]

def query_data_handler(bot, data):
#   print('IN query_data_handler')
  @bot.callback_query_handler(func=lambda callback_query: callback_query.data == data)  # <--- кнопка отмены
  def func_handler(callback_query: CallbackQuery):

    if data == 'Отмена':
      bot.answer_callback_query(callback_query.id)
      bot.edit_message_text('Действие отменено.', chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

      if callback_check.get(callback_query.from_user.id) in ('tests', 'practicks', 'admin'):
          del callback_check[callback_query.from_user.id]

      elif callback_check.get(callback_query.from_user.id) in ('1', '2', '3'):
        callback_check[callback_query.from_user.id] = save_check[callback_query.from_user.id]

    elif data == 'Техническая ошибка':
      markup = types.InlineKeyboardMarkup()
      itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')
      markup.add(itembtn9)

      bot.answer_callback_query(callback_query.id)
      bot.edit_message_text('Опиши полностью техническую ошибку, которая у тебя произошла.', chat_id=callback_query.from_user.id,
                            message_id=callback_query.message.message_id, reply_markup=markup)

      callback_check[callback_query.from_user.id] = '2'  # Присваиваем ИД переменную, чтобы дальше фильтровать
    
    elif data == 'Текстовая ошибка':
      markup = types.InlineKeyboardMarkup()
      itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')
      markup.add(itembtn9)

      bot.answer_callback_query(callback_query.id)
      bot.edit_message_text('Опиши полностью ошибку в вопросе.', chat_id=callback_query.from_user.id,
                            message_id=callback_query.message.message_id, reply_markup=markup)

      callback_check[callback_query.from_user.id] = '3'  # Присваиваем ИД переменную, чтобы дальше фильтровать

    elif data == 'Назад':
      try:
          del practicks_data[callback_query.from_user.id]
      except:
          pass

      markup_1 = types.InlineKeyboardMarkup()

      itembtn1 = types.InlineKeyboardButton('Тесты', callback_data='Тесты')
      itembtn2 = types.InlineKeyboardButton('Кейсы', callback_data='Кейсы')
      itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

      markup_1.add(itembtn1, itembtn2)
      markup_1.add(itembtn12)

      try:
          bot.edit_message_text(chat_id=callback_query.from_user.id, text="Какой вид обучения тебя интересует?",
                                message_id=callback_query.message.message_id, reply_markup=markup_1)
      except Exception as E:
          print(E.args)

      bot.answer_callback_query(callback_query.id)

    elif data == 'Обновить таблицы':
      global db_data

      db_data = {}
      db_data = get_db_excel.get_question()

      bot.answer_callback_query(callback_query.id)

      bot.send_message(chat_id=callback_query.from_user.id, text='Таблицы успешно обновлены!')
      print('Таблицы были обновлены!')

    elif data == 'Зарегистрировать пользователя':
        add_user(callback_query, data_base)
        bot.answer_callback_query(callback_query.id)

    elif data == 'Удалить пользователя':
        rm_user(callback_query, data_base)
        bot.answer_callback_query(callback_query.id)

# --------------------Обработка вложенных меню Диадок------------------------------------
    elif data == 'Диадок.Тесты.Web':
        test_diadoc_web(bot, callback_query)
    
    elif data == 'Диадок.Тесты.Интеграция':
        test_diadoc_integrtion(bot, callback_query)

    # elif data == 'Диадок.Тесты.Роуминг':
    #     test_diadoc_roaming(bot, callback_query)

    elif data == 'DD.Case.Admin':
        prk_diadoc_admin(bot, callback_query)
    
    elif data == 'DD.Case.Web':
        prk_diadoc_web(bot, callback_query)
    
    elif data == 'DD.Case.Roam':
        prk_diadoc_roam(bot, callback_query)   

# --------------------------- Новая часть меню админа -------------------------------------------

    elif data == 'Рассылка':
        sending_menu(bot, callback_query)

    elif data == 'База сообщений':
        sending_menu_base(bot, callback_query)

    elif data == 'Календарь рассылок':
        sending_menu_calendar(bot, callback_query)

    elif data == 'Начать новый набор':
        sending_menu_start_new_wave(bot, callback_query)
        
    elif data == 'Создать сообщение':
        message = bot.edit_message_text('Отправь текст нового сообщения.', 
                            chat_id=callback_query.from_user.id,
                            message_id=callback_query.message.message_id)
        bot.register_next_step_handler(message, sending_menu_base_add_to_sql)
        
    elif data == 'Просмотреть все сообщения':
            connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
            cursor = connection.cursor()
            SQLQuery = sql_queries.get_all_info_from_messages()
            cursor.execute(SQLQuery)
            all_messages = cursor.fetchall()
            for i in range(len(all_messages)):
                bot.send_message(callback_query.from_user.id, 
                                'Рассылка №' + str(all_messages[i][0]) + ':\n' + str(all_messages[i][1]), 
                                parse_mode='Markdown', disable_web_page_preview=True)
                time.sleep(0.1)
        
    elif data == 'Изменить сообщение':
        message = bot.edit_message_text("Отправь номер сообщения и новый текст, разделив их звездочкой. Пример: 5*Новый текст.\n"\
                            "Обрати внимание, что символ * - это разделитель и его нельяз использовать в тексте рассылки.\n"\
                            "При необходимоести указать символ ' необходимо указать его дважды - WIC''a.\n"\
                            "Гиперссылка указывается как [слово](http://www.example.com/).",
                            chat_id=callback_query.from_user.id,
                            message_id=callback_query.message.message_id)
        bot.register_next_step_handler(message, sending_menu_base_change)
        
    elif data == 'Задать день и номер рассылки':
        message = bot.edit_message_text("Отправь день и новый номер рассылки, разделив их звездочкой. Пример: 5*11 \n"\
                                "Обрати внимание, что символ * - это разделитель и его нужно указать один раз.\n"\
                                "Ты можешь указать любой номер рассылки, но не делай так. Пиши только те, что уже добавил.", 
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)
        bot.register_next_step_handler(message, edit_sending_menu_calendar)

    elif data == 'Просмотреть расписание':
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.get_all_info_from_calendar()
        cursor.execute(SQLQuery)
        all_messages = cursor.fetchall()
        group_calendar = str()
        for i in range(len(all_messages)):
            group_calendar = group_calendar + 'День '+ str(all_messages[i][0]) + ' - Номер рассылки: ' + str(all_messages[i][1]) + '\n'
        bot.send_message(callback_query.from_user.id, group_calendar)


    elif data == 'Очистить день от рассылки':
        message = bot.edit_message_text('Отправь номер дня в который нужно убрать рассылку.', 
                    chat_id=callback_query.from_user.id,
                    message_id=callback_query.message.message_id)
        bot.register_next_step_handler(message, sending_menu_calendar_delete)

    # По хорошему нужно сделать проверку последней даты для предотвращения повторного нажатия
    elif data == 'Начать новый набор!':
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.create_new_wave()
        cursor.execute(SQLQuery) 
        connection.commit()
        connection.close()
        bot.send_message(callback_query.from_user.id, 'Добавлен новый набор с ' + str(dt.date.today()) + '.')

    # ? Вызов как с другими функциями не получается, поскольку Admin_menu принимает не callback_query, message
    # ? Пока опция заблокрирована
    elif data == 'Вернуться в Меню админа':
        Admin_menu(bot, callback_query)

    elif data == 'Вернуться в Рассылки':
        sending_menu(bot, callback_query)
    
    elif data == 'Вернуться в База сообщений':
        sending_menu_base(bot, callback_query)
    
    elif data == 'Вернуться в Календарь рассылок':
        sending_menu_calendar(bot, callback_query)

# -----------------------------Конец новой части меню------------------------------------------

    elif data == 'Результаты':
        res(bot, callback_query)

    print('IN query_data_handler END')

add_modules()
query_data_handler(bot, 'Отмена')
query_data_handler(bot, 'Техническая ошибка')
query_data_handler(bot, 'Текстовая ошибка')
query_data_handler(bot, 'Назад')
query_data_handler(bot, 'Обновить таблицы')
query_data_handler(bot, 'Зарегистрировать пользователя')
query_data_handler(bot, 'Удалить пользователя')

query_data_handler(bot, "Диадок.Тесты.Web")
query_data_handler(bot, "Диадок.Тесты.Интеграция")
# query_data_handler(bot, "DD.Tests.Геракл")
query_data_handler(bot, "DD.Tests.Roam")

query_data_handler(bot, "DD.Case.Admin")
query_data_handler(bot, "DD.Case.Web")
query_data_handler(bot, "DD.Case.Roam")

query_data_handler(bot, "DD.Case.Admin.АдминкаДД")
query_data_handler(bot, "DD.Case.Admin.АдминкаПР")
query_data_handler(bot, "DD.Case.Admin.Билли")

query_data_handler(bot, "DD.Case.Web.Пользователи")
query_data_handler(bot, "DD.Case.Web.Контрагенты")
query_data_handler(bot, "DD.Case.Web.Документы")

query_data_handler(bot, "DD.Case.Web.Настройки и реквизиты")
query_data_handler(bot, "DD.Case.Web.Маршруты")

query_data_handler(bot, 'Рассылка')
query_data_handler(bot, 'База сообщений')
query_data_handler(bot, 'Календарь рассылок')
query_data_handler(bot, 'Начать новый набор')
query_data_handler(bot, 'Число сообщений')
query_data_handler(bot, 'Создать сообщение')
query_data_handler(bot, 'Просмотреть все сообщения')
query_data_handler(bot, 'Изменить сообщение')
query_data_handler(bot, 'Число рассылок')
query_data_handler(bot, 'Задать день и номер рассылки')
query_data_handler(bot, 'Просмотреть расписание')
query_data_handler(bot, 'Очистить день от рассылки')
query_data_handler(bot, 'Начать новый набор!')
query_data_handler(bot, 'Вернуться в Меню админа')
query_data_handler(bot, 'Вернуться в Рассылки')
query_data_handler(bot, 'Вернуться в База сообщений')
query_data_handler(bot, 'Вернуться в Календарь рассылок')

query_data_handler(bot, 'Результаты')
