"""
msyql修改语句
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


class ModifyDBMySQL:
    """数据库级别修改操作"""

    def __init__(self, 
                 sql_base: SampleBase
                 ) -> None:
        self.sql_base = sql_base
    
    def modify_table_name(self,
                          old_table_name: str,
                          new_table_name: str
                          ) -> None:
        """
        修改表名
        :param old_table_name: 旧表名
        :param new_table_name: 新表名
        """
        sql = f"ALTER TABLE {old_table_name} RENAME TO {new_table_name};"
        self.sql_base.execute(sql)

    def modify_table_comment(self,
                             table_name: str,
                             comment: str
                             ) -> None:
        """
        修改表注释
        :param table_name: 表名
        :param comment: 注释
        """
        sql = f"ALTER TABLE {table_name} COMMENT '{comment}';"
        self.sql_base.execute(sql)
        

class ModifyTableMySQL:
    """表级别修改操作"""
    
    def __init__(self,
                 sql_base: SampleBase
                 ) -> None:
        self.sql_base = sql_base
    
    def modify_column_name(self,
                           table_name: str,
                           old_column_name: str,
                           new_column_name: str
                           ) -> None:
        """
        修改列名
        :param table_name: 表名
        :param old_column_name: 旧列名
        :param new_column_name: 新列名
        """
        sql = f"ALTER TABLE {table_name} CHANGE COLUMN {old_column_name} {new_column_name};"
        self.sql_base.execute(sql)
    
    def modify_column_type(self,
                           table_name: str,
                           column_name: str,
                           column_type: str
                           ) -> None:
        """
        修改列类型
        :param table_name: 表名
        :param column_name: 列名
        :param column_type: 列类型
        """
        sql = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {column_type};"
        self.sql_base.execute(sql)
    
    def modify_column_comment(self,
                              table_name: str,
                              column_name: str,
                              comment: str
                              ) -> None:
        """
        修改列注释
        :param table_name: 表名
        :param column_name: 列名
        :param comment: 注释
        """
        sql = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} COMMENT '{comment}';"
        self.sql_base.execute(sql)
