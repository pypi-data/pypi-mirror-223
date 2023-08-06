"""
msyql drop语句
"""

from typing import Protocol, Any
from sqlalchemy.engine import Engine, Connection


class SampleBase(Protocol):
    
    engine: Engine
    
    def get_connection(self) -> Connection:
        ...
    
    def get_engine(self) -> Engine:
        ...
    
    def execute(self, sql: str) -> Any:
        ...

    def execute_script(self, sql: str) -> list[Any]:
        ...
    
    def dispose(self) -> None:
        ...


class DropDBMySQL:
    """数据库级别drop操作"""

    def __init__(self, 
                 sql_base: SampleBase
                 ) -> None:
        self.sql_base = sql_base
    
    def drop_table(self, 
                  table_name: str
                  ) -> None:
        """
        删除表
        :param table_name: 表名
        """
        sql = f"DROP TABLE {table_name};"
        self.sql_base.execute(sql)


    
class DropTableMySQL:
    """表级别drop操作"""

    def __init__(self, 
                 sql_base: SampleBase
                 ) -> None:
        """
        :param sql_base: 数据库操作对象
        """
        self.sql_base = sql_base
    
    def drop_column(self, 
                    table_name: str, 
                    column_name: str
                    ) -> None:
        """
        删除列
        :param table_name: 表名
        :param column_name: 列名
        """
        sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
        self.sql_base.execute(sql)
    
    def drop_column_comment(self,
                            table_name: str, 
                            column_name: str
                            ) -> None:
        """
        删除列注释
        :param table_name: 表名
        :param column_name: 列名
        """
        sql = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} COMMENT '';"
        self.sql_base.execute(sql)
    
    def drop_data(self,
                  table_name: str, 
                  column_name: str, 
                  column_value: Any
                  ) -> None:
        """
        删除数据
        :param table_name: 表名
        :param column_name: 列名
        :param column_value: 列值
        """
        sql = f"DELETE FROM {table_name} WHERE {column_name} = {column_value};"
        self.sql_base.execute(sql)
