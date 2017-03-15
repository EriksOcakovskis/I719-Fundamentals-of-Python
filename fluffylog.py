from datetime import datetime
from fluffyreq import post_json_to_server

class FluffyLog:
    __log_datetime_format = '%Y-%m-%d %H:%M:%S'

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

    def flush(self, server_url=''):
        self.__flog.update({'data': self.__flog_data})
        resp = post_json_to_server(server_url, self.__flog)
        # Hack for testing
        if resp == -1:
            return self.__flog
        self.__flog = {'kind': 'Log', 'data': []}
        self.__flog_data = []
