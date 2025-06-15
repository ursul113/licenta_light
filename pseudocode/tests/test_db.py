import unittest
import sqlite3
import os
import tempfile
from db import db_handler

class TestDBHandler(unittest.TestCase):
    def setUp(self):
        with sqlite3.connect('test.sqlite') as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS runs (name varchar(30), code TEXT)')
            conn.commit()
        self.handler = db_handler('test.sqlite')

    def test_insert_and_get_code(self):
        self.handler.insert_run("test1", "scrie(2+1)")
        result = self.handler.get_code("test1")
        self.assertEqual(result, [("scrie(2+1)",)])
        self.handler.insert_run("test1", "scrie(6+1)")
        result = self.handler.get_code("test1")
        self.assertEqual(result, [("scrie(6+1)",)])

    def test_get_code_names(self):
        self.handler.insert_run("test2", "code2")
        self.handler.insert_run("test3", "code3")
        names = self.handler.get_names()
        self.assertIn(("test2",), names)
        self.assertIn(("test3",), names)

    def tearDown(self):
        with sqlite3.connect('test.sqlite') as conn:
            conn.execute('DROP TABLE runs')
            conn.commit()

if __name__ == '__main__':
    unittest.main()
