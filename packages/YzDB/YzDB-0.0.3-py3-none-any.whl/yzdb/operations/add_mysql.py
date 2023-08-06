"""
msyql添加语句
"""

from typing import Protocol, Any
from sqlalchemy.engine import Engine, Connection
from pandas import DataFrame


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


class AddDBMySQL:
    """数据库级别添加操作"""

    def __init__(self, 
                 sql_base: SampleBase
                 ) -> None:
        self.sql_base = sql_base
    
    def add_table(self, 
                  table_name: str
                  ) -> None:
        """
        添加表
        :param table_name: 表名
        """
        # 判断表是否存在
        sql = f"CREATE TABLE {table_name} (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id));"
        self.sql_base.execute(sql)

    
class AddTableMySQL:
    """表级别添加操作"""

    def __init__(self, 
                 sql_base: SampleBase
                 ) -> None:
        """
        :param sql_base: 数据库操作对象
        """
        self.sql_base = sql_base

    def add_column(self, 
                   table_name: str, 
                   column_name: str, 
                   column_type: str,
                   comment: str = ''
                   ) -> None:
        """
        添加列
        :param table_name: 表名
        :param column_name: 列名
        :param column_type: 列类型
        :param comment: 列注释, 默认为空
        """
        sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} COMMENT '{comment}';"
        self.sql_base.execute(sql)
    
    def add_index(self, 
                  table_name: str, 
                  column_name: str, 
                  index_name: str
                  ) -> None:
        """
        添加索引
        :param table_name: 表名
        :param column_name: 列名
        :param index_name: 索引名
        """
        sql = f"ALTER TABLE {table_name} ADD INDEX {index_name} ({column_name});"
        self.sql_base.execute(sql)
    
    def add_data(self,
                 table_name: str,
                 data: DataFrame,
                 **kwargs  # type: ignore
                 ) -> None:
        """
        添加数据
        :param table_name: 表名
        :param data: 数据
        """
        data.to_sql(table_name, 
                    self.sql_base.get_connection(), 
                    if_exists='append', 
                    index=False, 
                    **kwargs  # type: ignore
                    )
