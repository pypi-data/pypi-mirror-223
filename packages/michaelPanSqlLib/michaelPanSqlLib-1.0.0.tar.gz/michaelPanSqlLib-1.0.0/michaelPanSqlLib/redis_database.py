# ***************************************************************
# Maintainers:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2023.8
# ***************************************************************
import redis
from michaelPanPrintLib.change_print import print_with_style


class DataBaseRedis:
    """
    To operate on a Redis database, there are several steps:
        1.Initialize the redis class, Enter the IP address, port number and password.

        2.select a function, query_sql
    """
    def __init__(self, host, port,  password):
        pool = redis.ConnectionPool(host=host, port=port, password=password, decode_responses=True)  # 实现一个连接池
        self.r = redis.Redis(connection_pool=pool)
        print_with_style('Database Connect Successful', color='cyan')

    def query_sql(self, key, value=None, method='insert', new_key=None, exact_search=True):
        """
        :param key: String format, a data key
        :param value: a String or Float or Int format
        :param method: 'insert' or 'select' or 'delete' or 'rename'
        :param new_key: Used in rename method
        :param exact_search: Whether to conduct an exact search
        :return: a search output
        """
        results = ''
        if method == 'insert':
            if self.r.exists(key):  # 当数据已经存在时
                print_with_style('key is already exists, please check it', color='cyan')
            else:
                if type(value) is str or type(value) is int or type(value) is float:  # 当类型为字符串、整数、小数时
                    self.r.set(key, value)
                else:
                    raise Exception('Lists or other types of data are not supported')
        elif method == 'delete':
            self.r.delete(key)
        elif method == 'select':
            if exact_search:  # 精确查找
                results = self.r.get(key)
            else:  # 模糊查找
                results = self.r.keys(key)
        elif method == 'rename':
            self.r.rename(key, new_key)
        else:
            raise Exception('Sql statements string is not correct, please check it.')
        return results
