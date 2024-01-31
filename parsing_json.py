import pypyodbc
import json
import test_mode_check

from config import DB_name

test_mode = test_mode_check.test_mode()

mySQLServer = test_mode_check.get_server(test_mode)
myDatabase = DB_name

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

            # Проверяем наличие поты юзера в общей базе доступа
            connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=' + mySQLServer + ';'
                                    'Database=' + myDatabase + ';')
            cursor = connection.cursor()
            SQLQuery = """SELECT COUNT (*)
                          FROM [dbo].[TrueAccess]
                          WHERE [Email] =  '""" + str(newUsers[n1].get('email')) + """'
                        """
            cursor.execute(SQLQuery)
            count = cursor.fetchall()
            connection.close()
            print(count[0][0])

            # Если ваписи там нет, то вносим её туда
            if count[0][0] is 0:
                print('Нет данных по ', str(newUsers[n1].get('email')), 'в true_access. Добавляем запись в БД')

                connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=' + mySQLServer + ';'
                                    'Database=' + myDatabase + ';')
                cursor = connection.cursor()

                SQLQuery = """INSERT INTO [dbo].[TrueAccess] ([Email], [UserNameTG])
                            VALUES('""" + str(newUsers[n1].get('email')) + """','""" + str(tg_name_changed) + """');
                            """
                # print(SQLQuery)
                cursor.execute(SQLQuery)
                connection.commit()
                connection.close()
            
            else:
                print('Юзер ', str(newUsers[n1].get('email')), ' уже есть в БД true_access. Действий не требуется')
                print('')

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