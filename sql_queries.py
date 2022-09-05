import pypyodbc
import time

def connection_with_db(mySQLServer, myDatabase):
    pypyodbc.connect('Driver={SQL Server};'
                     'Server=' + mySQLServer + ';'
                     'Database=' + myDatabase + ';')

def request_1(callback_query):
    return """ SELECT TOP(1) 
                    IIF(UserChat = """ + str(callback_query.from_user.id) + """, 
                        CONVERT(VARCHAR(max), UserChat), 
                        'False') as res
                    FROM dbo.WhiteList ORDER BY res"""

def request_2(callback_query):
    return """SELECT UserMark 
                       FROM dbo.WhiteList 
                       WHERE UserChat = """ + str(callback_query.from_user.id) + """;"""

def request_3(callback_query):
    return """ INSERT INTO dbo.WhiteList (UserChat, UserId, UserFIO, AddUserDate)
                        VALUES (""" + str(callback_query.from_user.id) + """, 
                        '@' + '""" + str(callback_query.from_user.username) + """', 
                        '""" + str(callback_query.from_user.first_name) + ' ' + str(callback_query.from_user.last_name) + """',
                        '""" + str(time.strftime('%Y-%m-%d')) + """');"""

def request_4(res):
    return """UPDATE dbo.WhiteList
                  SET UserMark = 1
                  WHERE UserChat = """ + str(res) + """;"""

def request_5(res):
    return """DELETE dbo.WhiteList 
                  WHERE UserChat = """ + str(res) + """;"""
