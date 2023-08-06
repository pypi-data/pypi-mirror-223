"""
msyql query语句
"""

from typing import Protocol, Any
from sqlalchemy.engine import Engine, Connection
from pandas import DataFrame, read_sql  # type: ignore 


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


class QueryDBMySQL:
    """数据库级别query操作"""

    def __init__(self, 
                 sql_base: SampleBase
                 ) -> None:
        """
        :param sql_base: 数据库操作对象
        """
        self.sql_base = sql_base

    def query_table_names(self) -> list[str]:
        """
        查询数据库中所有表名
        :return: 表名列表
        """
        sql = "SHOW TABLES;"
        table_names = self.sql_base.execute(sql)
        return [table_name[0] for table_name in table_names]

class QueryTableMySQL:

    def __init__(self, 
                 sql_base: SampleBase
                 ) -> None:
        """
        :param sql_base: 数据库操作对象
        """
        self.sql_base = sql_base

    def query_table_columns(self,
                            table_name: str
                            ) -> list[str]:
        """
        查询表中所有列名
        :param table_name: 表名
        :return: 列名列表
        """
        sql = f"SHOW COLUMNS FROM {table_name};"
        columns = self.sql_base.execute(sql)
        return [column[0] for column in columns]

    def query_table(self,
                    table_name: str,
                    **kwargs  # type: ignore
                    ) -> DataFrame:
        """
        查询表中所有数据
        :param table_name: 表名
        :param kwargs: 查询条件
        :return: 数据
        """
        sql = f"SELECT * FROM {table_name};"
        return read_sql(sql, self.sql_base.get_connection(), **kwargs)  # type: ignore

    def query_table_comment(self,
                            table_name: str
                            ) -> str:
        """
        查询表注释
        :param table_name: 表名
        :return: 注释
        """
        sql = f"SHOW CREATE TABLE {table_name};"
        table_comment = self.sql_base.execute(sql)[0][1]
        return table_comment.split("COMMENT='")[1].split("'")[0]

    def query_table_by_condition(self,
                                 table_name: str,
                                 condition_dict: dict[str, Any],
                                 **kwargs  # type: ignore
                                 ) -> DataFrame:
        """
        查询表数据，根据某列的值
        :param table_name: 表名
        :param condition_dict: 查询条件, 例如: {"id": 1}
        :param kwargs: 查询条件
        :return: 数据
        """
        sql = f"SELECT * FROM {table_name} WHERE "
        for key, value in condition_dict.items():
            sql += f"{key}='{value}' AND "
        sql = sql[:-5] + ";"
        return read_sql(sql, self.sql_base.get_connection(), **kwargs)  # type: ignore

    def query_table_by_search(self,
                              table_name: str,
                              search_dict: dict[str, Any],
                              **kwargs  # type: ignore
                              ) -> DataFrame:
        """
        查询表数据，根据某列的值进行搜索, LIKE
        :param table_name: 表名
        :param search_dict: 查询条件, 例如: {"name": "张三"}
        :param kwargs: 查询条件
        :return: 数据
        """
        sql = f"SELECT * FROM {table_name} WHERE "
        for key, value in search_dict.items():
            sql += f"{key} LIKE '%{value}%' AND "
        sql = sql[:-5] + ";"
        return read_sql(sql, self.sql_base.get_connection(), **kwargs)  # type: ignore
    
    def query_columns(self,
                      table_name: str,
                      columns: list[str],
                      **kwargs  # type: ignore
                      ) -> DataFrame:
        """
        查询表中指定列的数据
        :param table_name: 表名
        :param columns: 列名列表
        :return: 数据
        """
        sql = f"SELECT {','.join(columns)} FROM {table_name};"
        return read_sql(sql, self.sql_base.get_connection(), **kwargs)  # type: ignore
    
    def query_columns_by_condition(self,
                                   table_name: str,
                                   columns: list[str],
                                   condition_dict: dict[str, Any],
                                   **kwargs  # type: ignore
                                   ) -> DataFrame:
        """
        查询表中指定列的数据，根据某列的值
        :param table_name: 表名
        :param columns: 列名列表
        :param condition_dict: 查询条件, 例如: {"id": 1}
        :param kwargs: 查询条件
        :return: 数据
        """
        sql = f"SELECT {','.join(columns)} FROM {table_name} WHERE "
        for key, value in condition_dict.items():
            sql += f"{key}='{value}' AND "
        sql = sql[:-5] + ";"
        return read_sql(sql, self.sql_base.get_connection(), **kwargs)  # type: ignore
    
    def query_columns_by_search(self,
                                table_name: str,
                                columns: list[str],
                                search_dict: dict[str, Any],
                                **kwargs  # type: ignore
                                ) -> DataFrame:
        """
        查询表中指定列的数据，根据某列的值进行搜索, LIKE
        :param table_name: 表名
        :param columns: 列名列表
        :param search_dict: 查询条件, 例如: {"name": "张三"}
        :param kwargs: 查询条件
        :return: 数据
        """
        sql = f"SELECT {','.join(columns)} FROM {table_name} WHERE "
        for key, value in search_dict.items():
            sql += f"{key} LIKE '%{value}%' AND "
        sql = sql[:-5] + ";"
        return read_sql(sql, self.sql_base.get_connection(), **kwargs)  # type: ignore
    