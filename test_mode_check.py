import telebot

def test_mode():
    return False


def get_token(mode):
    if mode == True:
        return telebot.TeleBot('2075877718:AAHdfH9_PL2rBX-8uBIvFsIh-tdnUnHNA98',  threaded=False)    
    else:
        return telebot.TeleBot('1253732018:AAESPvgR9YfmnTAHtHRMWJ8tjOmApA_qSyI',  threaded=False)


def get_server(mode):
    if mode == True:
        return "ASUS\SQLEXPRESS" # тестовый сервер
    else:
        return "K1606047" # сервер продакшена


def get_admins(mode):
    if mode == True:
        return ['1325029854', '1325029854', '1325029854']
    else:
        return ['233770916', '391368365', '1325029854']
