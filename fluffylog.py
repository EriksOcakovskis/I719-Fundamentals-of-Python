from datetime import datetime
from fluffyreq import post_json_to_server

class FluffyLog:
    __log_datetime_format = '%Y-%m-%d %H:%M:%S'
    __server_url = server_url = 'http://127.0.0.1:9292/logs'

    def __init__(self):
        self.__flog = {'kind': 'Log', 'data': []}
        self.__flog_data = []

    def __append_to_log(self, level, info):
        dt_now = datetime.now().strftime(self.__log_datetime_format)
        self.__flog_data.append('{0} {1} {2}'.format(dt_now, level, info))

    def debug(self, message):
        self.__append_to_log('DEBUG', message)

    def info(self, message):
        self.__append_to_log('INFO', message)

    def error(self, message):
        self.__append_to_log('ERROR', message)

    def warning(self, message):
        self.__append_to_log('WARNING', message)

    def flush(self):
        self.__flog.update({'data': self.__flog_data})
        post_json_to_server(self.__server_url, self.__flog)
        # print(self.__flog)
        self.__flog = {'kind': 'Log', 'data': []}
        self.__flog_data = []
