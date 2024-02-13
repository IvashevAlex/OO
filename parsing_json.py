import pypyodbc
import json
import test_mode_check

from config import DB_name

test_mode = test_mode_check.test_mode()

mySQLServer = test_mode_check.get_server(test_mode)
myDatabase = DB_name


def tg_username_changer(tg_name_changed):
    if 'https://t.me/' in tg_name_changed:
        tg_name_changed = tg_name_changed.replace('https://t.me/','')

    if 't.me/' in tg_name_changed:
        tg_name_changed = tg_name_changed.replace('t.me/','')
    
    if str(tg_name_changed[0]) != '@':
        tg_name_changed = '@' + tg_name_changed

    return tg_name_changed


# Парсит файл data.json 
with open('data.json','r', encoding='utf-8') as file:
    result_dict = json.load(file)

newUsers = result_dict['newUsers']
modifiedUsers = result_dict['modifiedUsers']
firedUsers = result_dict['firedUsers']
lastModifiedDate = result_dict['lastModifiedDate']

newUsers_len = len(newUsers)
modifiedUsers_len = len(modifiedUsers)
firedUsers_len = len(firedUsers)

# newUsers_contacts = newUsers[0].get('contacts')
# modifiedUsers = modifiedUsers[0].get('contacts')
# firedUsers_email = firedUsers[0].get('email')
# firedUsers_email_len = len(firedUsers_email)

# Внесение записей о новых сотрудниках в TrueAccess
# new_users = open('new_users.csv', 'w+', encoding='utf-8')

print('НОВЫЕ ЮЗЕРЫ')

for n1 in range(newUsers_len):
    newUsers_contacts = dict(newUsers[n1])['contacts']
    newUsers_contacts_len = len(newUsers_contacts)
    
    for n2 in range(newUsers_contacts_len):
        if newUsers_contacts[n2].get('typeId') == 11:
            tg_name_changed = newUsers_contacts[n2].get('value')
            tg_name_changed = tg_username_changer(tg_name_changed)
            
            # new_users.write(str(newUsers[n1].get('email') + ',' + tg_name_changed + '\n'))
            print(newUsers[n1].get('email'), ',', tg_name_changed)

            # Проверяем наличие почты юзера в общей базе доступа
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

            # Если записи там нет, то вносим её туда
            if count[0][0] == 0:
                print('Нет данных по ', str(newUsers[n1].get('email')), 'в true_access. Добавляем запись в БД')
                print('')
                connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=' + mySQLServer + ';'
                                    'Database=' + myDatabase + ';')
                cursor = connection.cursor()

                SQLQuery = """INSERT INTO [dbo].[TrueAccess] ([Email], [UserNameTG])
                            VALUES('""" + str(newUsers[n1].get('email')) + """','""" + str(tg_name_changed) + """');
                            """
                cursor.execute(SQLQuery)
                connection.commit()
                connection.close()
            
            else:
                pass

# new_users.close()
print('')
print('МОДИФИЦИРОВАННЫЕ ЮЗЕРЫ')

# Внесение записей о действующих сотрудниках, изменявших информацию
for m1 in range(modifiedUsers_len):
    modifiedUsers_contacts = dict(modifiedUsers[m1])['contacts']
    modifiedUsers_contacts_len = len(modifiedUsers_contacts)
    
    for m2 in range(modifiedUsers_contacts_len):
        if modifiedUsers_contacts[m2].get('typeId') == 11:
            tg_name_changed = modifiedUsers_contacts[m2].get('value')
            tg_name_changed = tg_username_changer(tg_name_changed)
            
            # new_users.write(str(newUsers[n1].get('email') + ',' + tg_name_changed + '\n'))
            # print(modifiedUsers[m1].get('email'), ',', tg_name_changed)

            # Проверяем наличие почты юзера в общей базе доступа
            connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=' + mySQLServer + ';'
                                    'Database=' + myDatabase + ';')
            cursor = connection.cursor()
            SQLQuery = """SELECT COUNT (*)
                          FROM [dbo].[TrueAccess]
                          WHERE [Email] =  '""" + str(modifiedUsers[m1].get('email')) + """'
                        """
            cursor.execute(SQLQuery)
            count = cursor.fetchall()
            connection.close()

            # Если записи там нет, то вносим её туда
            if count[0][0] == 0:
                print('Нет данных по ', str(modifiedUsers[m1].get('email')), 'в true_access. Добавляем запись в БД')
                print('')
                connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=' + mySQLServer + ';'
                                    'Database=' + myDatabase + ';')
                cursor = connection.cursor()

                SQLQuery = """INSERT INTO [dbo].[TrueAccess] ([Email], [UserNameTG])
                            VALUES('""" + str(modifiedUsers[m1].get('email')) + """','""" + str(tg_name_changed) + """');
                            """
                cursor.execute(SQLQuery)
                connection.commit()
                connection.close()
            
            else:
                pass

print('')
print('УДАЛЁННЫЕ ЮЗЕРЫ')

# Удаление записей об уволенных сотрудниках из TrueAccess
# fired_users = open('fired_users.csv', 'w+', encoding='utf-8')
for n3 in range(firedUsers_len):
    firedUsers_email = dict()
    # fired_users.write(str(dict(firedUsers[n3]).get('email') + '\n'))
    print(dict(firedUsers[n3]).get('email'))

    connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server=' + mySQLServer + ';'
                            'Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = """SELECT COUNT (*)
                    FROM [dbo].[TrueAccess]
                    WHERE [Email] =  '""" + str(dict(firedUsers[n3]).get('email')) + """'
                """
    cursor.execute(SQLQuery)
    count = cursor.fetchall()
    connection.close()

    if count[0][0] == 1:

        connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server=' + mySQLServer + ';'
                            'Database=' + myDatabase + ';')
        cursor = connection.cursor()

        # Удаляем из TrueAccess записи, содержащие потчы из списка удаленных
        SQLQuery = """DELETE FROM [dbo].[TrueAccess]
                    WHERE [Email] =  '""" + str(dict(firedUsers[n3]).get('email')) + """'
                    """
        cursor.execute(SQLQuery)
        connection.commit()

        connection.close()
    
    else:
        pass

# fired_users.close()

# Удаляем из WhiteList все почты котрых нет в TrueAccess
connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server=' + mySQLServer + ';'
                            'Database=' + myDatabase + ';')

cursor = connection.cursor()
SQLQuery = """DELETE FROM [dbo].[WhiteList]
            WHERE [UserId] NOT IN (SELECT [UserNameTG] FROM [TrueAccess])
            """
cursor.execute(SQLQuery)
connection.commit()
