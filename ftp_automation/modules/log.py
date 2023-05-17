import os
import datetime
import time


def logging_top(automation_name):
    print()
    print(f'############################### Starting {automation_name} Automation\n')


def logging_bottom(automation_name):
    print()
    print(f'############################### Ending {automation_name} Automation')


def list_log_files(dir):
    """
    List logs in directory

    :param dir - Directory where logs are hosted
    """

    log_files = list()
    files = os.listdir(dir)

    for file in files:
        if os.path.isfile(os.path.join(dir, file)) and file[-4:] == '.log':
            log_files.append(os.path.join(dir, file))

    return log_files


def clear_logging(retention, file_path):
    """
    Clear files based on retention time (in days)

    :param retention: The period of time that file must be maintained
    :param file_path: A full path file list
    """

    today = int(datetime.date.today().strftime('%Y%m%d'))  # Captura data atual
    retention = today - retention

    for i in file_path:
        modtime_epoc = os.path.getmtime(i)  # Coleta a última data de modificação do arquivo
        modtime_local = time.strftime('%Y%m%d', time.localtime(modtime_epoc))  # Converte para formato localtime

        if int(modtime_local) < retention:  # Verifica arquivos que são mais antigos que o tempo de retenção
            os.remove(i)
            print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*info* Cleanup logging file {i}')
