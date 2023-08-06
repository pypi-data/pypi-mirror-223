import unittest

from yzdb.db_base import MySQLBase, SQLiteBase


class TestMYSQLBase(unittest.TestCase):
    
    def test_execute(self):
        """测试execute方法"""
        
        # create database
        conn = MySQLBase(
            host='localhost',
            port=3306,
            user='root',
            password='Hyz.js180518',
        )
        conn.execute('CREATE DATABASE IF NOT EXISTS test_db')
        conn.dispose()

        # create table
        conn = MySQLBase(
            host='localhost',
            port=3306,
            user='root',
            password='Hyz.js180518',
            database='test_db'
        )
        conn.execute('CREATE TABLE IF NOT EXISTS test_table (id INT, name VARCHAR(20))')
        conn.execute('INSERT INTO test_table VALUES (1, "test")')

        # check                
        table_name = conn.execute('SHOW TABLES')
        self.assertEqual(table_name.fetchall()[0][0], 'test_table')

        value = conn.execute('SELECT * FROM test_table')
        self.assertEqual(value.fetchall()[0][1], 'test')
        
        # drop table and database
        conn.execute('DROP TABLE test_table')
        conn.execute('DROP DATABASE test_db')
        conn.dispose()

    def test_execute_script(self):
        """测试execute_script方法"""
        
        sql_script = """
        CREATE DATABASE IF NOT EXISTS test_db;
        USE test_db;
        CREATE TABLE IF NOT EXISTS test_table (id INT, name VARCHAR(20));
        INSERT INTO test_table VALUES (1, "test");
        """

        conn = MySQLBase(
            host='localhost',
            port=3306,
            user='root',
            password='Hyz.js180518'
        )
        conn.execute_script(sql_script)
        # check                
        table_name = conn.execute('SHOW TABLES')
        self.assertEqual(table_name.fetchall()[0][0], 'test_table')

        value = conn.execute('SELECT * FROM test_table')
        self.assertEqual(value.fetchall()[0][1], 'test')
        
        # drop table and database
        drop_script = """
        DROP DATABASE test_db;
        """
        conn.execute_script(drop_script)


class TestSQLiteBase(unittest.TestCase):
    
    def test_execute(self):
        """测试execute方法"""
        
        # create table
        conn = SQLiteBase(
            path='tests/test.sqlite3'
        )
        conn.execute('CREATE TABLE IF NOT EXISTS test_table (id INT, name VARCHAR(20))')
        conn.execute('INSERT INTO test_table VALUES (1, "test")')

        # check                
        table_name = conn.execute('SELECT name FROM sqlite_master WHERE type="table"')
        self.assertEqual(table_name.fetchall()[0][0], 'test_table')

        value = conn.execute('SELECT * FROM test_table')
        self.assertEqual(value.fetchall()[0][1], 'test')
        
        # drop table and database
        conn.execute('DROP TABLE test_table')
        conn.dispose()

    def test_execute_script(self):
        """测试execute_script方法"""
        
        sql_script = """
        CREATE TABLE IF NOT EXISTS test_table (id INT, name VARCHAR(20));
        INSERT INTO test_table VALUES (1, "test");
        """

        conn = SQLiteBase(
            path='tests/test.sqlite3'
        )

        conn.execute_script(sql_script)
        # check                
        table_name = conn.execute('SELECT name FROM sqlite_master WHERE type="table"')
        self.assertEqual(table_name.fetchall()[0][0], 'test_table')

        value = conn.execute('SELECT * FROM test_table')
        self.assertEqual(value.fetchall()[0][1], 'test')
        
        # drop table and database
        drop_script = """
        DROP TABLE test_table;
        """
        conn.execute_script(drop_script)

