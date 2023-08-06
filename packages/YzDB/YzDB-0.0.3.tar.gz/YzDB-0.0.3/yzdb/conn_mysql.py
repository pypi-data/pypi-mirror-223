"""
连接模块，外部调用接口
"""

from yzdb.db_base import MySQLBase

from yzdb.operations.add_mysql import AddDBMySQL, AddTableMySQL
from yzdb.operations.drop_mysql import DropDBMySQL, DropTableMySQL
from yzdb.operations.modify_mysql import ModifyDBMySQL, ModifyTableMySQL 
from yzdb.operations.query_mysql import QueryDBMySQL, QueryTableMySQL 


class MySQLConn(MySQLBase,
                AddDBMySQL, AddTableMySQL,
                DropDBMySQL, DropTableMySQL,
                ModifyDBMySQL, ModifyTableMySQL,
                QueryDBMySQL, QueryTableMySQL):
    
    def __init__(self, 
                 host: str,
                 port: int,
                 user: str,
                 password: str,
                 db_name: str = ''
                 ) -> None:
        """
        :param host: 主机名
        :param port: 端口号
        :param user: 用户名
        :param password: 密码
        :param db_name: 数据库名
        """
        super().__init__(host, port, user, password, db_name)
        self.sql_base = self
        

def create_mysql_conn(host: str,
                      port: int,
                      user: str,
                      password: str,
                      db_name: str = ''
                      ) -> MySQLConn:
    """
    创建MySQL数据库连接对象
    :param host: 主机名
    :param port: 端口号
    :param user: 用户名
    :param password: 密码
    :param db_name: 数据库名
    :return: MySQL数据库连接对象
    """
    return MySQLConn(host, port, user, password, db_name)
