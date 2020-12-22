import modul_for_bot
from WhiteList import bot

def add_modules():
    # #--- Кнопки ФМС -----#

    modul_for_bot.quest("ФМС", 0, bot)
    modul_for_bot.quest("Отель", 2, bot)
    modul_for_bot.quest("Фокус", 4, bot)
    modul_for_bot.quest("Фокус API", 6, bot)
    modul_for_bot.quest("Компас", 8, bot)


    #------ Кнопки WIC ------#
    modul_for_bot.quest('WIC.Поиск_знаний', 0, bot)
    modul_for_bot.quest('WIC.Кейсы', 1, bot)

    #------ Кнопки Установки -----#
    modul_for_bot.quest('Компоненты для работы с ЭП', 0, bot)
    modul_for_bot.quest('Запрос КЭП', 1, bot)
    modul_for_bot.quest('Работа с ЭП', 2, bot)
    modul_for_bot.quest('КЭП для ЕГАИС', 3, bot)
    modul_for_bot.quest('Сертификаты УЦ', 4, bot)
    modul_for_bot.quest('Работа с ЭП не на Windows', 5, bot)
    modul_for_bot.quest('DSS', 6, bot)
    modul_for_bot.quest('Установка общее', 7, bot)

    #------- Кнопки внутр сервисы ------#
    modul_for_bot.quest('Билли', 0, bot)
    modul_for_bot.quest('КабУЦ', 1, bot)
    modul_for_bot.quest('Клиент-Сервис', 2, bot)

    #-----------Кнопки Диадок --------#
    modul_for_bot.quest("Web.Диадок", 0, bot)
    modul_for_bot.quest("Модуль.Диадок", 2, bot)
    modul_for_bot.quest("Роуминг.Диадок", 4, bot)
    modul_for_bot.quest("Коннекторы.Диадок", 6, bot)
    modul_for_bot.quest("Геракл.Диадок", 7, bot)

    #---- Кнопки КЭ ------#
    modul_for_bot.quest('Интерфейс', 0, bot)
    modul_for_bot.quest('Режим работы', 2, bot)
    modul_for_bot.quest('ФНС', 4, bot)
    modul_for_bot.quest('ИОН', 6, bot)
    modul_for_bot.quest('Таблица отчетности', 8, bot)
    modul_for_bot.quest('Письма ФНС', 10, bot)
    modul_for_bot.quest('ПФР', 12, bot)
    modul_for_bot.quest('НДС и требования', 14, bot)
    modul_for_bot.quest('НДФЛ', 16, bot)
    modul_for_bot.quest('Росстат', 18, bot)
    modul_for_bot.quest('РСВ', 20, bot)
    modul_for_bot.quest('Заполнение ПФР', 22, bot)

    #-----Кнопки Бухгалтерия -----#
    modul_for_bot.quest('ОСНО', 0, bot)
    modul_for_bot.quest('ЕНВД', 1, bot)
    modul_for_bot.quest('УСН', 2, bot)
    modul_for_bot.quest('ОПФ. Реквизиты. Взносы ИП', 3, bot)
    modul_for_bot.quest('Сотрудники', 4, bot)
    modul_for_bot.quest('БО и бухучет', 5, bot)
    modul_for_bot.quest('Работа в сервисе', 6, bot)

    #------Кнопки Эльба-------#
    modul_for_bot.quest('Реквизиты и ОПФ', 0, bot)
    modul_for_bot.quest('Налоги и взносы', 1, bot)
    modul_for_bot.quest('Сотрудники.Эльба', 3, bot)
    modul_for_bot.quest('Работа в сервисе.Эльба', 5, bot)
    modul_for_bot.quest('БО.Эльба', 7, bot)

    #----- Кнопки ОФД --------#
    modul_for_bot.quest("ОФД", 0, bot)
    modul_for_bot.quest("ККТ", 2, bot)
    modul_for_bot.quest("API", 4, bot)
    modul_for_bot.quest("1C", 6, bot)

    #----- Кнопки EDI (Ритейл) -----#
    modul_for_bot.quest("EDI Web", 0, bot)
    modul_for_bot.quest("EDI 1C", 2, bot)
    modul_for_bot.quest("Поставки", 4, bot)
    modul_for_bot.quest("Меркурий", 6, bot)


    #----- Кнопки УЦ -----#
    modul_for_bot.quest("Проекты УЦ", 0, bot)
    modul_for_bot.quest("ЭТП", 2, bot)
    modul_for_bot.quest("ИС", 4, bot)
    modul_for_bot.quest("Закупки", 6, bot)
    modul_for_bot.quest("Реестро", 8, bot)
    modul_for_bot.quest("Контур.Торги", 9, bot)
    modul_for_bot.quest("Декларант", 10, bot)
    modul_for_bot.quest("Школа", 12, bot)

    #----- Кнопки Маркета -----#
    modul_for_bot.quest("Маркет", 0, bot)
    modul_for_bot.quest("ЕГАИС", 2, bot)
    modul_for_bot.quest("КМК", 4, bot)
    modul_for_bot.quest("Меркурий в Маркете", 6, bot)
    modul_for_bot.quest("Маркировка в Маркете", 8, bot)
    modul_for_bot.quest("РАР", 10, bot)
