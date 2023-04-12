import json

def get_question():
    print('IN get_question')
    list_tables = ['УЦ', 'ФМС', 'Маркет', 'Ритейл', 'Диадок', 'KE', 'Бухгалтерия', 
    'Эльба', 'ОФД', 'Установка', 'WIC', 'Вн. сервисы', 'Фокус']


    name_dict = {
        'УЦ': 'UC',
        'ФМС': 'FMS',
        'Маркет': 'MK',
        'Ритейл': 'EDI',
        'Диадок': 'DD',
        'KE': 'KE',
        'Бухгалтерия': 'BH',
        'Эльба': 'ELB',
        'ОФД': 'OFD',
        'Установка': 'INST',
        'WIC': 'WIC',
        'Вн. сервисы' : 'OTHER',
        'Фокус' : 'KF'
    }

    bd_questions = {}

    for i in list_tables:
        with open(f'Data/ExcelToJSON/{i}.json', 'r', encoding='utf-8') as file:
            bd_questions[name_dict[i]] = json.load(file)
        print(list_tables[i],'... Ok')
    return bd_questions
