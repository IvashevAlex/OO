import pypyodbc

def connection_with_db(mySQLServer, myDatabase):
    pypyodbc.connect('Driver={SQL Server};'
                     'Server=' + mySQLServer + ';'
                     'Database=' + myDatabase + ';')
