"""
连接模块，外部调用接口
"""

from yzdb.db_base import SQLiteBase

from yzdb.operations.add_sqlite import AddDBSQLite, AddTableSQLite
from yzdb.operations.drop_sqlite import DropDBSQLite, DropTableSQLite
from yzdb.operations.modify_sqlite import ModifyDBSQLite, ModifyTableSQLite
from yzdb.operations.query_sqlite import QueryDBSQLite, QueryTableSQLite


class SQLiteConn(SQLiteBase,
                AddDBSQLite, AddTableSQLite,
                DropDBSQLite, DropTableSQLite,
                ModifyDBSQLite, ModifyTableSQLite,
                QueryDBSQLite, QueryTableSQLite):
    
    def __init__(self, 
                 path: str
                 ) -> None:
        """
        :param path: 数据库文件路径
        """
        super().__init__(path)
        self.sql_base = self
        

def create_sqlite_conn(path: str) -> SQLiteConn:
    """
    创建sqlite数据库连接
    :param path: 数据库文件路径
    """
    return SQLiteConn(path)
