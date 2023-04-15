log_file = open('jarvislog.txt','a')

# Функция открывает файл на запись, записывает информацию и закрывает файл
def write_file(log_file, info):
    log_file = open('jarvislog.txt','a')
    log_file.write(info)
    log_file.close()

