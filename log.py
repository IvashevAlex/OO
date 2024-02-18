# Добавить проверку на наличие файла логов и в случае его остутствия
# поместить первой строчкой 'Date,Time,UserID,Theme,Type,Status'
log_file = open('jarvislog.txt','a')
# actions_log_file = open('actions_log_file.txt','a')

# Функция открывает файл на запись, записывает информацию и закрывает файл
def write_file(log_file, info):
    log_file = open('jarvislog.txt','a')
    log_file.write(info)
    log_file.close()

# def write_actions_log(actions_log_file, info):
#     actions_log_file = open('actions_log_file.txt','a',encoding='utf-8')
#     actions_log_file.write(str(info))
#     actions_log_file.close()
