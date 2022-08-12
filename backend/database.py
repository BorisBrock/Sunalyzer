import sqlite3


class Database:
    def __init__(self, file_name):
        self.cursor = None
        self.connection = None
        self.open(file_name)

    def __del__(self):
        self.close()

    def open(self, file_name):
        '''Opens the database connection.'''
        self.connection = sqlite3.connect(file_name)
        self.cursor = self.connection.cursor()

    def close(self):
        '''Closes the data base.'''
        self.connection.commit()
        self.connection.close()

    def execute(self, query):
        '''Executes a query and returns resulting rows.'''
        self.cursor.execute(query)
        return self.cursor.fetchall()
