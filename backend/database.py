import sqlite3


class Database:
    def __init__(self, file_name):
        self.cursor = None
        self.connection = None
        self.db_file_name = file_name

    def open(self):
        '''Opens the database connection.'''
        self.connection = sqlite3.connect(self.db_file_name)
        self.cursor = self.connection.cursor()

    def close(self):
        '''Closes the data base.'''
        self.connection.commit()
        self.connection.close()

    def execute(self, query):
        '''Executes a query and returns resulting rows.'''
        self.cursor.execute(query)
        return self.cursor.fetchall()
