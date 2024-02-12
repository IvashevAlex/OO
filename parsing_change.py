import json

# Парсит файл data.json 
with open('data.json','r', encoding='utf-8') as file:
    result_dict = json.load(file)

# print(result_dict.keys())

newUsers = result_dict['newUsers']
modifiedUsers = result_dict['modifiedUsers']
firedUsers = result_dict['firedUsers']
lastModifiedDate = result_dict['lastModifiedDate']

N = len(newUsers[0])

for A1 in range(N):
    print('Запись', A1+1, 'из', N)
    print(newUsers[A1]['surname'], newUsers[A1]['firstname'], newUsers[A1]['patronymic'])
    print(newUsers[A1]['status'])
    print(newUsers[A1]['recruited'])

    for A2 in range(len(newUsers[A1]['contacts'])):
        if newUsers[A1]['contacts'][A2]['typeId'] == 11:
            print(newUsers[A1]['contacts'][A2]['value'])
        else:
            pass

    print()

# newUsers_Contacts = newUsers[0].get('contacts')
# firedUsers_email = firedUsers[0].get('email')

# newUsers_len = len(newUsers)
# firedUsers_len = len(firedUsers)


# firedUsers_email_len = len(firedUsers_email)