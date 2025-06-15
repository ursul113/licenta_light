import sqlite3
class db_handler:
    def __init__(self,db_file='identifier.sqlite'):
        self.__file=db_file

    def insert_run(self, name, code):
        names = [i[0] for i in self.get_names()]
        if name not in names:
            with sqlite3.connect(self.__file) as conn:
                conn.execute('INSERT INTO runs (name, code) VALUES (?, ?)', (name, code))
                conn.commit()
        else:
            with sqlite3.connect(self.__file) as conn:
                conn.execute('UPDATE runs SET  code=? where name=?', (code, name))
                conn.commit()
    def get_code(self,name):
        with sqlite3.connect(self.__file) as conn:
            cursor =conn.execute('SELECT code FROM runs where name=?',(name,))
            return cursor.fetchall()

    def get_names(self):
        with sqlite3.connect(self.__file) as conn:
            cursor =conn.execute('SELECT name FROM runs')
            return cursor.fetchall()
