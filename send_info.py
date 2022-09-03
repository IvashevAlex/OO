import time
from WhiteList import bot

if time.gmtime()[4] % 3 == 0:
    if time.gmtime()[5] < 5:
        print('Пришло время для 3-х минутной рассылки!')
        bot.send_message(5484457194, 'Пришло время для 3-х минутной рассылки!')
        time.sleep(5)
if time.gmtime()[4] % 5 == 0:
    if time.gmtime()[5] < 5:
        print('Пришло время для 5-ти минутной рассылки!')
        bot.send_message(5737229331, 'Пришло время для 5-ти минутной рассылки!')
        time.sleep(5)
