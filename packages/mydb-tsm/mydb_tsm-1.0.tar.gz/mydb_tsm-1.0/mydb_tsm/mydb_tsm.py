import pymysql


def commit(sql_run):
    """
    当sql语句执行异常时，该闭包可以自动回滚，自动关闭数据库连接。
    :param sql_run: 执行sql语句的方法
    :return: 返回inner，形成闭包
    """
    closeFlag = False  # True表示需要关闭数据库资源。闭包中的变量，用于判断是否需要关闭数据库连接。

    def inner(self, *args, **kwargs) -> None:
        """
        内层函数
        :param self: 给实例方法增加装饰器，self表示实例对象
        :param args: args表示可变参数
        :param kwargs: kwargs表示可变参数
        :return: None
        """
        nonlocal closeFlag  # 闭包可以修改外层函数的变量

        try:
            rows = sql_run(self, *args, **kwargs)  # 执行SQL方法
            # 如果是插入、更新、删除语句，且受影响的行数不为0，则执行提交
            if rows and not sql_run.__name__.startswith('query'):
                self.conn.commit()  # 提交
        except Exception as e:
            closeFlag = True  # 报错后关闭SQL连接
            print('闭包-SQL执行失败！！', e, sep='\t\t')
            if self.conn:  # 连接存在时，回滚
                self.conn.rollback()  # 回滚
                print("回滚成功！")
        else:
            closeFlag = False
        finally:
            if closeFlag:
                self.close()
                print("闭包-数据库连接已关闭！")

    return inner


class DBUtil(object):
    def __init__(self, config: dict) -> None:
        self.config = config
        self.conn = None
        self.cur = None
        self.config['port'] = self.config.get('port', 3306)
        print("正在创建数据库连接...")
        self.connection()  # 创建数据库连接
        if self.conn:
            print("初始化已完成，数据库连接成功！")
        else:
            print("初始化失败，数据库连接失败！")

    @commit
    def connection(self) -> None:
        """
        连接数据库
        :return: None
        """
        self.conn = pymysql.connect(**self.config)
        self.cur = self.conn.cursor()

    def close(self) -> None:
        """
        关闭数据库资源
        :return: None
        """
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    @commit
    def create_db(self, db_name: str, character="utf8mb4", collate="utf8mb4_unicode_ci") -> None:
        """
        创建数据库
        :param db_name: 数据库名称
        :param character: 字符集
        :param collate: 字符集校对规则
        :return: None
        """
        SQL = f'create database if not exists {db_name} default character set "{character}" collate "{collate}";'
        self.cur.execute(SQL)

    @commit
    def drop_db(self, db_name: str) -> None:
        """
        删除数据库
        :param db_name: 数据库名称
        :return: None
        """
        SQL = f'drop database if exists {db_name};'  # 如果数据库存在则删除，避免已存在数据库导致报错
        self.cur.execute(SQL)

    @commit
    def use_db(self, db_name: str) -> None:
        """
        使用数据库
        :param db_name: 数据库名称
        :return: None
        """
        self.cur.execute(f'use {db_name};')

    @commit
    def create_table(self, sql: str) -> None:
        """
        创建表
        :sql: 创建表的SQL语句
        :return: None
        """
        self.cur.execute(sql)

    @commit
    def drop_table(self, table_name: str) -> None:
        """
        删除表
        :param table_name: 表名称
        :return: None
        """
        self.cur.execute(f'drop table if exists {table_name};')  # 如果test存在则删除，避免已存在数据库导致报错

    @commit
    def changeRows(self, sql: str, args: (tuple, list)) -> (int, None):
        """
        插入、更新、删除数据
        :param sql: SQL语句
        :param args: pymysql中的args，用来给SQL语句传参
        :return: None or rows  # rows表示受影响的行数
        """
        rows = None
        if sql.startswith('insert'):  # 用户输入的sql是插入语句insert
            if len(args) > 1 and isinstance(args[0], (tuple, list)):
                rows = self.cur.executemany(sql, args)
                if rows == len(args):
                    return rows
            else:
                rows = self.cur.execute(sql, args)
                if rows:
                    return rows

            return None

        rows = self.cur.execute(sql, args)  # 执行SQL语句

        if rows == 0:  # 如果影响行数为0，说明SQL语句执行失败
            print("已修改行数为0，数据操作失败！")
            return

        if sql.startswith('delete'):  # 用户传入的sql是删除语句delete
            if rows:
                return rows
        elif sql.startswith('update'):  # 用户输入的sql是更新语句update
            if rows:
                return rows

    @commit
    def queryRows(self, sql: str, args: (list, tuple), size=None) -> (tuple, None):
        """
        查询数据
        :param sql: SQL语句
        :param args: pymysql中的args，用来给SQL语句传参
        :param size: 查询结果的条数
        :return: None or result  # result表示查询结果
        """
        self.cur.execute(sql, args)
        if size is None:
            result = self.cur.fetchall()
            return result
        elif size == 1:
            result = self.cur.fetchone()
            return result
        elif size > 0:
            result = self.cur.fetchmany(size)
            return result
        elif size <= 0:
            raise ValueError("size参数必须大于0！")


if __name__ == '__main__':
    config = {
        'host': '192.168.93.131',
        'port': 3306,
        'user': 'root',
        'password': 'Tomboy_test',
    }

    db = DBUtil(config)
    db.create_db('mydb_tsm')
