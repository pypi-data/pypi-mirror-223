# ***************************************************************
# Maintainers:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2023.8
# ***************************************************************
import pymysql
from michaelPanPrintLib.change_print import print_with_style
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()


class DataBaseMySql:
    """
    To operate on a MySQL database, there are several steps:
        1.Initialize the MySQL class, Enter the IP address, port number, username, password, and database name.

        2.select a function, query_sql

    A few simple adding, deleting, modifying and searching instructions are as follows:
        1.query: select * form table_name where column1 > 18;

        2.insert: INSERT INTO table_name(column1,column2,column3, ...) VALUES (value1,value2,value3, ...);

        3.alter: UPDATE table_name SET column1='DB',column2=3.5... WHERE column3=2;

        4.delete: delete from table_name where column1=2;
    """
    def __init__(self, host, port, user, password, database):
        # 打开数据库连接
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    def query_sql(self, sql1):
        """
        :param sql1: Query statements string
        :return: Query results, a List
        """
        task_str = sql1.split(' ')[0].lower()
        if task_str == 'select':
            self.cursor.execute(sql1)
            results = self.cursor.fetchall()
            print_with_style(f"✅{task_str} Successful✅, The total amount of data is: {len(results)}", color='cyan')
        elif task_str == 'insert' or task_str == 'update' or task_str == 'delete':
            self.cursor.execute(sql1)
            self.db.commit()
            results = []
            print_with_style(f"✅{task_str} Successful✅", color='cyan')
        else:
            raise Exception('Sql statements string is not correct, please check it.')
        return list(results)  # 返回所有结果


