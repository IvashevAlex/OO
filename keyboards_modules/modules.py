import modul_for_bot
from WhiteList import bot

# 0, 2, ... - тесты
# 1, 3, ... - кейсы. Если чередование строгое, то в данном файле они не прописываются
# Если последоавтельность произвольная, то происываются все вкладки (например Диадок)

def add_modules():
    # #--- Кнопки ФМС -----#

    modul_for_bot.quest("ФМС", 0, bot)
    modul_for_bot.quest("Отель", 2, bot)


    #------ Кнопки WIC ------#
    modul_for_bot.quest('WIC.Поиск_знаний', 0, bot)
    modul_for_bot.quest('WIC.Кейсы', 1, bot)


    #------ Кнопки Установки -----#
    modul_for_bot.quest('Сертификаты и носители', 0, bot)
    modul_for_bot.quest('Работа с электронной подписью', 1, bot)
    # modul_for_bot.quest('Компоненты для работы с ЭП', 0, bot)
    # modul_for_bot.quest('Запрос КЭП', 1, bot)
    # modul_for_bot.quest('Работа с ЭП', 2, bot)
    # modul_for_bot.quest('КЭП для ЕГАИС', 3, bot)
    # modul_for_bot.quest('Сертификаты УЦ', 4, bot)
    # modul_for_bot.quest('Работа с ЭП не на Windows', 5, bot)
    # modul_for_bot.quest('DSS', 6, bot)
    # modul_for_bot.quest('Установка общее', 7, bot)


    #------- Кнопки внутр сервисы ------#
    modul_for_bot.quest('Билли', 0, bot)
    modul_for_bot.quest('КабУЦ', 1, bot)
    # modul_for_bot.quest('Клиент-Сервис', 2, bot)


    #-----------Кнопки Диадок --------#
    modul_for_bot.quest("DD.Tests.Web.Общее", 0, bot)
    modul_for_bot.quest("DD.Tests.Web.Документы", 1, bot)
    modul_for_bot.quest("DD.Tests.Web.Пользователи", 2, bot)
    modul_for_bot.quest("DD.Tests.Web.Контрагенты", 3, bot)
    modul_for_bot.quest("DD.Tests.Web.Настройки", 4, bot)
    modul_for_bot.quest("DD.Tests.Web.Маршруты", 5, bot)
    
    modul_for_bot.quest("DD.Tests.Int.Общие", 6, bot)
    modul_for_bot.quest("DD.Tests.Int.Документы", 7, bot)
    modul_for_bot.quest("DD.Tests.Int.Настройки", 8, bot)
    modul_for_bot.quest("DD.Tests.Int.Ошибки", 9, bot)

    # modul_for_bot.quest("DD.Tests.Геракл", 10, bot)
    modul_for_bot.quest("DD.Tests.Roam", 10, bot)

    modul_for_bot.quest("DD.Case.Admin.АдминкаДД", 11, bot)
    modul_for_bot.quest("DD.Case.Admin.АдминкаПР", 12, bot)
    modul_for_bot.quest("DD.Case.Admin.Билли", 13, bot)

    modul_for_bot.quest("DD.Case.Web.Пользователи", 14, bot)
    modul_for_bot.quest("DD.Case.Web.Контрагенты", 15, bot)
    modul_for_bot.quest("DD.Case.Web.Документы", 16, bot)

    modul_for_bot.quest("DD.Case.Roam.Заявки", 17, bot)
    modul_for_bot.quest("DD.Case.Roam.Мониторинг", 18, bot)


    #---- Кнопки КЭ ------#
    modul_for_bot.quest('Знакомство', 0, bot)
    modul_for_bot.quest('ФНС', 1, bot)
    modul_for_bot.quest('ЕНП', 2, bot)
    modul_for_bot.quest('Мелкие сервисы', 3, bot)
    modul_for_bot.quest('Case.Мелкие', 4, bot)
    modul_for_bot.quest('Test.SFR_pens', 5, bot)
    modul_for_bot.quest('Case.SFR_pens', 6, bot)
    modul_for_bot.quest('Test.SFR_sots', 7, bot)
    modul_for_bot.quest('Case.SFR_sots', 8, bot)
    modul_for_bot.quest('НДС и НДС+', 9, bot)
    modul_for_bot.quest('Case.НДС', 10, bot)
    modul_for_bot.quest('Test.Trebovanie', 11, bot)
    modul_for_bot.quest('Case.Требования', 12, bot)
    modul_for_bot.quest('РСВ', 13, bot)
    modul_for_bot.quest('Case.РСВ', 14, bot)
    modul_for_bot.quest('НДФЛ', 15, bot)
    modul_for_bot.quest('Case.НДФЛ', 16, bot)

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
    modul_for_bot.quest("Школа", 12, bot)


    #----- Кнопки Маркета -----#
    modul_for_bot.quest("Маркет", 0, bot)
    modul_for_bot.quest("ЕГАИС", 2, bot)
    modul_for_bot.quest("КМК", 4, bot)
    modul_for_bot.quest("Меркурий в Маркете", 6, bot)
    modul_for_bot.quest("Маркировка в Маркете", 8, bot)
    modul_for_bot.quest("РАР", 10, bot)


    #----- Кнопки Фокус -----#
    modul_for_bot.quest("Фокус", 0, bot)
    modul_for_bot.quest("Case.Фокус", 1, bot)
    modul_for_bot.quest("API Фокус", 2, bot)
    modul_for_bot.quest("Case.API Фокус", 3, bot)
    modul_for_bot.quest("Компас", 4, bot)
    modul_for_bot.quest("Case.Компас", 5, bot)
    modul_for_bot.quest("KD.Test.Tech", 6, bot)
    modul_for_bot.quest("KD.Case.Tech", 7, bot)
    modul_for_bot.quest("KD.Test.Method", 8, bot)
    modul_for_bot.quest("KD.Case.Method", 9, bot)

    