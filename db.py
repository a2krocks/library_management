import sqlite3
import pandas as pd
import csv


class Books:
    def __init__(self):
        self.__conn = sqlite3.connect('database.db')
        self.__table = "books"

    def create_database(self):
        self.__conn.execute(f"""
        CREATE TABLE {self.__table} (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name varchar(255),
            book_Author varchar(255),
            book_isbn varchar(255)
        );
        """)

    def add(self, book_name, book_author, book_isbn):
        self.__conn.execute(
            f"""INSERT INTO 
            {self.__table} (
                 book_name,
                 book_Author,
                 book_isbn
            ) 
            VALUES (
                :book_name,
                :book_author,
                :book_isbn
            )""", {
                "book_name": book_name,
                "book_author": book_author,
                "book_isbn": book_isbn,
            })
        self.__conn.commit()

    def get_all(self, formed=False):
        get_query = f"SELECT * FROM {self.__table}"
        if formed:

            return pd.read_sql_query(get_query, self.__conn)
        return self.__conn.execute(get_query).fetchall()

    def get(self, size=1, formed=False):
        if type(size) == type(1):
            get_query = f"SELECT * FROM {self.__table} LIMIT {size}"
            if formed:
                return pd.read_sql_query(get_query, self.__conn)
            return self.__conn.execute(get_query).fetchmany(size)

    def delete(self, book_id):
        self.__conn.execute(f"DELETE  FROM {self.__table} WHERE book_id = :book_id", {
            "book_id": book_id,
        })
        self.__conn.commit()

    def destroy_table(self):
        self.__conn.execute(f"DROP TABLE {self.__table}")

    def add_sample_data(self):
        with open("books.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                x = str(row).split(",")
                self.add(x[10][2:-1], x[5][2:-1], x[5][2:-1])
