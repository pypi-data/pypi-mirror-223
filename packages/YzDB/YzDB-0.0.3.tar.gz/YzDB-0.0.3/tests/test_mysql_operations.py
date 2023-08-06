import unittest

from yzdb.db_base import MySQLBase
from yzdb.operations.add_mysql import AddDBMySQL, AddTableMySQL

class TestAddDBMySQL(unittest.TestCase):

    def test_add_db(self):
        # prepare
        mysql_base = MySQLBase(
            host='localhost',
            port=3306,
            user='root',
            password='Hyz.js180518',
        )
        mysql_base.execute('DROP DATABASE IF EXISTS test;')
        mysql_base.execute('CREATE DATABASE IF NOT EXISTS test;')
        mysql_base.execute('USE test;')
        
        # method
        add_db = AddDBMySQL(mysql_base)
        add_db.add_table('test_table')
        # check
        result = mysql_base.execute('SHOW TABLES;')
        self.assertEqual(result.fetchall()[0][0], 'test_table')

        # dispose
        mysql_base.execute('DROP DATABASE IF EXISTS test;')
        mysql_base.dispose()

class TestAddTableMySQL(unittest.TestCase):

    def test_add_column(self):
        # prepare
        mysql_base = MySQLBase(
            host='localhost',
            port=3306,
            user='root',
            password='Hyz.js180518',
        )
        mysql_base.execute('DROP DATABASE IF EXISTS test;')
        mysql_base.execute('CREATE DATABASE IF NOT EXISTS test;')
        mysql_base.execute('USE test;')
        mysql_base.execute('CREATE TABLE IF NOT EXISTS test_table (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id));')

        # method
        add_table = AddTableMySQL(mysql_base)
        add_table.add_column('test_table', 'test_column', 'VARCHAR(10)', 'test_comment')
        # check
        result = mysql_base.execute('SHOW FULL COLUMNS FROM test_table;')
        self.assertEqual(result.fetchall()[1][0], 'test_column')

        # dispose
        mysql_base.execute('DROP DATABASE IF EXISTS test;')
        mysql_base.dispose()

    def test_add_index(self):
        # prepare
        mysql_base = MySQLBase(
            host='localhost',
            port=3306,
            user='root',
            password='Hyz.js180518',
        )
        mysql_base.execute('DROP DATABASE IF EXISTS test;')
        mysql_base.execute('CREATE DATABASE IF NOT EXISTS test;')
        mysql_base.execute('USE test;')
        mysql_base.execute('CREATE TABLE IF NOT EXISTS test_table (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id));')

        # method
        add_table = AddTableMySQL(mysql_base)
        add_table.add_index('test_table', 'id', 'test_index')
        # check
        result = mysql_base.execute('SHOW INDEX FROM test_table;')
        self.assertEqual(result.fetchall()[1][2], 'test_index')

        # dispose
        mysql_base.execute('DROP DATABASE IF EXISTS test;')
        mysql_base.dispose()
