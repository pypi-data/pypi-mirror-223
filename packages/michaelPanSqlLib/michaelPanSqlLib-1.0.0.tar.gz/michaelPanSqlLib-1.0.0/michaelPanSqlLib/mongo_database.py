# ***************************************************************
# Maintainers:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2023.8
# ***************************************************************
import pymongo
from michaelPanPrintLib.change_print import print_with_style


class DataBaseMongo:
    """
    To operate on a Mongo database, there are several steps:
        1.Initialize the Mongo class, Enter the IP address, port number, username, password and database name.

        2.select a function, query_sql
    """
    def __init__(self, host, port, username, password, db_name):
        if int(pymongo.version[0]) >= 4:  # 新版本pymongo
            # 连接mongo
            self.client = pymongo.MongoClient(f"mongodb://{host}:{port}", username=username, password=password)
        else:  # 兼容旧版本
            self.client = pymongo.MongoClient(host=host, port=port)
            self.client["admin"].authenticate(username, password)
        self.db = self.client[db_name]  # 切换到指定数据库下
        print_with_style('Database Connect Successful', color='cyan')

    def query_sql(self, collection_name, data, method='insert', condition=None):
        """
        :param collection_name: a collection name
        :param data: Used in insert,delete and update. a dictionary or a list,
        :param method: choose a function(string format), it concludes: 'insert'  'delete'  'update'  'select'
        :param condition: Used in update and select, a dictionary
        :return: select results, a list

        An example are as follows:
            from michaelPanSqlLib.mongo_database import DataBaseMongo

            host1 = '127.0.0.1'

            port1 = 27017

            username = 'xxx'

            password = 'xxx'

            db_name = 'test1'

            collection_name = 'stu'

            data = [{'id': '001', 'name': 'zhangsan', 'age': 10}, {'id': '002', 'name': 'lisi', 'age': 15}]

            db = DataBaseMongo(host1, port1, username, password, db_name)

            res_list = db.query_sql(collection_name, data, 'select', {"age": 10})
        """
        collection = self.db[collection_name]
        res_list = []
        if method == 'insert':
            if isinstance(data, list):  # 当为多组数据的时候
                collection.insert_many(data)
            else:  # 一组数据
                collection.insert_one(data)
        elif method == 'delete':
            collection.delete_one(data)
        elif method == 'update':
            collection.update_one(condition, {"$set": data})
        elif method == 'select':
            # 查询数据
            ress = collection.find(condition)  # 筛选条件
            res_list = [res for res in ress]
        else:
            raise Exception('Sql statements string is not correct, please check it.')
        return res_list







