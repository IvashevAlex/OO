# Данный файл инициилизирует Кнопки отделов и их разделов + доп кнопки

from modul_for_bot import *

bot = telebot.TeleBot('1253732018:AAESPvgR9YfmnTAHtHRMWJ8tjOmApA_qSyI',  threaded=False) # - @OOHelper


reg_user(bot)
del_user(bot)
update_tables(bot)
cancel_error(bot) #Кнопка Отмена
tehn_error(bot)
txt_error(bot)
lesten_res(bot)
btn_back_menu(bot) #Кнопка назад

#---- инициализируем меню тестов\кейсов -----#
tests(bot)
praktics(bot)

#----- Главное меню -------#
Inst_menu("Установка", bot)
DD_menu("Диaдoк", bot)
EDI_menu("Ритейл", bot)
ext_menu("Экстерн", bot)
UC_menu("УЦ", bot)
M_menu("Maркет", bot)
OFD_menu("OФД", bot)
FMS_menu("ФMС", bot)
Buh_menu("Бухгалтерия", bot)
Elba_menu("Эльба", bot)


#------ Кнопки Установки -----#
quest('Компоненты для работы с ЭП', 0, bot)
quest('Запрос КЭП', 1, bot)
quest('Работа с ЭП', 2, bot)
quest('КЭП для ЕГАИС', 3, bot)
quest('Сертификаты УЦ', 4, bot)
quest('Работа с ЭП не на Windows', 5, bot)
quest('DSS', 6, bot)
quest('Установка общее', 7, bot)

#-----------Кнопки Диадок --------#
quest("Web.Диадок", 0, bot)
quest("Модуль.Диадок", 2,bot)
quest("Роуминг.Диадок", 4,bot)
quest("Коннекторы.Диадок", 6,bot)

#---- Кнопки КЭ ------#
quest('Интерфейс', 0, bot)
quest('Режим работы', 2, bot)
quest('ФНС', 4, bot)
quest('ИОН', 6, bot)
quest('Таблица отчетности', 8, bot)
quest('Письма ФНС', 10, bot)
quest('ПФР', 12, bot)
quest('НДС и требования', 14, bot)
quest('НДФЛ', 16, bot)
quest('Росстат', 18, bot)
quest('РСВ', 20, bot)
quest('Заполнение ПФР', 22, bot)

#-----Кнопки Бухгалтерия -----#
quest('ОСНО', 0, bot)
quest('ЕНВД', 1, bot)
quest('УСН', 2, bot)
quest('ОПФ. Реквизиты. Взносы ИП', 3, bot)
quest('Сотрудники', 4, bot)
quest('БО и бухучет', 5, bot)
quest('Работа в сервисе', 6, bot)

#------Кнопки Эльба-------#
quest('Реквизиты и ОПФ', 0, bot)
quest('Налоги и взносы', 1, bot)
quest('Сотрудники.Эльба', 3, bot)
quest('Работа в сервисе.Эльба', 5, bot)
quest('БО.Эльба', 7, bot)

#----- Кнопки ОФД --------#
quest("ОФД", 0, bot)
quest("ККТ", 2, bot)
quest("API", 4, bot)
quest("1C", 6, bot)

#----- Кнопки EDI (Ритейл) -----#
quest("EDI Web", 0, bot)
quest("EDI 1C", 2, bot)
quest("Поставки", 4, bot)
quest("Меркурий", 6, bot)

#--- Кнопки ФМС -----#
quest("ФМС", 0, bot)
quest("Отель", 2, bot)
quest("Фокус", 4, bot)
quest("Фокус API", 6, bot)
quest("Компас", 8, bot)

#----- Кнопки УЦ -----#
quest("Проекты УЦ", 0, bot)
quest("ЭТП", 2, bot)
quest("ИС", 4, bot)
quest("Закупки", 6, bot)
quest("Реестро", 8, bot)
quest("Контур.Торги", 9, bot)
quest("Декларант", 10, bot)
quest("Школа", 12, bot)

#----- Кнопки Маркета -----#
quest("Маркет", 0, bot)
quest("ЕГАИС", 2, bot)
quest("КМК", 4, bot)
quest("Меркурий в Маркете", 6, bot)
quest("Маркировка в Маркете", 8, bot)
quest("РАР", 10, bot)
#--------------------#