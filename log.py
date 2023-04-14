def init_file():
    log_file = open('jarvislog.txt','a')
    return log_file


def write_file(log_file, info):
    log_file.write(info)

init_file()
