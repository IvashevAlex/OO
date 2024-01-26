import json

with open('data.json','r', encoding='utf-8') as file:
    result_dict = json.load(file)

newUsers = result_dict['newUsers']
firedUsers = result_dict['firedUsers']

newUsers_Contacts = newUsers[0].get('contacts')
firedUsers_email = firedUsers[0].get('email')

newUsers_len = len(newUsers)
firedUsers_len = len(firedUsers)


firedUsers_email_len = len(firedUsers_email)

print('Список новых пользователей:')

# ! удалить начало вида https://t.me/ и t.me/. Добавить ко всем названим @
new_users = open('new_users.csv', 'w+', encoding='utf-8')
for n1 in range(newUsers_len):
    newUsers_Contacts = dict(newUsers[n1])['contacts']
    newUsers_Contacts_len = len(newUsers_Contacts)
    
    for n2 in range(newUsers_Contacts_len):
        if newUsers_Contacts[n2].get('typeId') == 11:
            tg_name_changed = newUsers_Contacts[n2].get('value')

            if 'https://t.me/' in tg_name_changed:
                tg_name_changed = tg_name_changed.replace('https://t.me/','')

            if 't.me/' in tg_name_changed:
                tg_name_changed = tg_name_changed.replace('t.me/','')
            
            if str(newUsers_Contacts[n2].get('value'))[0] != '@':
                tg_name_changed = '@' + tg_name_changed
            
            new_users.write(str(newUsers[n1].get('email') + ',' + tg_name_changed + '\n'))
            print(newUsers[n1].get('email'), ',', tg_name_changed)
new_users.close()

print('')
print('Список уволенных пользователей:')
fired_users = open('fired_users.csv', 'w+', encoding='utf-8')
for n3 in range(firedUsers_len):
    firedUsers_email = dict()
    fired_users.write(str(dict(firedUsers[n3]).get('email') + '\n'))
    print(dict(firedUsers[n3]).get('email'))
fired_users.close
print('')