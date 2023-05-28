import telebot
from config import *

# По умолчанию тестовый режим включен. При запуске в продакшн устанавливаем значение False
def test_mode():
    return True

# Возвращает бота с нужным токеном в зависимости от режима
def get_token(mode):
    if mode == True:
        return telebot.TeleBot(test_token, threaded=False) # Тестовый бот
    elif mode == False:
        return telebot.TeleBot(prod_token, threaded=False) # Рабочий бот
    else:
        print('Что-то пошло не так! Не удалось определить режим запуска!')

# Возвращает имя сервера в зависимости от режима
def get_server(mode):
    if mode == True:
        return test_server_name # тестовый сервер
    else:
        return prod_server_name # раюочий сервер

# Возвращает админские id в зависимости от режима
def get_admins(mode):
    if mode == True:
        return [str(admins[1]), str(admins[1])]
    else:
        return [str(admins[0]), str(admins[1])]
