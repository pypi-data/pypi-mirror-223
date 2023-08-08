import pymysql


"""
验证闭包能自动关闭数据库连接：
    # 创建连接失败，看能不能读取到cur,conn
    # 创建数据库失败，看能不能读取到cur,conn
    # 创建连接成功，创建数据库成功，看能不能读取到cur,conn
"""


def commit(sql_run):
    closeFlag = False  # True表示需要关闭数据库资源。闭包中的变量，用于判断是否需要关闭数据库连接。

    def inner(self, *args, **kwargs):
        nonlocal closeFlag
        try:
            rows = sql_run(self, *args, **kwargs)  # 执行SQL方法
            print('rows', rows)
            if rows and not sql_run.__name__.startswith('query'):
                self.conn.commit()  # 提交
                print("提交成功！")
        except Exception as e:
            closeFlag = True  # 报错后关闭SQL连接
            print('闭包-SQL执行失败！！', e, sep='\t\t')
            if self.conn:
                self.conn.rollback()  # 回滚
                print("回滚成功！")
        else:
            closeFlag = False  # 如果没有报错，不需要关闭数据库连接
        finally:
            if closeFlag:  # closeFlag = True则关闭数据库连接
                self.close()
                print("闭包-数据库连接已关闭！")

    return inner


class DBUtil(object):
    def __init__(self, config):
        self.config = config
        print("正在创建数据库连接...")
        self.connection()
        if self.conn:
            print("初始化已完成，数据库连接成功！")
        else:
            print("初始化失败，数据库连接失败！")

    @commit
    def connection(self):
        """连接数据库"""
        self.conn = pymysql.connect(**self.config)
        self.cur = self.conn.cursor()

    def close(self):
        """关闭数据库资源"""
        if self.cur:
            self.cur.close()
            print("游标已关闭！")
        if self.conn:
            self.conn.close()
            print("数据库连接已关闭！")

    @commit
    def create_db(self, db_name, character="utf8mb4", collate="utf8mb4_unicode_ci"):
        """创建数据库"""
        SQL = f'create database {db_name} default character set "{character}" collate "{collate}";'
        self.cur.execute(SQL)
        print("数据库创建成功！")

    @commit
    def drop_db(self, db_name):
        """删除数据库"""
        SQL = f'drop database if exists {db_name};'  # 如果数据库存在则删除，避免已存在数据库导致报错
        self.cur.execute(SQL)
        print("======数据库删除成功！======")

    @commit
    def use_db(self, db_name):
        self.cur.execute(f'use {db_name};')
        print(f'使用数据库{db_name}')

    @commit
    def create_table(self, sql):
        """创建表"""
        self.cur.execute(sql)

    @commit
    def drop_table(self, table_name):
        """删除表"""
        self.cur.execute(f'drop table if exists {table_name};')  # 如果test存在则删除，避免已存在数据库导致报错
        print(f"======删除{table_name}表成功！======")

    @commit
    def changeRows(self, sql, args):
        rows = None
        if sql.startswith('insert'):  # 用户输入的sql是插入语句insert
            print("我是insert语句！")
            print(args)
            if len(args) > 1 and isinstance(args[0], (tuple, list)):
                print("多行插入！")
                rows = self.cur.executemany(sql, args)
                if rows == len(args):
                    print(f"数据插入成功，插入行数{rows}！")
                    return rows
            else:
                print("单行插入！")
                rows = self.cur.execute(sql, args)
                if rows:
                    print(f"数据插入成功，插入行数{rows}！")
                    return rows

            return None

        print("我是非insert语句！")
        rows = self.cur.execute(sql, args)  # 执行SQL语句

        if rows == 0:
            print("未更新数据！请检查SQL语句是否正确！")
            return

        if sql.startswith('delete'):  # 用户传入的sql是删除语句delete
            if rows:
                print(f"数据删除成功，删除行数{rows}！")
                return rows
        elif sql.startswith('update'):  # 用户输入的sql是更新语句update
            if rows:
                print(f"数据更新成功，更新行数{rows}！")
                return rows

    @commit
    def queryRows(self, sql, args, size=None):
        """查询数据"""
        self.cur.execute(sql, args)
        if size is None:
            result = self.cur.fetchall()
            print(f"查询-所有数据，共计{len(result)}条数据！")
            return result
        elif size == 1:
            result = self.cur.fetchone()
            print(f"查询到{size}条数据！")
            return result
        elif size > 0:
            result = self.cur.fetchmany(size)
            print(f"查询到前{size}条数据！")
            return result
        self.conn.insert_id()
        self.cur.lastrowid



if __name__ == '__main__':
    config = {
        'host': '192.168.93.131',
        'port': 3306,
        'user': 'root',
        'password': 'Tomboy_test',
    }

    db = DBUtil(config)
    db.create_db('testpysql')
    db.use_db('testpysql')
    db.create_table("create table test520(id int primary key auto_increment, uname varchar(20));")

    db.changeRows('insert into test520(uname) values(%s);', ['Tom'])
    db.changeRows('insert into test520(uname) values(%s);', [('Tom', ), ('Jerry', ), ('Tomboy', ), ('Effie', )])
    db.changeRows('insert into test520(uname) values(%s);', [('Tom',), ('Jerry',), ('Tomboy',), ('Effie',)])
    db.changeRows('insert into test520(uname) values(%s);', [('Tom',), ('Jerry',), ('Tomboy',), ('Effie',)])
    db.changeRows('insert into test520(uname) values(%s);', [('Tom',), ('Jerry',), ('Tomboy',), ('Effie',)])


    db.changeRows('update test520 set uname=%s where id between %s and %s;', ['莫林', 1, 3])
    db.changeRows('update test520 set uname=%s where id=%s;', ['Tom', 1])
    db.changeRows('update test520 set uname=%s where id=%s;', ['Jerry', 20])

    db.changeRows('delete from test520 where id=%s', [3])
    # try:
    db.changeRows("delete from test520 where uname in (%s, %s);", ('莫林', 'Tom'))  # 删除多条
    # except Exception as e:
    #     print(e)




    res = db.queryRows('select * from test520 where id between %s and %s;', [1, 10])  # 查询所有
    print(res)
    print('==================================================================================')
    res = db.queryRows('select * from test520 where id between %s and %s;', [1, 10], 1)  # 查询一条
    print(res)
    print('000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
    res1 = db.queryRows('select * from test520 where id between %s and %s;', [1, 10], 1)  # 查询多条
    print(res1)
    res2 = db.queryRows('select * from test520 where id between %s and %s;', [1, 10], 5)  # 查询多条
    print(res2)
    # 这句有问题

    # db = DBUtil(config)
    # db.drop_table('test520')
    # db.drop_db('testpysql')

    print(db.cur, db.conn)
