"""
数据库连接
"""

from sqlalchemy import create_engine, text

from sqlalchemy import Engine, Connection
from abc import ABC, abstractmethod
from typing import Any, Self


class DBbase(ABC):
    """
    数据库连接基类
    """
    __instance: Self | None = None

    
    def __new__(cls, *args, **kwargs) -> Self:  # type: ignore
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance
        
    @abstractmethod
    def create_engine(self) -> Engine:
        ...

    def __init__(self) -> None:
        self.engine: Engine = self.create_engine()

    def get_engine(self) -> Engine:
        return self.engine
    
    def get_connection(self) -> Connection:
        return self.engine.connect()
    
    def execute(self, sql: str) -> Any:
        """
        execute single sql, should be used for update, delete, insert
        :param sql: sql to execute
        :return: None
        """
        with self.engine.begin() as conn:
            return conn.execute(text(sql))
    
    def execute_script(self, sql: str) -> list[Any]:
        """
        execute sql script, should be used for create table, create database
        :param sql: sql to execute
        :return: None
        """
        # spit sql by ';'
        sqls = sql.split(';')
        # remove empty sql
        sqls = [s.strip() for s in sqls if s.strip() != '']
        # execute sql
        with self.engine.begin() as conn:
            results = [conn.execute(text(s)) for s in sqls]
        return results
    
    def dispose(self) -> None:
        self.engine.dispose()


class MySQLBase(DBbase):
    """
    mysql connection
    """

    def __init__(self, host: str, port: int, user: str, password: str, database: str = '') -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        super().__init__()
    
    def create_engine(self) -> Engine:
        return create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}'
            f':{self.port}/{self.database}?charset=utf8mb4'
        )


class SQLiteBase(DBbase):
    """
    sqlite connection
    """

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()
    
    def create_engine(self) -> Engine:
        return create_engine(f'sqlite:///{self.path}')
    