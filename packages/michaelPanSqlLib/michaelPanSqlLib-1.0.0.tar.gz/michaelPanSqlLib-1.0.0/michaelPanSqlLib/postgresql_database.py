# ***************************************************************
# Maintainers:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2023.8
# ***************************************************************
import psycopg2
from michaelPanPrintLib.change_print import print_with_style


class DataBasePostgresql:
    """
        To operate on a Postgresql database, there are several steps:
            1.Initialize the Postgresql class, Enter the IP address, port number and password.

            2.select a function, query_sql
        """

    def __init__(self, host, port, username, password, db_name):
        self.conn = psycopg2.connect(database=db_name, host=host, user=username, password=password, port=port)
        self.cursor = self.conn.cursor()
        print_with_style('Database Connect Successful', color='cyan')

    def query_sql(self, sql1, params=None):
        """
        :param sql1: Query statements string
        :param params: Used in 'insert','update',delete, a Tuple
        :return: a List
        An example are as follows:
            from michaelPanSqlLib.postgresql_database import DataBasePostgresql

            host1 = '127.0.0.1'

            port1 = 5432

            username = 'postgres'

            password = 'xxxxxx'

            db_name = 'postgres'

            db = DataBasePostgresql(host1, port1, username, password, db_name)

            select_sql = '''SELECT * FROM "User";'''

            insert_sql = '''INSERT INTO "User" ("User_id", "User_name", "User_password") VALUES (%s, %s, %s);'''

            insert_param = (2, '1', '2')

            update_sql = '''update "User" set "User_name" = %s where "User_id" = %s '''

            update_param = ('y', 1)

            delete_sql = '''delete from "User" where "User_id" = %s '''

            delete_param = (2, )

            results = db.query_sql(delete_sql, delete_param)
        """
        results = []
        task_str = sql1.split(' ')[0].lower()
        if task_str == 'select':
            self.cursor.execute(sql1)
            results = self.cursor.fetchall()  # 查询全部语句
            print_with_style(f"✅{task_str} Successful✅, The total amount of data is: {len(results)}", color='cyan')
        elif task_str == 'insert' or task_str == 'update' or task_str == 'delete':
            if params is None:
                print_with_style('The parameter is not specified, please check and modify before trying again.',
                                 color='cyan')
            else:
                self.cursor.execute(sql1, params)
                print_with_style(f"✅{task_str} Successful✅", color='cyan')
        # 事物提交
        self.conn.commit()
        # 关闭数据库连接
        self.conn.close()
        return results

