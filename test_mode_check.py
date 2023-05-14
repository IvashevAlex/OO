import telebot

# По умолчанию тестовый режим включен. При запуске в продакшн устанавливаем значение False
def test_mode():
    return True

# Возвращает бота с нужным токеном в зависимости от режима
def get_token(mode):
    if mode == True:
        return telebot.TeleBot('2075877718:AAHdfH9_PL2rBX-8uBIvFsIh-tdnUnHNA98',  threaded=False) # Тестовый бот
    elif mode == False:
        return telebot.TeleBot('1253732018:AAESPvgR9YfmnTAHtHRMWJ8tjOmApA_qSyI',  threaded=False) # Рабочий бот
    else:
        print('Что-то пошло не так! Не удалось определить режим запуска!')

# Возвращает имя сервера в зависимости от режима
def get_server(mode):
    if mode == True:
        # return "ASUS\SQLEXPRESS" # тестовый сервер старый ПК
        return "MSI\SQLEXPRESS" # тестовый сервер новый ПК
        # Добавить имя нового сервера после настройки 
    else:
        return "K1606047" # рабочий сервер

# Возвращает админские id в зависимости от режима
def get_admins(mode):
    if mode == True:
        return ['1325029854', '1325029854', '1325029854']
    else:
        return ['233770916', '391368365', '1325029854']
